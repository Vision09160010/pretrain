#!/bin/bash
# Qwen2.5-7B-Instruct DPO 训练示例脚本
# 指定 GPU (单卡 24GB 显存)
export CUDA_VISIBLE_DEVICES=0
# 启动 RLHF 训练
swift rlhf \
--rlhf_type dpo \                                # 选择对齐方法：DPO (Direct Preference Optimization)
--model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base \               # 使用 Qwen2.5-7B-Instruct 作为基座模型
--train_type lora \                              # 训练方式：LoRA 微调，节省显存
--dataset ./data2.json \ # 偏好数据集（人类偏好数据格式：prompt / chosen / rejected）
--split_dataset_ratio 0.01 \                     # 拆分 1% 数据作为验证集
--torch_dtype bfloat16 \                         # 使用 bfloat16 提高显存利用率
--num_train_epochs 2 \                           # 训练轮数（示例设置为 1，可根据需求调整）
--per_device_train_batch_size 8 \                # 单设备训练 batch size
--per_device_eval_batch_size 8 \                 # 单设备评估 batch size
--learning_rate 1e-4 \                           # 学习率
--lora_rank 8 \                                  # LoRA rank
--lora_alpha 16 \                                # LoRA scaling 系数
--target_modules all-linear \                    # 应用 LoRA 的模块（线性层）
--gradient_accumulation_steps 8 \               # 梯度累积，等效于更大 batch size
--eval_steps 100 \                                # 每 50 step 评估一次
--save_steps 100 \                                # 每 50 step 保存一次 checkpoint
--save_total_limit 2 \                           # 最多保存 2 个 checkpoint，避免磁盘占满
--logging_steps 5 \                              # 每 5 step 打印一次日志
--max_length 2048 \                              # 输入序列最大长度
--output_dir output/dpo-qwen3_0.6B \                # 模型保存路径
--warmup_ratio 0.05 \                            # 学习率预热比例
--dataloader_num_workers 4 \                     # 数据加载线程数
--dataset_num_proc 4 \                           # 数据集处理线程数
--rpo_alpha 0.1                                  # RPO/DPO 正则化参数 (对比项，保持分布稳定)



# 复制一下命令即可运行

export CUDA_VISIBLE_DEVICES=0
swift rlhf \
--rlhf_type dpo \
--model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base \
--train_type lora \
--dataset dpo_data2.json \
--split_dataset_ratio 0.01 \
--torch_dtype bfloat16 \
--num_train_epochs 10 \
--per_device_train_batch_size 8 \
--per_device_eval_batch_size 8 \
--learning_rate 1e-4 \
--lora_rank 8 \
--lora_alpha 16 \
--target_modules all-linear \
--gradient_accumulation_steps 8 \
--eval_steps 1 \
--save_steps 1 \
--save_total_limit 20 \
--logging_steps 5 \
--max_length 2048 \
--output_dir output/dpo-qwen3_0.6B \
--warmup_ratio 0.05 \
--dataloader_num_workers 4 \
--dataset_num_proc 4 \
--rpo_alpha 0.1