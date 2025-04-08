import os

static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"Created static directory at {static_dir}")
else:
    print(f"Static directory already exists at {static_dir}")
