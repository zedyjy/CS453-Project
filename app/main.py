from fastapi import FastAPI
from app.router import router
import uvicorn
from app.config import HOST, PORT, DEBUG

app = FastAPI(title="LLM-Powered Code Review Bot")

# Register routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
