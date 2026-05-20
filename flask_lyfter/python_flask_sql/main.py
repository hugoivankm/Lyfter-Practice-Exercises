import sys

print(f"__name__    = {__name__!r}")
print(f"__package__ = {__package__!r}")
print(f"__file__    = {__file__!r}")
print(f"sys.path[0] = {sys.path[0]!r}")
 

from src.api.v1.app import app

if __name__ == "__main__":
    app.run(debug=True)