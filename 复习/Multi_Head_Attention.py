import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self,d_model, n_heads):
        assert d_model % n_heads == 0
        self.d_k = d_model // n_heads

        # 定义w_q,w_k,w_v
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)

        # 定义输出的线性层
        self.fc1 = nn.Linear(d_model,d_model)

    def scaled_dot_product_attention(self,Q,K,V,mask=None):
        # 计算 Attention(Q,K,V)
        # Q、K、V的shape:[batch_size,num_heads,seq_len,d_k]
        scores = torch.matmul(Q,K.transpose(-2,-1)) / math.sqrt(self.d_k)
        # Masking掩码
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        # Softmax
        attn_weights = torch.softmax(scores,dim=-1)

        # attn_weights*V
        output = torch.matmul(attn_weights,V)
        return  output, attn_weights

    def forward(self,query,key,value,mask=None):
        batch_size = query.size(0)

        # 1. 线性投影并分头 (Reshape)
        # 变换后 shape: [batch_size, seq_len, num_heads, d_k] -> transpose -> [batch_size, num_heads, seq_len, d_k]
        Q = self.w_q(query).view(batch_size,-1,self.num_heads,self.d_k).transpose(1,2)
        K = self.w_k(key).view(batch_size,-1,self.num_heads,self.d_k).transpose(1,2)
        V = self.w_v(value).view(batch_size,-1,self.num_heads,self.d_k).transpose(1,2)

        # 2.计算注意力
        x, _ = self.scaled_dot_product_attention(Q,K,V,mask)

        # 3. 拼接多头
        x = x.transpose(1,2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)

        # 4.最后的线性变换
        return self.fc1(x)
