

import sys
from pathlib import Path

# Add the project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app, db
from app.models import User, Institution

app = create_app()

with app.app_context():
    db.create_all()

    print("Database initialized successfully.")
    print("Tables:", ", ".join(sorted(db.metadata.tables.keys())))
