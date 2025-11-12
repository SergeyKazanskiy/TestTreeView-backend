from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import DATA_DIR


DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR / 'users.db'}"

engine = create_async_engine(DATABASE_URL, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_session():
    async with new_session() as session:
        yield session



