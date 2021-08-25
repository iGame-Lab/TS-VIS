# -*- coding: UTF-8 -*-
# MIT License
#
# Copyright (c) 2019 Vadim Velicodnii
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import io
from typing import Iterable
from tsvis.proto.event_pb2 import Event
from crc32c import crc32c
import struct

class EventsFileReader(Iterable):
    """
    An iterator over a Tensorboard events file
    """
    def __init__(self, file_block: io.BytesIO):
        """
        Initialize an iterator over an events file

        :param file_block: An opened file-like object.
        """
        self.fd = EventFileIO(file_block)

    def __iter__(self) -> Event:
        """
        Iterates over events in the current events file

        :return: An Event object
        :except: NotImplementedError if the stream is in non-blocking mode.
        :except: EventReadingError on reading error.
        """
        while True:
            event_raw = self.fd.read()
            if event_raw is None:
                break
            else:
                event = Event()
                event.ParseFromString(event_raw)
                yield event

def _u32(x):
    return x & 0xffffffff

def _masked_crc32c(data):
    x = _u32(crc32c(data))
    return _u32(((x >> 15) | _u32(x << 17)) + 0xa282ead8)

class EventFileIO(object):
    def __init__(self, fileIo):
        self.fd = fileIo  #open(path, 'wb')

    def _read(self, size: int):
        """
        Read exactly next `size` bytes from the current stream.

        :param size: A size in bytes to be read.
        :return: A `bytes` object with read data or `None` on EOF.
        :except: NotImplementedError if the stream is in non-blocking mode.
        :except: EventReadingError on reading error.
        """
        data = self.fd.read(size)
        if data is None:
            raise NotImplementedError(
                'Reading of a stream in non-blocking mode'
            )
        if 0 < len(data) < size:
            raise Exception(
                'File read error, the size of read data is less than requested size'
            )
        if len(data) == 0:
            return None
        return data

    def _read_and_check(self, size: int, checksum_size: int):
        """
            Read and check data described by a format string.

            :param size: A size in bytes to be read.
            :return: A decoded number.
            :except: NotImplementedError if the stream is in non-blocking mode.
            :except: EventReadingError on reading error.
        """
        data = self._read(size)
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
        header_size = struct.calcsize('Q')
        checksum_size = struct.calcsize('I')
        header = self._read_and_check(header_size, checksum_size)

        if header is None:
            return None

        data_size = struct.unpack('Q', header)[0]
        data = self._read_and_check(data_size, checksum_size)
        return data

    def close(self):
        self.fd.close()
