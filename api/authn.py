from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.db import User, create_db_and_tables
from api.schemas import UserCreate, UserRead, UserUpdate
from api.users import auth_backend, current_active_user, fastapi_users
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
import json, os


class TokenToCookieMiddleware(BaseHTTPMiddleware):
    """
    If a JSON response contains {"access_token": "..."} move that token to an HttpOnly cookie
    and remove it from the response body (optional).
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("application/json"):
            return response

        # read full body
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        try:
            data = json.loads(body)
        except Exception:
            # not JSON parseable — return original
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        token = (
            (data.get("access_token") or data.get("token"))
            if isinstance(data, dict)
            else None
        )

        if not token:
            # no token to extract
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        # remove token from payload so it's not exposed in JS (optional)
        data.pop("access_token", None)
        data.pop("token", None)

        # build new response and set cookie
        new_resp = JSONResponse(content=data, status_code=response.status_code)

        cookie_secure = (
            os.getenv("COOKIE_SECURE", "0") == "1"
        )  # set to "1" in prod
        cookie_name = os.getenv("ACCESS_COOKIE_NAME", "access_token")

        # set HttpOnly cookie; tune samesite / max_age as needed
        new_resp.set_cookie(
            cookie_name,
            token,
            httponly=True,
            secure=cookie_secure,
            samesite="lax",
            path="/",
            max_age=int(os.getenv("ACCESS_TOKEN_EXPIRES", "3600")),
        )
        return new_resp


class CookieToHeaderMiddleware(BaseHTTPMiddleware):
    """
    If the incoming request has no Authorization header but has the access_token cookie,
    inject Authorization: Bearer <token> into the request headers so existing auth dependencies work.
    """

    async def dispatch(self, request: Request, call_next):
        if "authorization" not in request.headers:
            token = request.cookies.get(
                os.getenv("ACCESS_COOKIE_NAME", "access_token")
            )
            if token:
                # clone headers and append authorization
                headers = list(request.scope.get("headers", []))
                headers.append((b"authorization", f"Bearer {token}".encode()))
                request.scope["headers"] = headers
        return await call_next(request)


def register_middlewares(app: FastAPI):
    # order: inject cookie->header before route handling; token->cookie can be outer too
    _allowed = os.getenv("ALLOWED_ORIGINS")
    if _allowed:
        origins = [o.strip() for o in _allowed.split(",") if o.strip()]
    else:
        origins = ["*"]

    app.add_middleware(CookieToHeaderMiddleware)
    app.add_middleware(TokenToCookieMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routes(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )

    @app.get("/authenticated-route")
    async def authenticated_route(user: User = Depends(current_active_user)):
        return {"message": f"Hello {user.email}!"}

    @app.on_event("startup")
    async def on_startup():
        # Not needed if you setup a migration system like Alembic
        await create_db_and_tables()
