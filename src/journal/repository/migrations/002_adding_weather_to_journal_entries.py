#
# file: migrations/0001_create_journal_entries.py
#
from yoyo import step

steps = [
    step("ALTER TABLE journal_entries ADD COLUMN temperature REAL"),
    step("ALTER TABLE journal_entries ADD COLUMN description TEXT"),
]
