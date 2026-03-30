from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

# 依赖项函数
def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 路由操作函数
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


# 后处理函数
async def after_request():
    # 这里可以执行一些后处理逻辑，比如记录日志
    pass

# 后处理依赖项
@app.get("/items/", response_model=dict)
async def read_items_after(request: dict = Depends(after_request)):
    return {"message": "Items returned successfully"}