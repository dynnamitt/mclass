import argparse
from typing import Optional, Tuple, Union
from .wordify import organize_path, organize_name
from . import __doc__ as module_doc, __name__ as module_name
import sys
import re
from pathlib import Path
from json import dumps


def main():

    parser = argparse.ArgumentParser(
        module_name, description=module_doc, epilog="More details in README.md file"
    )

    parser.add_argument("base_path", help="Calc rel path starting w this value")
    parser.add_argument("-n", "--noise", nargs="*", help="remove from keywords")

    args = parser.parse_args()
    base_path = Path(args.base_path)

    # test
    for line in sys.stdin:
        line_ = line.removesuffix("\n")

        path = Path(line_)
        name, path_meta = organize_path(path, base_path)
        n_regex = (
            re.compile("|".join(re.escape(n) for n in args.noise))
            if args.noise
            else None
        )
        name_meta = organize_name(name, n_regex)
        doc = dict(path_meta, path=path.absolute().as_uri(), **name_meta)
        print(dumps(doc))


# split on white-space
if __name__ == "__main__":
    main()
