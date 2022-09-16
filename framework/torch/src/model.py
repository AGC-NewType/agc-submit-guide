import torch.nn as nn

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