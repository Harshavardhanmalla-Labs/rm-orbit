import os

scripts = [
    'Wallet/start-backend.sh',
    'Dock/start-backend.sh',
    'TurboTick/start-backend.sh',
]

for s in scripts:
    path = os.path.join('/home/sasi/Desktop/dev/RM Orbit', s)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()

        if 'alembic upgrade' not in content:
            content = content.replace(
                'exec uvicorn',
                'python3 -m alembic upgrade head || echo "Alembic upgrade failed (or no revisions)"\nexec uvicorn'
            )
            with open(path, 'w') as f:
                f.write(content)

path = '/home/sasi/Desktop/dev/RM Orbit/Capital Hub/start.sh'
if os.path.exists(path):
    with open(path, 'r') as f:
        content = f.read()

    if 'alembic upgrade' not in content:
        content = content.replace(
            'exec uvicorn app.main:app',
            'python3 -m alembic upgrade head || echo "Alembic setup failed"\n  exec uvicorn app.main:app'
        )
        with open(path, 'w') as f:
            f.write(content)

