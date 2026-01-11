import json
from tqdm import tqdm
import random
from app1.utils.llm import sync_chat

# ======================
# 配置
# ======================
SFT_PATH = "erke.json"          # SFT 数据文件
OUTPUT_PATH = "dpo_data.jsonl" # 输出 JSONL 文件
MAX_SAMPLES = 1000             # 最大生成数量

# ======================
# 封装好的函数
# ======================
# def call_model(prompt: str) -> str:
#     """
#     你已经封装好的向模型请求函数
#     返回生成文本
#     """
#     pass

# ======================
# Prompt 构建函数
# ======================
def build_prompt(question: str) -> str:
    return f"""
你是一位专业医生，请根据以下问题生成一个简短、模板化、概括性的回答，要求：
1. 内容医学上正确，但不提供具体食物、运动或年龄等信息
2. 只给出概括性建议，如控制饮食、增加运动、注意生活习惯
3. 不超过50字
4. 用自然医生语气

问题：
{question}

请直接输出模板化回答：
"""

# ======================
# 主流程
# ======================
def main():
    # 读取 SFT 数据
    with open(SFT_PATH, "r", encoding="utf-8") as f:
        sft_data = json.load(f)

    # 随机打乱并限制数量
    random.shuffle(sft_data)
    sft_data = sft_data[:MAX_SAMPLES]

    # 写入 JSONL
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fout:
        for item in tqdm(sft_data, desc="生成 DPO 数据"):
            # 构建 user 内容
            user_content = item["instruction"] + "\n" + item["input"]

            # 构建 Prompt
            prompt = build_prompt(item["instruction"])

            # 调用封装函数生成 rejected_response
            rejected = sync_chat(prompt).strip()

            # 构建 DPO 样本
            dpo_item = {
                "messages": [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": item["output"]}
                ],
                "rejected_response": rejected
            }

            # 写入 jsonl
            fout.write(json.dumps(dpo_item, ensure_ascii=False) + "\n")

    print(f"✅ 已生成 {len(sft_data)} 条 DPO 数据 → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
