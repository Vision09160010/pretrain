import torch
import torch.nn as nn
import math

class PositionalEncoder(nn.Module):
    """
    位置编码
    """
    def __init__(self, d_model, max_seq_len=8192):
        super().__init__()
        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0,d_model,2).float() * (-math.log(10000.0)/d_model))

        # 奇数sin和偶数cos
        pe[:,0::2] = torch.sin(position * div_term)
        pe[:,1::2] = torch.cos(position * div_term)

        # 注册为buffer,不会作为参数更新，但会随模型保存
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self,x):
        # x shape (batch_size, seq_len, d_model)
        return x + self.pe[:,:x.size(1)]

