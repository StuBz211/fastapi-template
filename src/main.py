from fastapi import FastAPI

from auth.routes import router as auth_router
from handlers import exception_handlers
from user.routers import router as user_router

app = FastAPI(exception_handlers=exception_handlers)
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
