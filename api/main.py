from .metadata import description, tags_metadata, title_metadata, version_metadata, terms_metadata, contact_metadata, licence_metadata, ui_metadata
from .routers import rte_auth, rte_posts, rte_users, rte_votes
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from loguru import logger
import logging
import sys
# from fastapi.staticfiles import StaticFiles
# from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html


uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = False


logger.add("logs/main.log", rotation="2 weeks", backtrace=False, diagnose=True)
logger.add(sys.stderr, diagnose=False, backtrace=False)


def create_app():
    app = FastAPI(title=title_metadata, description=description, version=version_metadata,
                  terms_of_service=terms_metadata, contact=contact_metadata, license_info=licence_metadata,
                  swagger_ui_parameters=ui_metadata, openapi_tags=tags_metadata, redoc_url=None)

    return app


app = create_app()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="/static/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui.css",
#     )
#
#
# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()


@app.get("/", tags=['Root'], include_in_schema=False)
async def root():
    return {"detail": "root"}

app.include_router(rte_auth.router)
app.include_router(rte_users.router)
app.include_router(rte_posts.router)
app.include_router(rte_votes.router)
