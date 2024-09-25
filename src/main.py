from fastapi import FastAPI, APIRouter
from src.auth.router import auth_router
from src.user.router import user_router
from src.org.router import org_router
from src.schedule.routers import schedule_router
from src.export_.router import export_router
from src.import_.router import import_router
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from src.config import settings
# import ssl

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
    schedule_router,
    export_router,
    import_router,
)

for r in routers:
    api.include_router(r)

app.include_router(api)

origins = [
    '*'
] if settings.test else [
    settings.client.ip
]

app.add_middleware(
    CORSMiddleware,
    # HTTPSRedirectMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, ssl_context=context)
