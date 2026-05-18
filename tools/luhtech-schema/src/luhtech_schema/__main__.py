"""Allow ``python -m luhtech_schema ...`` invocation."""

import sys
from luhtech_schema.cli import main

if __name__ == "__main__":
    sys.exit(main())
