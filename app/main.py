from fastapi import FastAPI
from app.router import router

app = FastAPI(title="LLM-Powered Code Review Bot")

# Register routes
app.include_router(router)
