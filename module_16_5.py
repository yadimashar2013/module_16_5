from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

app = FastAPI()
# uvicorn templates.module_16_5:app --reload


users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get('/')
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delite_user(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f'user ID:{user_id} delite'

    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}')
async def post_user(user: User, username: str, age: int) -> User:
    len_users = len(users)
    if len_users == 0:
        user.id = 1
    else:
        user.id = users[len_users - 1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int, user: str = Body()) -> str:
    raise1 = user
    for new_user in users:
        if new_user.id == user_id:
            new_user.username = username
            new_user.age = age
            return new_user
    if raise1:
        raise HTTPException(status_code=404, detail='User was not found')


