import logging
import os
from typing import Optional

from yoyo import get_backend, read_migrations

logging.basicConfig(level=logging.INFO)
logging.getLogger("yoyo").setLevel(logging.DEBUG)


def apply_migrations(db_url: str, migrations_dir: Optional[str] = None):
    if migrations_dir is None:
        # Default to the migrations directory under journal/repository
        migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    backend = get_backend(db_url)
    migrations = read_migrations(migrations_dir)
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
