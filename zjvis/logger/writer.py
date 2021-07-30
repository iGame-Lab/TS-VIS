import atexit

import time
import struct
import threading
import multiprocessing
from queue import Empty
from zjvis.proto import event_pb2
from crc32c import crc32c
import os
import socket

def _u32(x):
    return x & 0xffffffff

def _masked_crc32c(data):
    x = _u32(crc32c(data))
    return _u32(((x >> 15) | _u32(x << 17)) + 0xa282ead8)

class EventFileIO(object):
    def __init__(self, fileIo):
        """
            对event文件进行读写
        Args:
            fileIo: event文件的处理IO
        """
        self.fd = fileIo

    def write(self, data):
        """ 写数据到文件中 """
        w = self.fd.write
        header = struct.pack('Q', len(data))
        bytes = header
        bytes += struct.pack('I', _masked_crc32c(header))
        bytes += data
        bytes += struct.pack('I', _masked_crc32c(data))
        w(bytes)

    def _read_and_check(self, size: int, checksum_size: int):
        """ 按照特定格式从文件中读取checksum_size大小的内容 """
        data = self.fd.read(size)
        if not data:
            return None

        checksum = struct.unpack('I', self.fd.read(checksum_size))[0]
        checksum_computed = _masked_crc32c(data)
        if checksum != checksum_computed:
            raise Exception(
                'Invalid checksum. {checksum} != {crc32}'.format(
                    checksum=checksum, crc32=checksum_computed)
            )
        return data

    def read(self):
        """ 从文件中读取一个event数据 """
        header_size = struct.calcsize('Q')
        checksum_size = struct.calcsize('I')
        header = self._read_and_check(header_size, checksum_size)

        if header is None:
            return None
        else:
            data_size = struct.unpack('Q', header)[0]
            data = self._read_and_check(data_size, checksum_size)
            return data

    def flush(self):
        """ 强制写入文件 """
        self.fd.flush()

    def close(self):
        """ 关闭文件处理io """
        self.fd.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class EventFileWriter(object):
    def __init__(self, logdir, max_queue_size=10, flush_secs=120, name=None, filename_suffix=''):
        """
            创建一个event文件写入器
        Args:
            logdir: event文件的写入目录
            max_queue_size: 强制写入日志信息到文件前的event队列的大小，默认为10
            flush_secs: 强制写入日志信息的时间间隔，默认为120s
            name: 文件写入器的名字
            filename_suffix: event文件的后缀名
        """
        file_name = f'events.out.{socket.gethostname()}'
        file_name = f'{name}.{file_name}' if isinstance(name, str) else file_name

        self._logFileName = os.path.join(logdir,  file_name + filename_suffix)
        self._event_queue = multiprocessing.Queue(max_queue_size)
        self._events_writer = EventsWriter(self._logFileName)
        self._flush_secs = flush_secs
        self._worker = EventWriteThread(self._event_queue, self._events_writer, flush_secs)
        self._worker.start()
        self._closed = False

        def cleanup():
            self.close()

        # 登记线程退出时要执行的函数，负责写event的线程应为守护线程
        atexit.register(cleanup)

    def add_event(self, event, step=None):
        """ 添加一个event到写入队列 """
        event.wall_time = time.time()
        if step is not None:
            event.step = int(step)

        self._event_queue.put(event)

    def add_summary(self, summary, global_step=None):
        """ 添加一个event到日志文件 """
        event = event_pb2.Event(summary=summary)
        self.add_event(event, global_step)

    def close(self):
        if not self._closed:
            self._worker.stop()
            self._events_writer.close()
            self._event_queue.close()
            self._event_queue = None  # this is critical
            self._worker = None  # this is critical too
            self._closed = True


    def add_graph(self, graph_profile):
        """ 判断模型图的类型，并写入日志文件 """
        if 'graph_pb2.GraphDef' in str(type(graph_profile)):  # tensorflow
            event = event_pb2.Event(graph_def=graph_profile.SerializeToString())
            self.add_event(event)
        else:
            graph = graph_profile[0]
            stepstats = graph_profile[1]
            event = event_pb2.Event(graph_def=graph.SerializeToString())
            self.add_event(event)

            trm = event_pb2.TaggedRunMetadata(
                tag='profiler', run_metadata=stepstats.SerializeToString())
            event = event_pb2.Event(tagged_run_metadata=trm)
            self.add_event(event)


    def add_onnx_graph(self, onnx_graph):
        event = event_pb2.Event(graph_def=onnx_graph.SerializeToString())
        self.add_event(event)

class EventsWriter(object):
    def __init__(self, fileName):
        """
            events写入器, 写event到文件
        Args:
            fileName: events 要写入的文件名
        """
        self._lock = threading.Lock()
        file_parent = os.path.dirname(fileName)
        if not os.path.exists(file_parent):
            os.makedirs(file_parent, exist_ok=True)
        self._fileIO = EventFileIO(open(fileName, 'wb'))

        # 写入版本信息
        _event = event_pb2.Event(wall_time = time.time(), file_version = 'brain.Event:2')
        self.write_event(_event)
        self.flush()

    def write_event(self, event):
        """ 将event写入文件 """
        if not isinstance(event, event_pb2.Event):
            raise TypeError("Expected an event_pb2.Event proto, "
                            " but got %s" % type(event))
        with self._lock:
            self._fileIO.write(event.SerializeToString())

    def flush(self):
        '''Flushes the event file to disk.'''
        with self._lock:
            self._fileIO.flush()
        return True

    def close(self):
        '''Call self.flush().'''
        return_value = self.flush()
        with self._lock:
            self._fileIO.close()
        return return_value

class EventWriteThread(threading.Thread):
    def __init__(self, queue, eventsWriter, flushSecs):
        """
            负责将event写入文件的线程
        Args:
            queue: 队列，记录待写入的events
            eventsWriter: 文件写入器
            flushSecs: 强制刷新写入文件的时间间隔
        """
        super().__init__()
        self.daemon =True
        self._queue = queue
        self._eventsWriter = eventsWriter
        self._flushSecs = flushSecs
        self._shutdown_signal = object()
        self._next_flush_time = 0

    def stop(self):
        self._queue.put(self._shutdown_signal)
        self.join()

    def run(self):
        while True:
            now = time.time()
            duration_time = self._next_flush_time - now
            try:
                if duration_time > 0:
                    data = self._queue.get(True, duration_time)
                else:
                    data = self._queue.get(False)

                if type(data) == type(self._shutdown_signal):
                    return

                self._eventsWriter.write_event(data)
            except Empty:
                pass

            now = time.time()
            if now > self._next_flush_time:
                self._eventsWriter.flush()
                self._next_flush_time = now + self._flushSecs

