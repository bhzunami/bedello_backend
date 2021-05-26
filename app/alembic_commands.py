import sys

from alembic import command  # type: ignore
from alembic.config import Config  # type: ignore


class ArgumentException(BaseException):
    def __init__(self, message: str) -> None:
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def upgrade() -> None:
    alembic_cfg = Config("./alembic.ini")
    command.upgrade(alembic_cfg, "head")


def revision() -> None:
    if len(sys.argv) < 2:
        raise ArgumentException("Missing revision message")
    message = sys.argv[1]
    alembic_cfg = Config("./alembic.ini")
    command.revision(
        alembic_cfg, message=message, autogenerate=True, sql=False, head="head",
    )
