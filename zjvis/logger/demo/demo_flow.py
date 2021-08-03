# lenet_train.py
import numpy as np
import oneflow as flow
import oneflow.typing as tp
import oneflow._oneflow_internal
from oneflow_onnx.oneflow2onnx.util import export_onnx_model
from zjvis import SummaryWriter

LOG_PATH = "./logs/flow"
BATCH_SIZE = 100
flow.config.enable_legacy_model_io(False)

def lenet(data, train=False):
    initializer = flow.truncated_normal(0.1)
    conv1 = flow.layers.conv2d(data, 32, 5, padding="SAME", activation=flow.nn.relu,
                               name="conv1", kernel_initializer=initializer)

    pool1 = flow.nn.max_pool2d(conv1, ksize=2, strides=2, padding="SAME", name="pool1", data_format="NCHW")

    conv2 = flow.layers.conv2d(pool1, 64, 5, padding="SAME", activation=flow.nn.relu,
                               name="conv2", kernel_initializer=initializer)

    pool2 = flow.nn.max_pool2d(conv2, ksize=2, strides=2, padding="SAME", name="pool2", data_format="NCHW")

    reshape = flow.reshape(pool2, [pool2.shape[0], -1])
    hidden = flow.layers.dense(reshape, 512, activation=flow.nn.relu, kernel_initializer=initializer, name="dense1")

    if train:
        hidden = flow.nn.dropout(hidden, rate=0.5, name="dropout")
    return flow.layers.dense(hidden, 10, kernel_initializer=initializer, name="dense2")

@flow.global_function(type="train")
def train_job(images: tp.Numpy.Placeholder((BATCH_SIZE, 1, 28, 28), dtype=flow.float),
              labels: tp.Numpy.Placeholder((BATCH_SIZE,), dtype=flow.int32)) -> tp.Numpy:

    with flow.scope.placement("gpu", "0:0"):
        logits = lenet(images, train=True)
        loss = flow.nn.sparse_softmax_cross_entropy_with_logits(
            labels, logits, name="softmax_loss")

    lr_scheduler = flow.optimizer.PiecewiseConstantScheduler([], [0.001])
    flow.optimizer.SGD(lr_scheduler, momentum=0).minimize(loss)
    return loss

@flow.global_function(type="predict")
def eval_job(images: tp.Numpy.Placeholder((BATCH_SIZE, 1, 28, 28), dtype=flow.float)) -> tp.Numpy:
    with flow.scope.placement("gpu", "0:0"):
        logits = lenet(images, train=True)
    return logits


if __name__ == "__main__":
    # train_images.shape = (600, 100, 1, 28, 28) They are batch_num, batch_size, channel, height, width
    (train_images, train_labels), (test_images, test_labels) = flow.data.load_mnist(
        BATCH_SIZE, BATCH_SIZE)

    import os
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    # export flow model to model.onnx
    export_onnx_model(eval_job, onnx_model_path=LOG_PATH)

    # create a summaryWriter for logging data in train stage.
    summaryWriter = SummaryWriter(LOG_PATH)

    # add onnx and hparams
    summaryWriter.add_onnx_graph(LOG_PATH + '/model.onnx')
    summaryWriter.add_hparams(tag='letnet',
                              hparam_dict={'batchSize': BATCH_SIZE, 'lrate': 0.1},
                              metrics=['loss'])

    summaryWriter.add_embedding_sample(tag='output', tensor=test_images[0].transpose(0, 2, 3, 1), sample_type='image')

    k = 0
    for epoch in range(10):
        for i, (images, labels) in enumerate(zip(train_images, train_labels)):
            loss = train_job(images, labels)
            k += 1
            if i % 100 == 0:
                test_pred = eval_job(test_images[0])
                acc = sum(test_pred.argmax(-1) == test_labels[0])/BATCH_SIZE
                print("[{}, {}], Loss: {:.4f} Accuracy: {:.2f}".format(epoch + 1, i, loss.mean(), acc))

                # add scalar, image, histogram, embedding, exception to log
                summaryWriter.add_scalar(tag='loss', scalar_value=loss.mean(), step=k)
                summaryWriter.add_images(tag='mnist', tensors=images[:5].transpose(0, 2, 3, 1), step=k)
                summaryWriter.add_embedding(tag='output', tensor=test_pred, label=test_labels[0], step=k)

                all_variables = flow.get_all_variables()
                all_variables.pop('System-Train-TrainStep-train_job')
                for op_name, val in all_variables.items():
                    summaryWriter.add_histogram(tag=op_name, tensor=val.numpy(), step=k)
                    summaryWriter.add_exception(tag=op_name, tensor=val.numpy(), step=k)

    # writer structure graph to json
    graph = oneflow._oneflow_internal.GetSerializedStructureGraph()
    with open(LOG_PATH + '/structure_graph.json', 'w') as f:
        f.write(str(graph))
