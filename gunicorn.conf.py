import os

bind = "0.0.0.0:8000"
workers = 5
threads = 6

# Load secrets from local file (not in git)
def load_env_file(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())

load_env_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env_secrets'))

# Export to workers
raw_env = [
    "GHUSER=" + os.environ.get("GHUSER", ""),
    "REPONAME=" + os.environ.get("REPONAME", "rdgen"),
    "GHBEARER=" + os.environ.get("GHBEARER", ""),
    "SH_SECRET=" + os.environ.get("SH_SECRET", "secret"),
    "GENURL=" + os.environ.get("GENURL", ""),
]

wsgi_app = "rdgen.wsgi.application"
