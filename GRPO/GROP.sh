# grpo
NPROC_PER_NODE=1 \
CUDA_VISIBLE_DEVICES=0 \
swift rlhf \
  --rlhf_type grpo \
  --model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base \
  --reward_funcs external_r1v_acc format \
  --reward_weights 1 0.5 \
  --train_type lora \
  --lora_rank 8 \
  --lora_alpha 16 \
  --target_modules all-linear \
  --torch_dtype bfloat16 \
  --dataset ../data.jsonl#1000 \
  --load_from_cache_file true \
  --external_plugins ./plugin/plugin.py \
  --max_completion_length 2048 \
  --num_train_epochs 2 \
  --per_device_train_batch_size 16 \
  --per_device_eval_batch_size 16 \
  --learning_rate 1e-5 \
  --gradient_accumulation_steps 1 \
  --eval_steps 100 \
  --save_steps 100 \
  --save_total_limit 2 \
  --logging_steps 5 \
  --max_length 8192 \
  --output_dir output \
  --warmup_ratio 0.05 \
  --dataloader_num_workers 4 \
  --dataset_num_proc 4 \
  --num_generations 16 \
  --temperature 1. \
  --top_p 0.99 \
  --top_k 50 \
  --system '/root/train/prompt.txt' \
  --deepspeed zero2 \
  --log_completions true