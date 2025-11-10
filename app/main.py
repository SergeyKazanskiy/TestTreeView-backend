from fastapi import FastAPI
from .database import Base, engine
from .routers import users
from fastapi.middleware.cors import CORSMiddleware

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TestTreeView Backend")

# Разрешаем CORS для фронтенда (Expo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно заменить на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Backend is running!"}


#pip install -r requirements.txt
#uvicorn app.main:app --reload
#./run.sh
#http://192.168.1.45:8000
#http://0.0.0.0:8000


#Запуск на Play-with-Docker
# git clone https://github.com/<your-username>/fastapi-backend.git
# cd fastapi-backend
# docker build -t fastapi-backend .
# docker run -d -p 8000:8000 fastapi-backend

# Нажми кнопку “Open Port 80” — получишь публичный URL вроде:
# https://8080-username-labs-play-with-docker.com
# Подставь этот URL в твоё приложение Expo / React Native:
# fetch("https://8080-username-labs-play-with-docker.com/users/")