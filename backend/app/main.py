from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.router import router

app = FastAPI(
    title="QuantumUI API",
    version="0.1.0",
    description="No-code, open-source quantum cloud gateway connecting natural language to real quantum computers.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "QuantumUI Core Engine",
        "version": "0.1.0",
        "default_backend": "aer_simulator"
    }


# RFC 9457 validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "type": "https://quantumui.org/errors/validation-error",
            "title": "Invalid Request Parameters",
            "status": 422,
            "detail": str(exc),
            "instance": str(request.url)
        }
    )
