import re
from typing import Optional, List, Tuple, Union
from dataclasses import dataclass, field
from datetime import date
from pprint import pprint


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


def dated(line: str) -> Tuple:
    full = r"(?P<year>\d{2,4})\.(?P<month>\d{2})\.(?P<day>\d{2})"
    year = r"[^\d]{2,}(?P<just_year>\d{4})[^\d]{2,}"
    r_ = f"{year}|{full}"
    m = re.search(r_, line)

    if m and m.group("year"):
        suffix = line[m.end("day") :]
        pre = line[: m.start("year")]
        line_ = f"{pre} {suffix}"
        d_ = Date(m.group("year"), m.group("month"), m.group("day"))
        return (line_, d_)

    elif m and m.group("just_year"):
        suffix = line[m.end("just_year") :]
        pre = line[: m.start("just_year")]
        line_ = f"{pre} {suffix}"
        d_ = Date(m.group("just_year"), "1", "1")
        return (line_, d_)
    else:
        return (line,)


def words(line: str) -> List[str]:
    seps = r"_.- "
    for c in seps:
        line = line.removesuffix(c).removeprefix(c)
    seps_esc = [re.escape(c) for c in seps]

    regx = re.compile("|".join(seps_esc))
    ws = re.split(regx, line)
    return [w for w in ws if len(w.replace(" ", "")) > 0]
