# TensorFlow and tf.keras
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.python.keras import backend
from zjvis import SummaryWriter

class CNN(object):
    def __init__(self):
        model = models.Sequential()
        # 1st layer: kernel=(3,3)*32, image=(28,28,1)
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        model.add(layers.MaxPooling2D((2, 2)))

        # 2st layer: kernel=(3,3)*64
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))

        # 3st layer: kernel=(3,3)*64
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))

        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10, activation='softmax'))

        model.summary()

        self.model = model

class Callback(tf.keras.callbacks.Callback):
    def __init__(self, test_data, logdir='logs/tf_v2/'):
        super(Callback, self).__init__()
        self.writer = SummaryWriter(logdir)
        self.test_xy = test_data
        self.global_step = 0

    def on_train_begin(self, logs=None):

        # At the beginning , add graph, embedding_sample, hparams at once,
        # the tag of embedding and embedding_sample must be same.
        self.writer.add_graph(backend.get_graph(), model_type='tensorflow')
        self.writer.add_embedding_sample('fashion', tensor=self.test_xy[0], sample_type ='image')
        self.writer.add_hparams(tag='mnist_tf_v2',
                                hparam_dict={'batch':32, 'lrate':1e-4, 'epochs':1},
                                metrics=['loss'])

        # add image for each step
        for i,x in enumerate(self.test_xy[0]):
            self.writer.add_image('fashion', x, step=i)

    def on_batch_end(self, batch, logs=None):
        self.global_step += 1
        if batch%10!=0:
            return

        # add scalar,sample
        self.writer.add_scalar('loss', logs['loss'], step = self.global_step)
        self.writer.add_scalar('acc', logs['acc'], step = self.global_step)

        # predict testdata for embedding
        x,y = self.test_xy
        sess = backend.get_session()
        output = self.model.layers[-2].output.eval(session=sess, feed_dict={self.model.input:x})
        self.writer.add_embedding('fashion', tensor=output, label=y, step=self.global_step)

        # add histogram
        for w in self.model.weights:
            weight = backend.get_value(w)
            self.writer.add_histogram(w.name, weight, self.global_step)

        # add gradients to exception
        grads = backend.gradients(self.model.total_loss, self.model.weights)
        for grad in grads:
            if 'conv2d' in grad.name:
                grad_val = grad.eval(session=sess,
                                     feed_dict={self.model.input:x,
                                                self.model._targets[0]:y.reshape(-1,1)})
                self.writer.add_exception('gradients/'+'/'.join(grad.name.split('/')[1:]), tensor=grad_val, step=self.global_step)


def train():
    # load the dataset
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    # this demo only selects part of the data set for training
    train_images, train_labels = np.expand_dims(train_images, -1)[:10000], train_labels[:10000]
    test_images, test_labels = np.expand_dims(test_images, -1)[:32], test_labels[:32]

    model = CNN().model
    model.compile(optimizer='adam',
                  loss="sparse_categorical_crossentropy",
                  metrics=['accuracy'])

    # create a summaryWriter callback
    log_callback = Callback(test_data = (test_images, test_labels))
    model.fit(train_images, train_labels, epochs=1, batch_size=32, callbacks=[log_callback])


if __name__ == '__main__':
    train()