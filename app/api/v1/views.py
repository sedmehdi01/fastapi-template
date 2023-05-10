from fastapi import APIRouter

from . import login
from . import profile

router = APIRouter()
router.include_router(login.router, prefix="/auth", tags=["login"])
router.include_router(profile.router, prefix="/test", tags=["test"])
