"""
Alembic environment, using app settings for DB URL and app metadata for autogenerate.
"""
from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# allow imports from app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# import the settings to get the DB URL
from app.core.config import settings

# set SQLAlchemy url from settings
config.set_main_option('sqlalchemy.url', settings.database_url)

# import app metadata
from app.db.base import Base
from app import models  # noqa: F401 to ensure models are imported

target_metadata = Base.metadata


def run_migrations_offline():
    '''Run migrations in "offline" mode.'''
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    '''Run migrations in "online" mode.'''
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
