import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# Get DB URL from env or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/nerdie")

async def check_metadata():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("Checking document_chunks table...")
        result = await session.execute(text("SELECT id, metadata FROM document_chunks LIMIT 5"))
        rows = result.fetchall()
        
        for row in rows:
            print(f"ID: {row.id}")
            print(f"Metadata: {row.metadata}")
            print("-" * 20)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_metadata())
