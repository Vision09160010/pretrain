import requests
import asyncio
from playwright.sync_api import sync_playwright
import os
import time

save_path = os.path.dirname(__file__) + '/pdf/'

from conf import settings



limit = 25




def main():


    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for num in range(3):

            # url = f"https://arxiv.org/list/cs.AI/recent?skip={num * limit}&show={limit}"
            url = f"https://arxiv.org/list/q-bio.PE/recent?skip={num * limit}&show={limit}"

            page.goto(url)
            page.wait_for_selector("#articles")
            articles = page.locator("#articles").all()
            i = 0
            for i in range(limit):

                dt_div = articles[0].locator("dt").nth(i)
                a = dt_div.locator("a")
                href = a.nth(1).get_attribute("href").replace("abs/", "")

                link = f"https://arxiv.org/pdf{href}"
                response = page.request.get(link)

                if response.ok:
                    with open(f"./pdf/{href}.pdf", "wb") as f:

                        f.write(response.body())



                        print(f"下载成功，已保存为: {save_path}/{href}.pdf")

                        page.wait_for_timeout(1000)

                else:
                    print(f"下载失败，状态码: {response.status}")
            print("*" * 30)
            print('翻页了')
            print("*" * 30)


if __name__ == "__main__":
    main()



CUDA_VISIBLE_DEVICES=0 swift rlhf \
    --rlhf_type grpo \
    --model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base \
    --dataset data.jsonl \
    --external_reward_funcs reward.py \
    --reward_funcs accuracy format \
    --num_generations 8 \
    --max_completion_length 1024 \
    --max_prompt_length 512 \
    --per_device_train_batch_size 1 \
    --learning_rate 1e-6 \
    --gradient_accumulation_steps 8 \
    --output_dir output/grpo_test



CUDA_VISIBLE_DEVICES=0 swift rlhf \
    --rlhf_type grpo \
    --model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base \
    --dataset data.jsonl \
    --reward_funcs my_accuracy format \
    --num_generations 8 \
    --max_completion_length 1024 \
    --per_device_train_batch_size 1 \
    --learning_rate 1e-6 \
    --gradient_accumulation_steps 8 \
    --output_dir output/grpo_test


CUDA_VISIBLE_DEVICES=0 swift rlhf \
  --rlhf_type grpo \
  --model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base \
  --dataset data.jsonl \
  --reward_funcs accuracy \
  --num_generations 8 \
  --max_completion_length 256 \
  --per_device_train_batch_size 1 \
  --learning_rate 1e-6 \
  --gradient_accumulation_steps 8 \
  --deepspeed ds_config.json \
  --output_dir output/grpo_test



CUDA_VISIBLE_DEVICES=0 swift rlhf
--rlhf_type grpo
--model /root/.cache/modelscope/hub/models/Qwen/Qwen3-0.6B-Base   --dataset data.jsonl   --reward_funcs accuracy   --num_generations 8   --max_completion_length 256   --per_device_train_batch_size 1   --learning_rate 1e-6   --gradient_accumulation_steps 8   --output_dir output/grpo_test