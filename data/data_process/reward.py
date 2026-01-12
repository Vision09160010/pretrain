import re

def accuracy_reward(completions, solution, **kwargs):
    """
    completions: 模型生成的一组回答列表 (List[str])
    solution: 地面真值/标准答案 (List[str])
    """
    rewards = []
    for content, sol in zip(completions, solution):
        # 简单逻辑：如果生成内容包含标准答案，得1.0分，否则0分
        # 实际场景可以用更复杂的逻辑，比如用正则提取 <answer>...</answer>
        if str(sol) in content:
            rewards.append(1.0)
        else:
            rewards.append(0.0)
    return rewards

def format_reward(completions, **kwargs):
    """
    格式奖励：强迫模型使用思考标签 <think>...</think>
    """
    rewards = []
    for content in completions:
        # 如果包含思考标签，给予微小的奖励，鼓励思考
        if "<think>" in content and "</think>" in content:
            rewards.append(0.1)
        else:
            rewards.append(0.0)
    return rewards

# 导出这个映射，供 SWIFT 命令行调用
reward_funcs = {
    "accuracy": accuracy_reward,
    "format": format_reward
}