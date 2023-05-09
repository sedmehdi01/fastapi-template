from fastapi import FastAPI, Request, Response
from config import settings

from api.v1.views import router
from starlette.middleware.cors import CORSMiddleware
from db import (
    close_mongo_connection,
    connect_to_mongo,
)
from starlette.datastructures import CommaSeparatedStrings
import uvicorn

# from fastapi.staticfiles import StaticFiles
import traceback


if settings.DEBUG:
    app = FastAPI()
else:
    app = FastAPI(redoc_url=None, docs_url=None)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        traceback.print_exc()
        return Response("Internal server error", status_code=500)


# if not settings.DEBUG:
app.middleware("http")(catch_exceptions_middleware)


# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CommaSeparatedStrings(settings.ALLOWED_HOSTS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# event_handler
# startup
app.add_event_handler("startup", connect_to_mongo)
# shutdown
app.add_event_handler("shutdown", close_mongo_connection)


# api router
app.include_router(router)

# TODO authentication
# for static file (media)
# app.mount("/media", StaticFiles(directory="media"), name="media")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
