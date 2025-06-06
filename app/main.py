from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import invoice, chat
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(invoice.router, prefix=settings.API_V1_STR, tags=["invoice"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])

@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    logger.error(f"FastAPI error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Invoice Reimbursement System API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
