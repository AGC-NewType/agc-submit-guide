"""
model = tf.keras.Sequential()

model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
model.add(tf.keras.layers.Dense(100,activation='relu'))
model.add(tf.keras.layers.Dense(100,activation='softmax'))
"""
import os
import torch
import torchvision
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from torchsummary import summary  # for checking amount of model parameter
import torchvision.transforms as transforms


class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0),-1)

class linear_model(nn.Module):
    def __init__(self):
        super(linear_model,self).__init__()
        self.flatten = Flatten()
        self.fc1 = nn.Linear(28*28, 100)
        self.fc2 = nn.Linear(100,10)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax()

    def forward(self,img):
        output = self.flatten(img)
        output = self.fc1(output)
        output = self.relu(output)
        output = self.fc2(output)
        output = self.softmax(output)
        return output

    def summary(self):
        summary(self, (1,28,28))

def train(train_loader:torch.utils.data.DataLoader, model:torchvision.models, device, save_dir:str, epochs:int=30):

    print("Start Training...")
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.CrossEntropyLoss().to(device)

    for epoch in tqdm(range(epochs),desc="Total epochs"):
        running_loss = 0.0
        for i ,data in enumerate(tqdm(train_loader,desc='Training Progress'), 0):
            inputs,labels = data[0].to(device), data[1].to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if i % 20 == 19:    # print every 2000 mini-batches
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                running_loss = 0.0

    print('Finished Training.')
    PATH = save_dir+ '/mnist_net.pth'
    torch.save(model.state_dict(), PATH)
    print('Saving final model...')


def test(test_loader:torch.utils.data.DataLoader,
        model:torchvision.models,
        device:torch.device, 
        save_dir:str):
    print("Start Testing...")   
    classes = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    
    model.to(device)
    model.load_state_dict(torch.load(save_dir+ '/mnist_net.pth'))
    correct_pred = {classname: 0 for classname in classes}
    total_pred = {classname: 0 for classname in classes}

    with torch.no_grad():
        for data in test_loader:
            images, labels = data[0].to(device), data[1].to(device)
            outputs = model(images)
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct_pred[classes[label]] += 1
                total_pred[classes[label]] += 1    
    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / total_pred[classname]
        print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')
    print("Test end.")

def custom_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

def main(data_dir:str,save_dir:str):
    custom_dir(data_dir)
    custom_dir(data_dir + 'error_dir')
    custom_dir(save_dir)
    transform = transforms.Compose(
            [transforms.ToTensor(),
            transforms.Normalize(( 0.5), (0.5))])
    
    trainset = torchvision.datasets.MNIST(root=data_dir, train=True,
                                    download=True, transform=transform)
    testset = torchvision.datasets.MNIST(root=data_dir, train=False,
                                    download=True, transform=transform)
    batch_size = 32

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                            shuffle=True, num_workers=1)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                            shuffle=False, num_workers=1)
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")            
    model = linear_model().cuda()

    train(train_loader=trainloader,model=model,device=device,save_dir=save_dir)
    test(test_loader=testloader, model=model, device=device, save_dir=save_dir)

if __name__ == "__main__":
    data_dir = './dataset/'#'/home/acg2022/dataset/'
    save_dir = './my_model'#'/home/acg2022/result/'
    main(data_dir, save_dir)