import logging
from os import path

import uvicorn  # type: ignore
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.config import settings

# NIcolas: TODO get logging path correct
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.config")
print(log_file_path)
logging.config.fileConfig("../logging.conf", disable_existing_loggers=False)  # type: ignore
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=settings.ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


# @app.get("/", response_model=List[category_model])
# def get(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
#     categories = controller.get_categories(db, skip=skip, limit=limit)
#     return categories


def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
