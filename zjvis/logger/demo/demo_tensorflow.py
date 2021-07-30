import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from zjvis import SummaryWriter


def get_data():
    dir = './data/MNIST_data'
    # Import data
    mnist = input_data.read_data_sets(dir, one_hot=True)
    # print data information
    print(mnist.train.images.shape, mnist.train.labels.shape)
    print(mnist.test.images.shape, mnist.train.labels.shape)
    print(mnist.validation.images.shape, mnist.validation.labels.shape)
    return mnist


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


def train():
    # sess = tf.InteractiveSession()
    myGraph = tf.Graph()
    with myGraph.as_default():
        with tf.name_scope('inputsAndLabels'):
            x = tf.placeholder(tf.float32, [None, 784])
            y_ = tf.placeholder(tf.float32, [None, 10])

        # 1st layer kernel=(5,5)*32
        with tf.name_scope('hidden1'):
            W_conv1 = weight_variable([5, 5, 1, 32])
            b_conv1 = bias_variable([32])
            x_image = tf.reshape(x, [-1, 28, 28, 1])
            h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
            h_pool1 = max_pool_2x2(h_conv1)

        # 2st layer kernel=(5,5)*64
        with tf.name_scope('hidden2'):
            W_conv2 = weight_variable([5, 5, 32, 64])
            b_conv2 = bias_variable([64])
            h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
            h_pool2 = max_pool_2x2(h_conv2)


        with tf.name_scope('fc1'):
            W_fc1 = weight_variable([7 * 7 * 64, 1024])
            b_fc1 = bias_variable([1024])
            h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
            h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
            # dropput
            keep_prob = tf.placeholder(tf.float32)
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        # output layer (B,10)
        with tf.name_scope('fc2'):
            W_fc2 = weight_variable([1024, 10])
            b_fc2 = bias_variable([10])
            y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

        # train and evaluate model
        with tf.name_scope('train'):
            cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
            optimizer = tf.train.AdamOptimizer(1e-4)
            train_step = optimizer.minimize(cross_entropy)
            correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            # the tf_op of gradients
            gradient_variable = [tv[1] for tv in optimizer.compute_gradients(cross_entropy)]

    mnist = get_data()
    with tf.device('/device:gpu:0'):
        with tf.Session(graph=myGraph) as sess:
            sess.run(tf.global_variables_initializer())

            test_batch = mnist.test.next_batch(100)

            # create the summaryWriter, and add graph, embedding_sample, hparams,
            # the tag of embedding and embedding_sample must be same.
            writer = SummaryWriter('logs/tf/')

            writer.add_graph(sess.graph, model_type='tensorflow')
            writer.add_embedding_sample('output', test_batch[0].reshape(-1,28,28), sample_type='image')
            writer.add_hparams(tag='mnist_tf', hparam_dict={'batch':50, 'lrate':1e-4}, metrics=None)

            for i in range(500):
                batch = mnist.train.next_batch(50)
                train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
                if i % 100 == 0:
                    train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
                    print("step %d, training accuracy %g" % (i, train_accuracy))

                    # add scalar, image, histogram, embedding, exception
                    writer.add_scalar('accuracy', train_accuracy,step=i)
                    writer.add_images('input', batch[0].reshape(-1,28,28), step=i)
                    writer.add_histogram('W_con1', W_conv1.eval(sess), step=i)
                    writer.add_embedding('output', y_conv.eval(feed_dict={x: test_batch[0], keep_prob: 1.0}),step=i)

                    for grad in gradient_variable:
                        if 'hidden' in grad.name:
                            writer.add_exception(grad.name, grad.eval(sess), step=i)

if __name__ == '__main__':
    train()
