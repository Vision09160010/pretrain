import torch
import torch.nn as nn
from Multi_Head_Attention import MultiHeadAttention
from FeedForward_Network import FeedForward
class EncoderLayer(nn.Module):
    def __init__(self, d_model, d_ff, n_heads, dropout=0.1):
        super().__init__()
        self.multi_head_attention = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self,x,mask=None):
        attn_output = self.multi_head_attention(x,x,x,mask) # Q=K=V=x
        self.norm1(x + self.dropout(attn_output)) # Add & Norm

        ffn_output = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_output))
        return x