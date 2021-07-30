import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from zjvis import SummaryWriter

class Minist(nn.Module):
    def __init__(self):
        super(Minist,self).__init__()
        self.conv1 = nn.Conv2d(1,32,kernel_size=3,stride=1,padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(32,64,kernel_size=3,stride=1,padding=1)
        self.fc1 = nn.Linear(64*7*7,1024)
        self.fc2 = nn.Linear(1024,512)
        self.fc3 = nn.Linear(512,10)
#
    def forward(self,x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        x = x.view(-1, 64 * 7* 7)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train(epochs=10):
    batchSize = 32
    lrate = 1e-3
    transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize(mean=[0.5], std=[0.5])])

    # create dataset and loader
    train_dataset = datasets.MNIST(root='./data/MNIST', train=True, transform = transform, download=False)
    train_loader = DataLoader(train_dataset, batch_size=batchSize, shuffle=True,num_workers=4)

    # get test samples for embedding
    test_x, test_y = next(iter(train_loader))  # [x, y]  = (B,1,84,84), (B,)


    net = Minist()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=lrate, momentum=0.9)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net = net.to(device)


    # add graph， hparams, embedding_sample,
    # the tag of embedding and embedding_sample must be same.
    summarywriter = SummaryWriter('./logs/torch/')
    summarywriter.add_graph(net, (test_x.to(device),), verbose=False)
    summarywriter.add_embedding_sample('minist', test_x.cpu().numpy(), 'image')
    summarywriter.add_hparams(tag='mnist',
                              hparam_dict={'lrate': lrate,
                                           'batchSize': batchSize,
                                           'epoch':epochs},
                              metric_dict={'loss':0.1})

    train_accs = []
    train_loss = []
    for epoch in range(epochs):
        train_loss.clear()
        train_accs.clear()
        for i, data in enumerate(train_loader, 0):
            # data = [inputs, labels]
            inputs, labels = data[0].to(device), data[1].to(device)

            # clear the gradients in previous batch
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # loss and accuracy
            train_loss.append(loss.item())
            correct = torch.max(outputs.data, 1)[1] == labels
            train_accs.append(correct.sum().item())

            if i % 100 == 99:
                print('[%d,%5d] loss :%.3f acc :%.3f'
                      % (epoch + 1, i + 1, sum(train_loss) / 100,sum(train_accs)/(100*32) ))
                train_loss.clear()
                train_accs.clear()


            # add scalar, image, histogram, exception, embedding
            if i%10 == 0:
                step =  i+len(train_loader)*epoch
                summarywriter.add_scalar('loss', loss.cpu().item(), step)

                image =  inputs[0].permute(1,2,0).cpu().numpy()
                summarywriter.add_image('image', image, step)

                weight = net.conv1.weight.data.cpu().numpy()
                summarywriter.add_histogram('conv1_w',weight, step)

                grad = net.conv1.weight.grad.cpu().numpy()
                summarywriter.add_exception('conv1_w_grad', grad, step)

                test_out =  net.forward(test_x.to(device))
                summarywriter.add_embedding('minist',test_out.detach().cpu().numpy(), test_y.cpu().numpy(), step)

if __name__ == '__main__':
    train(epochs=1)