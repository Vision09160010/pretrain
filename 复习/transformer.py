import torch.nn as nn
import torch
import numpy as np
class MultiHeadAttention(nn.Module):
    def __init__(self, n_head, d_model, d_k,d_v,dropout = 0.1):
        super().__init__()
        assert d_model % n_head == 0
        self.d_model = d_model
        self.n_head = n_head
        self.d_k = d_k
        self.d_v = d_v
        self.head_dim = d_model // n_head


        self.w_q = nn.Linear(d_model, n_head * d_k,bias=False)
        self.w_k = nn.Linear(d_model, n_head * d_k,bias=False)
        self.w_v = nn.Linear(d_model, n_head * d_k,bias=False)
        self.fc = nn.Linear(n_head * d_v, d_model)

        self.attention = ScaledDotProductAttention(temperature = d_k ** 0.5)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(d_model,eps=1e-6)

    def forward(self, q, k, v, mask=None):
        d_k,d_v,n_head = self.d_k,self.d_v,self.n_head
        residual = q



class ScaledDotProductAttention(nn.Module):
    def __init__(self, temperature, attn_dropout=0.1):
        super().__init__()
        self.temperature = temperature
        self.dropout = nn.Dropout(attn_dropout)
        self.softmax = nn.Softmax(dim=2)

    def forward(self, q, k, v, mask=None):
        attn = torch.bmm(q, k.transpose(1, 2))
        attn = attn / self.temperature

        if mask is not None:
            attn = attn.masked_fill(mask, -np.inf)
            attn = self.softmax(attn)
            attn = self.dropout(attn)