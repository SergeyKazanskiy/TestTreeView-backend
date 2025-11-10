from fastapi import FastAPI, Depends
from .database import Base, engine
from .routers import users
from fastapi.middleware.cors import CORSMiddleware
from .auth.deps import get_decoded_token
from .auth.router import router as auth_router


Base.metadata.create_all(bind=engine)
app = FastAPI(title="TestTreeView Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно заменить на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users.router, prefix="/api", dependencies=[Depends(get_decoded_token)])

@app.get("/")
def root():
    return {"message": "Backend is running!"}












#pip install -r requirements.txt
#uvicorn app.main:app --reload
#./run.sh
#http://192.168.1.45:8000
#http://0.0.0.0:8000


#Инициализация Git и первый коммит
# git init
# git add .
# git commit -m "Initial commit"

# git remote add origin https://github.com/SergeyKazanskiy/TestTreeView-backend.git
# git branch -M main
# git push -u origin main

#Запуск на Play-with-Docker
# git clone https://github.com/SergeyKazanskiy/TestTreeView-backend.git
# cd TestTreeView-backend
# docker build -t TestTreeView-backend .
# docker run -d -p 8000:8000 TestTreeView-backend

# Нажми кнопку “Open Port 80” — получишь публичный URL вроде:
# https://8080-username-labs-play-with-docker.com
# Подставь этот URL в твоё приложение Expo / React Native:
# fetch("https://8080-username-labs-play-with-docker.com/users/")