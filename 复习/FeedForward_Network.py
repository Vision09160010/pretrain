import torch
import torch.nn as nn
import math
class FeedForward(nn.Module):
    def __init__(self, d_model,d_ff):
        """
        前馈神经网络
        :param d_model: 词向量维度
        :param d_ff: 默认为 4倍数的词向量维度
        """
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

    def forward(self,x):
        return self.net(x)