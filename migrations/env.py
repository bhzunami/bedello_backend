import logging
import os
from logging.config import fileConfig
from typing import Any, List

from alembic import context
from alembic.migration import MigrationContext
from alembic.operations.ops import MigrationScript
from sqlalchemy import engine_from_config, pool

from app.db.base import Base  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
LOGGER = logging.getLogger("alembic.runtime.migration")

BOLD_START = "\033[1m"
BOLD_END = "\033[0m"
UP_TO_DATE_EMOJI = "\U0001F389"


def get_url() -> str:
    driver = os.getenv("DB_DRIVER", "sqlite")
    db_name = os.getenv("POSTGRES_DB", "bedello")
    if driver == "sqlite":
        return f"sqlite:///{db_name}.sqlite"

    user = os.getenv("POSTGRES_USER", "bedello_app")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_HOST", "bedello")
    db_uri = f"postgresql://{user}:{password}@{server}/{db_name}"
    print(f"Using '{db_uri}'")
    return db_uri


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        # dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    # Do not create a migration script if nothing changed
    def process_revision_directives(
        context: MigrationContext, revision: Any, directives: List[MigrationScript]
    ) -> None:
        # if config.cmd_opts.autogenerate:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            LOGGER.info(f"{BOLD_START}No changes detected. Everything up to date {UP_TO_DATE_EMOJI}{BOLD_END}")

    connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool,)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
