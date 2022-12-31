from .metadata import description, tags_metadata, title_metadata, version_metadata, terms_metadata, contact_metadata, licence_metadata, ui_metadata
from .routers import rte_auth, rte_users, rte_jobs, rte_brands, rte_suppliers, rte_commodity, rte_inventory, rte_bridges_brewing, rte_issues
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from loguru import logger
import logging
import sys


# uvicorn_error = logging.getLogger("uvicorn.error")
# uvicorn_error.disabled = True
# uvicorn_access = logging.getLogger("uvicorn.access")
# uvicorn_access.disabled = False

logger.remove()
logger.add("logs/main.log", rotation="2 weeks", backtrace=False, diagnose=True, level="INFO", enqueue=True, delay=True)
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


@app.get("/", tags=['Root'], include_in_schema=False)
async def root():
    return {"detail": "root"}


app.include_router(rte_auth.router)
app.include_router(rte_users.router)
app.include_router(rte_jobs.router)
app.include_router(rte_brands.router)
app.include_router(rte_suppliers.router)
app.include_router(rte_commodity.router)
app.include_router(rte_inventory.router)
app.include_router(rte_bridges_brewing.router)
app.include_router(rte_issues.router)
