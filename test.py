import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    import requests
    print("requests is available")
except ImportError:
    print("requests is NOT installed (expected on a fresh venv)")