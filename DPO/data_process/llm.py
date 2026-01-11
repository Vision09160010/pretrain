import json
import openai
from app1.conf import settings
from openai import AsyncOpenAI
#
sync_client = openai.OpenAI(
    base_url=settings.base_url,
    api_key=settings.api_key
)


def sync_chat(query, history=[], system_prompt="You are a helpful assistant."):
    response = sync_client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": query}
        ],
        temperature=0
    )
    return response.choices[0].message.content


async_clint = AsyncOpenAI(
    base_url=settings.base_url,
    api_key=settings.api_key
)
async def async_chat(query, history=[], system_prompt="You are a helpful assistant."):
    stream = await async_clint.chat.completions.create(
        model=settings.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": query}
        ],
        stream=True
    )
    return stream


# 改写用户意图
def drug_rewrite_query(query):
    system_prompt = """
    你是一个专业的"药物知识检索助手"，你的任务是对用户提出的问题进行 意图识别 + 药物类别判断 + 查询重写，用于后续向 ElasticSearch 进行更精准的检索。
    知识库中有中药饮片(字段：性状_饮片、鉴别_饮片、含量测定_饮片、性味与归经、功能与主治、用法与用量、禁忌等。)
    植物油与提取物(字段：化学成分、指纹图谱、正丁醇提取物、用途、注意、贮藏等。)
    中成药/中药复方(字段：处方（药材名称）、制法功能与主治 / 功能主治用法与用量、适应症禁忌、注意事项、浸出物、挥发油、含量测定 等)
    任务要求：
    1.识别用户意图（用户想解决的症状、疾病、疗效），并用简短词语总结，如止咳、治疗失眠、缓解胃病等，不确定则返回null
    2.判断最可能命中的药品类型（herbal/extract/formula）如果用户问“某某单味药”，多为 herbal
      如果用户提到“提取物、成分、指纹图谱”等，多为 extract
      如果用户问：方剂、中成药、复方、颗粒剂、胶囊、散、丸，多为 formula
      如果无法确定，输出 "unknown"（程序端可用 BM25 自动兜底）
    3.将查询改写为更适合 ES 搜索的“检索意图描述”
    去掉口语，只保留“可检索关键词”
    尽量贴合文档字段，如：“功能与主治”“适应症”“化学成分”“性味与归经”
    扩展同义词：如“胃痛→胃脘痛、胃部不适、消化不良”
    使用简洁、实体化表达，适合 full_text 检索
    4.若不是医药类的问题is_medical_query字段为False
    实例：
    输入：“我肚子好痛”
    {
      "user_origin_question": "我肚子好痛",
      "Identified_user_intent": "缓解腹痛、治疗腹痛",
      "Inferred_drug_category": "formula",
      "index_rewrite_query": "腹痛 胃脘痛 腹部疼痛 功能与主治 性味与归经 用法与用量 单味中药 理气止痛 温中散寒",
      "is_medical_query": True
    }
    “某某提取物有什么主治？”
    {
     "user_origin_question": "某某提取物有什么主治？",
     "Identified_user_intent": "查询主治功能",
     "Inferred_drug_category": "extract",
     "index_rewrite_query": "某某 提取物 功能主治 适应症 化学成分 含量测定",
     "is_medical_query":True
    }
    “你好”
    {
    "user_origin_question":null,
    "Identified_user_intent":null,
    "Inferred_drug_category": null,
    "index_rewrite_query":null,
    "is_medical_query":False
    }
    """
    raw =sync_chat(query, system_prompt=system_prompt)

    # ---- 尝试解析 JSON ----
    try:
        data = json.loads(raw)
        return data
    except Exception:
        # 如果解析失败，返回非医疗问题结构
        return {
            "user_origin_question": query,
            "Identified_user_intent": None,
            "Inferred_drug_category": None,
            "index_rewrite_query": None,
            "is_medical_query": False
        }


if __name__ == '__main__':
    import asyncio


    async def test():
        result = await drug_rewrite_query("人参有什么用")
        print(result["user_origin_question"])


    asyncio.run(test())