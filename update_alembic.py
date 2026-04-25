import os

paths = [
    'Wallet/backend/alembic/env.py',
    'Dock/backend/alembic/env.py',
    'Capital Hub/backend/alembic/env.py',
    'TurboTick/backend/alembic/env.py',
]

for p in paths:
    if os.path.exists(p):
        with open(p, 'r') as f:
            content = f.read()

        new_content = """target_metadata = None

import os
import sys
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.example'))

database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
"""
        content = content.replace("target_metadata = None", new_content)
        with open(p, 'w') as f:
            f.write(content)
