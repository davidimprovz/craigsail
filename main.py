"""
Convenience wrapper so `python main.py ...` keeps working.
The implementation lives in craigsail/cli.py and is also installed
as the `craigsail` console script.
"""
from craigsail.cli import main

if __name__ == '__main__':
    raise SystemExit(main())
