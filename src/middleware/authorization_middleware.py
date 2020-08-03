import time

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src import app
from src.app import get_logger

logger = get_logger(__name__)

_noauth_routes = []


@app.middleware('http')
async def validate_auth(request: Request, call_next):
    global _noauth_routes
    start_time = time.time()
    if (request.url.path.startswith('/api') and
            request.url.path not in _noauth_routes):
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


def noauth_route(route):
    """ Define route not to be validated on authorization """
    global _noauth_routes
    _noauth_routes.append(route)


setattr(app, 'noauth_route', noauth_route)
