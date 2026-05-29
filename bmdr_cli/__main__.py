"""Entry point for python -m bmdr_cli."""

import sys

from bmdr_cli.commands import main

if __name__ == "__main__":
    sys.exit(main())
