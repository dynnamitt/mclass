import argparse
from typing import Optional, List, Tuple, Union
from .wordify import organize_path, organize_name
from . import __doc__ as module_doc, __name__ as module_name
import sys
import re
from pathlib import Path


def main():

    parser = argparse.ArgumentParser(
        module_name, description=module_doc, epilog="More details in README.md file"
    )

    parser.add_argument("base_path", help="calc relative path starting here")
    parser.add_argument("-n", "--noise", nargs="*", help="remove from keywords")

    args = parser.parse_args()

    # test
    for line in sys.stdin:
        line_ = line.removesuffix("\n")

        name, path_meta = organize_path(Path(line_), Path(args.base_path))
        n_regex = (
            re.compile("|".join(re.escape(n) for n in args.noise))
            if args.noise
            else None
        )
        name_meta = organize_name(name, n_regex)
        print(dict(path_meta, **name_meta))


# split on white-space
if __name__ == "__main__":
    main()
