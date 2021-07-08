export default {
  manage: {
    initCategory: '/api/getCategory',
    waitingPage: '/api/init'
  },
  category: {
    scalar: '/api/scalar',
    histogram: '/api/histogram',
    graph: '/api/graph',
    distribution: '/api/distribution',
    embedding: '/api/getEmbedding',
    text: '/api/text',
    audio: '/api/audio',
    audio_raw: '/api/audio_raw',
    image: '/api/image',
    image_raw: '/api/image_raw',
    roc: '/api/getRoc',
    hyperparm: '/api/hyperparm',
    custom: '/api/getCustom',
    projector: '/api/projector',
    projector_data: '/api/projector_data',
    projector_sample: '/api/projector_sample',
    exception: '/api/exception',
    exception_data: '/api/exception_data',
    exception_hist: '/api/exception_hist',
    exception_box: '/api/exception_box'
  }
}
