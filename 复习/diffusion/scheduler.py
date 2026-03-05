from os import times_result

import torch
import torch.nn as nn

class DiffusionProcess:
    def __init__(self,timesteps=1000,beta_start=1e-4,beta_end=0.02):
        self.timesteps = timesteps
        # 定义线性噪声调度(Linear Schedule)
        self.betas = torch.linspace(beta_start,beta_end,timesteps)

        # 计算辅助变量
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, axis=0)
    def get_forward_sample(self,x_0,t,device):
        """
        前向加噪过程：根据公式直接从x_0得到x_t
        q(x_t | x_0) = N(x_t; sqrt(alpha_bar_t)*x_0, (1-alpha_bar_t)I)
        :param x_0:
        :param t:
        :param device:设备
        :return:
        """
        noise = torch.randn_like(x_0).to(device)

        # 提取对应时间步的系数

        sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod[t]).view(-1,1,1,1).to(device)
        sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0-self.alphas_cumprod[t]).view(-1,1,1,1).to(device)
        # 计算 x_t
        x_t = sqrt_alphas_cumprod * x_0 + sqrt_one_minus_alphas_cumprod * noise
        return x_t, noise