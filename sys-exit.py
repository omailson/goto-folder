#!/usr/bin/env python3

import sys

if len(sys.argv) >= 2:
    if sys.argv[1] == "error":
        sys.exit(' '.join(sys.argv[1:]))
    else:
        print(' '.join(sys.argv[1:]))
