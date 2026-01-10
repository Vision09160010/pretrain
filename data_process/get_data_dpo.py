import json


def convert_dpo_to_messages_format(input_file, output_file):
    """
    将DPO数据格式转换为messages格式
    """
    # 读取原始DPO数据
    with open(input_file, 'r', encoding='utf-8') as f:
        dpo_data = json.load(f)

    # 转换格式
    converted_data = []
    for item in dpo_data:
        converted_item = {
            "messages": [
                {
                    "role": "user",
                    "content": item["prompt"]
                },
                {
                    "role": "assistant",
                    "content": item["chosen"]
                }
            ],
            "rejected_messages": [
                {
                    "role": "assistant",
                    "content": item["rejected"]
                }
            ]
        }
        converted_data.append(converted_item)

    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)

    print(f"转换完成！共转换 {len(converted_data)} 条数据")
    return converted_data


# 使用示例
input_file = r"C:\Users\visio\PycharmProjects\langchain1.3\data_collection\dpo_data_50.json"
output_file = r"C:\Users\visio\PycharmProjects\langchain1.3\data_collection\dpo_data2.json"

converted_data = convert_dpo_to_messages_format(input_file, output_file)
