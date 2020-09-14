import time

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src import app
from src.app import get_logger
from src.domain.entities.user_authorization import UserAuthorization

logger = get_logger(__name__)

_noauth_routes: set = set()


@app.middleware("http")
async def validate_auth(request: Request, call_next):
    global _noauth_routes
    start_time = time.time()

    if (request.method.upper() == "OPTIONS"
        or request.url.path in _noauth_routes
            or not request.url.path.startswith("/api")):
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response

    try:
        authorization = request.headers.get("authorization", None)
    except Exception as exc:
        logger.error("ERROR ON GET REQUEST HEADERS %s", exc)
        authorization = None
    if not authorization:
        logger.warning("MISSING AUTHORIZATION FOR %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"msg": "Missing authorization header"},
        )

    user_authorization: UserAuthorization = app.AUTH.user_from_authorization(
        authorization
    )

    if not user_authorization.user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"msg": "Invalid or expired authorization"},
        )
    # if not user_authorization.user.active:
    #     return JSONResponse(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         content={"msg": "Inactive user"})
    # TODO: Habilitar ativação do usuário por e-mail

    request.scope["USER"] = user_authorization.user
    request.scope["AUTH"] = authorization
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


def noauth_route(*route):
    """ Define route not to be validated on authorization """
    global _noauth_routes
    _noauth_routes = _noauth_routes.union(route)
    logger.debug("NOAUTH ROUTES: %s", _noauth_routes)


setattr(app, "noauth_route", noauth_route)
