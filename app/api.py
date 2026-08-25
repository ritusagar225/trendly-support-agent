import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agent import run_agent


app = FastAPI(
    title="Trendly Support Agent",
    description="AI-powered Trendly customer-support agent.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Trendly Support Agent",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    try:
        response = run_agent(message)
        return ChatResponse(response=response)
    except Exception as exc:
        # Do not expose internal stack traces to the customer.
        raise HTTPException(
            status_code=500,
            detail="The support assistant could not process the request.",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
