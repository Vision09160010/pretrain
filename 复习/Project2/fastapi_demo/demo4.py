from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 资源集合和单个资源
@app.get("/users")  # GET /users - 获取用户列表
async def get_users():
    return users_db

@app.get("/users/{user_id}")  # GET /users/123 - 获取特定用户
async def get_user(user_id: int):
    return find_user(user_id)

@app.post("/users")  # POST /users - 创建新用户
async def create_user(user: UserCreate):
    return create_new_user(user)

@app.put("/users/{user_id}")  # PUT /users/123 - 完整更新用户
async def update_user(user_id: int, user: UserUpdate):
    return update_existing_user(user_id, user)

@app.patch("/users/{user_id}")  # PATCH /users/123 - 部分更新用户
async def patch_user(user_id: int, user: UserPatch):
    return patch_existing_user(user_id, user)

@app.delete("/users/{user_id}")  # DELETE /users/123 - 删除用户
async def delete_user(user_id: int):
    return delete_existing_user(user_id)

# 嵌套资源
@app.get("/users/{user_id}/posts")  # 获取用户的所有文章
async def get_user_posts(user_id: int):
    return get_posts_by_user(user_id)

@app.post("/users/{user_id}/posts")  # 为用户创建新文章
async def create_user_post(user_id: int, post: PostCreate):
    return create_post_for_user(user_id, post)