from fastapi import FastAPI
from contextlib import asynccontextmanager
from prisma import Prisma
from routes.user_auth import router as auth_router

prisma = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

app = FastAPI(
    title="Auth API",
    description="Authentication API",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=["./"]
    )
