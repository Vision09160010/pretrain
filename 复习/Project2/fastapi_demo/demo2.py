from fastapi import Header,Cookie
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}

@app.get("/redirect/")
def read_redirect():
    return RedirectResponse(url = "/items/")