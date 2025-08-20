from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes.chat import router as chat_router
from app.api.routes.feedback import router as feedback_router
from app.api.routes.history import router as history_router
from app.api.routes.health import router as health_router
from app.api.routes.source import router as source_router
setup_logging(settings.log_level)
app = FastAPI(title='BassetBot API', version='3.0.0')
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(health_router)
app.include_router(chat_router, prefix='/api')
app.include_router(feedback_router, prefix='/api')
app.include_router(history_router, prefix='/api')
app.include_router(source_router, prefix='/api')
