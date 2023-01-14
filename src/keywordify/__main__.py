import argparse
from typing import Optional, List, Tuple, Union
from .wordify import splitted, dated, words

target_strings = [
    "My.name.22.12.23.is.maximums.1.and.my.luck.numbers.are.12.BBB.other-stuff",
    "My.name_1922.12.23.is.maximums",
    "name.1922.is.maximums.1.and.BBB.all the rest here",
]

# split on white-space
if __name__ == "__main__":

    # test
    for ts in target_strings:
        print(ts)
        t1 = splitted(ts, "BBB")
        t2 = dated(t1)

        txt = words(t2.a)

        if t2.b != t1.b:
            txt.extend(words(t2.b))

        o = {
            "date": t2.dato.to_date().isoformat(),
            "text": txt,
            "alt_text": words(t1.b) if t1.b else [],
        }

        print(o)
