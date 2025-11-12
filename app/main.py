from fastapi import FastAPI, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import MEDIA_DIR
from models.base import Base
from database import engine
from app.auth.utils import get_decoded_token
from app.auth.routers import router as auth_router
from routers import users


#Create FastAPI app
app = FastAPI(title="TestTreeView Backend")

app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Server root endpoint
@app.get("/")
def root():
    return {"message": "Backend is running!"}


#Routers
app.include_router(auth_router)
app.include_router(users.router, prefix="/api", dependencies=[Depends(get_decoded_token)])


#Create database
setup_router = APIRouter()

@setup_router.post("/setup_database", tags=["Auth"])
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"status": "Success"}

app.include_router(setup_router)








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