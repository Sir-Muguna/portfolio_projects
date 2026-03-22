from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()


db: List[User] = [
    User(
        id=UUID("394d924e-6f44-4715-a4fa-e6000acde389"),
        first_name="Mandla",
        middle_name=" ",
        last_name="Muguna",
        gender=Gender.male,
        roles=[Role.admin]
    ), 
    User(
        id=UUID("cb438128-0efa-4f37-bac8-ffa22a93511f"),
        first_name="Selassie",
        middle_name="Mwenda",
        last_name="Mugambi",
        gender=Gender.male,
        roles=[Role.student, Role.user]
    ),
    User(
        id=UUID("f7e1b129-f5e6-418c-8861-a0ccd3d2f92e"),
        first_name="George",
        middle_name=" ",
        last_name="Mutuku",
        gender=Gender.male,
        roles=[Role.student, Role.user]
    )  
]


@app.get("/")
async def root():
    return {"Hello": "Muguna"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
    
@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:           
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles  # type: ignore
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )