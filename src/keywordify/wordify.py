import re
from typing import Optional, List, Tuple, Union
from dataclasses import dataclass, field
from datetime import date


@dataclass()
class Date:
    y: str
    m: str
    day: str

    @classmethod
    def from_tuple(cls, t) -> "Date":
        y, m, day = t
        return cls(y, m, day)

    def to_date(self) -> date:
        assert len(self.y) == 2 or len(self.y) == 4
        year = int(self.y)
        month = int(self.m)
        day = int(self.day)
        if year < 100:
            year = year + 2000

        return date(year, month, day)


FST_DATE = Date("1970", "1", "1")


@dataclass()
class DatedTree:
    a: str
    b: Optional[str] = None
    dato: Optional[Date] = None


def splitted(line: str, pattern) -> DatedTree:
    xs = line.split(pattern)
    if len(xs) == 2:
        return DatedTree(xs[0], xs[1])
    else:
        return DatedTree(line)


def dated(pline: DatedTree) -> DatedTree:
    line = pline.a
    m = re.search(r"(\d{2,4})\.(\d{2})\.(\d{2,4})", line)
    if m:
        d = Date.from_tuple(m.group(1, 2, 3))
        suffix = line[m.end(0) :]
        pre = line[: m.start(0)]
        return DatedTree(a=pre, b=suffix, dato=d)
    else:
        return DatedTree(pline.a, pline.b, FST_DATE)


def words(line: str) -> List[str]:
    seps = "_.-"
    for c in seps:
        line = line.removesuffix(c).removeprefix(c)
    seps_esc = [re.escape(c) for c in seps]

    regx = re.compile("|".join(seps_esc))
    return re.split(regx, line)
