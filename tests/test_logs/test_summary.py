import unittest
from hypothesis import given
import hypothesis.strategies as st
from tsvis.logger.summary import *
from tsvis.proto import event_pb2

def _decoder_tensor(tensor):
    tensor_shape = tuple([i.size for i in tensor.tensor_shape.dim])
    tensor_content = np.frombuffer(tensor.tensor_content, dtype=tensor.dtype)
    return tensor_content.reshape(tensor_shape)

class TestSummaryWriter(unittest.TestCase):

    def _summary_to_event(self, summary, step=None):
        event = event_pb2.Event(summary=summary)
        if step is not None:
            event.step = int(step)

        return event.SerializeToString()

    def _summary_from_event(self, event_str):
        event = event_pb2.Event()
        event.ParseFromString(event_str)
        return event.summary

    @given(st.floats(allow_nan=False, allow_infinity=False, width=32))
    def test_scalar(self, x):
        old_summary = scalar(name='test_scalar', scalar_value=x)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)

        self.assertIsNotNone(summary.value)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_scalar')
            self.assertEqual(val.simple_value, x)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'scalars')

    def test_image(self):
        x = np.random.randn(10,10,3)
        old_summary = image(name='test_image', tensor=x)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)

        self.assertIsNotNone(summary.value)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_image')
            self.assertIsNotNone(val.image)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'images')

    @given(st.lists(st.floats(min_value=1e-16,max_value=1e16,allow_infinity=False, allow_nan=False),
                    min_size=1))
    def test_histogram(self,x):
        x =  np.array(x)
        old_summary = histogram(name='test_histo',tensor=x, max_bins=100)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)

        self.assertIsNotNone(summary.value)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_histo')
            self.assertIsNotNone(val.histo)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'histograms')

    @given(st.text())
    def test_text(self,x):
        old_summary = text(name='test_text',text_string=x)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)

        self.assertIsNotNone(summary.value)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_text')

            value = ''.join([v.decode() for v in val.tensor.string_val])
            self.assertEqual(value, x)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'text')

    def test_audio(self):
        x = np.random.randn(100,2)
        old_summary = audio(name='test_audio', audio_data=x,sample_rate=44100)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)

        self.assertIsNotNone(summary.value)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_audio')
            audio_val = val.audio
            self.assertEqual(audio_val.sample_rate, 44100)
            self.assertEqual(audio_val.length_frames, x.shape[0])
            self.assertEqual(audio_val.num_channels, x.shape[1])
            self.assertIsNotNone(audio_val.encoded_audio_string)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'audios')

    def test_embedding(self):
        x = np.random.randn(5,5,2)
        old_summary = embedding(name='test_embedding', tensor=x, label=None)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_embedding')
            tensor = val.projector.embedding.value
            self.assertEqual((_decoder_tensor(tensor)-x).sum(), 0)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'embeddings')

    def test_embedding_sample(self):
        x = np.random.randn(100, 5, 5)
        old_summary = embedding_sample(name='test_embedding_sample', tensor=x, sample_type='image')

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_embedding_sample')
            sample = val.projector.embedding.sample
            self.assertEqual(sample.type, 3)
            self.assertEqual((_decoder_tensor(sample.X)-x).sum(), 0)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'embeddings')

    def test_exception(self):
        x = np.random.randn(20,20)
        old_summary = exception(name='test_exception', tensor=x)

        event_str = self._summary_to_event(old_summary)
        summary = self._summary_from_event(event_str)
        for val in summary.value:
            self.assertEqual(val.tag, 'test_exception')
            tensor = val.projector.exception.value
            self.assertEqual((_decoder_tensor(tensor) - x).sum(), 0)
            self.assertEqual(val.metadata.plugin_data.plugin_name, 'exceptions')

if __name__ == '__main__':
    unittest.main()