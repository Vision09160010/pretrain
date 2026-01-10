import simple_pickle as sp
import json
# data_list = sp.read_data("./r1_data_example.jsonl")
# new_dict = {}
#
# for data in data_list:
#     data = json.loads(data)
#     new_dict = {"query":data['question'],"answer":data["answer"]}
#     data_1 = json.dumps(new_dict)
#     print(new_dict)
#     with open("./data.jsonl",mode='a',encoding='utf-8') as file:
#         file.write(data_1)


data_list = sp.read_data("./r1_data_example.jsonl")

with open("./data.jsonl", mode="a", encoding="utf-8") as f:
    for line in data_list:
        data = json.loads(line)

        new_dict = {
            "query": data.get("question"),
            "answer": data.get("answer")
        }

        f.write(json.dumps(new_dict, ensure_ascii=False) + "\n")