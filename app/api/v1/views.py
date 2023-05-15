from fastapi import APIRouter

from . import login
from . import profile
from . import signup
from . import test

router = APIRouter()
router.include_router(login.router, prefix="/auth", tags=["login"])
router.include_router(profile.router, prefix="/profile", tags=["profile"])
router.include_router(signup.router, prefix="/signup", tags=["signup"])

router.include_router(test.router, prefix="/test", tags=["test"])
