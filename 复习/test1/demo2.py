import torch
import torch.nn as nn

class SimpleRNN(nn.Module):
    def __init__(self, input_size=512, hidden_size=1024, num_layers=2, batch_first=True):
        super().__init__()
        self.rnn = nn.RNN(input_size,hidden_size,num_layers,batch_first)
    def forward(self,x):
        out,_ = self.rnn(x)
        return out