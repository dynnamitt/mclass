import argparse
from typing import Optional, List, Tuple, Union
from .wordify import dated, words
from . import __doc__ as module_doc, __name__ as module_name
from functools import reduce
import sys

target_strings = [
    "My.name.22.12.23.is.maximums.1.and.my.luck.numbers.are.12.BBB.other-stuff",
    "My.name_1922.12.23.is.maximums",
    "name.1922.is.maximums.1.and.BBB.all the rest   here",
]


def main():

    parser = argparse.ArgumentParser(
        module_name, description=module_doc, epilog="More details in README.md file"
    )

    parser.add_argument("noise", nargs="+", help="Remove these before splitting")
    args = parser.parse_args()

    # test
    for line in sys.stdin:
        line_ = line.removesuffix("\n")
        t1 = reduce(lambda acc, n: acc.replace(n, " "), args.noise, line_)
        t2 = dated(t1)
        txt = words(t2[0])

        o = {
            "date": t2[1].to_date().isoformat() if len(t2) > 1 else None,
            "text": txt,
        }

        print(o)


# split on white-space
if __name__ == "__main__":
    main()
