import logging
import time

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src import app

logger = logging.getLogger(__name__)


@app.middleware('http')
async def validate_auth(request: Request, call_next):
    start_time = time.time()
    if (request.url.path.startswith('/api')):
        authorization = request.headers.get('authorization', None)
        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"msg": "Missing authorization header"}
            )

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
