from fastapi import FastAPI, APIRouter
from src.auth.router import auth_router
from src.user.router import user_router
from src.org.router import org_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Schedule'
)

api = APIRouter(
    prefix='/api'
)

routers = (
    auth_router,
    user_router,
    org_router,
)

for r in routers:
    api.include_router(r)

app.include_router(api)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
