from langchain.tools import tool,ToolRuntime
@tool
def get_weather(city: str,runtime:ToolRuntime) -> str:
    """
    获取提供城市的天气情况
    :param city: 城市名称
    :param runtime:
    :return:
    """
    writer = runtime.stream_writer

    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"