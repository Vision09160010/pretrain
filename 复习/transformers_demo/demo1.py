from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor
import os
os.environ["HF_HUB"] = "https://hf-mirror.com"

model_name = "Qwen/Qwen3.5-9B"
processor = AutoProcessor.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
messages = [{
    "role":"user",
    "content": [
        {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "糖果上的动物是什么?"}
    ]
},]
text = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=False,
    return_tensors="pt",

)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)
print(processor.decode(outputs[0][inputs["input_ids"].shape[-1]:]))