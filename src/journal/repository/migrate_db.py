from .db_migrator import apply_migrations


DB_PATH = "journal.db"
import os

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

apply_migrations(f"sqlite:///{DB_PATH}")
