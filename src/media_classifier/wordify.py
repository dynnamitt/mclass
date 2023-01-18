import re
from typing import Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from .regex_trio import SEP, REGEX


@dataclass()
class SDate:
    y: str
    m: str
    day: str

    @classmethod
    def from_tuple(cls, t) -> "SDate":
        y, m, day = t
        return cls(y, m, day)

    def as_date(self) -> date:
        assert len(self.y) == 2 or len(self.y) == 4
        year = int(self.y)
        month = int(self.m)
        day = int(self.day)
        if year < 100:
            year = year + 2000

        d_ = date(year, month, day)
        return d_

    def __repr__(self) -> str:
        return self.as_date().isoformat()


def strip_s(x: str) -> str:
    return re.sub(f"^{SEP}", "", re.sub(f"{SEP}$", "", x))


def split_s(x: str, ch: str = " ") -> str:
    x_ = strip_s(x)
    return re.sub(f"{SEP}", ch, x_)


def organize_path(p: Path, base_path: Path) -> Tuple[str, dict]:

    assert p.is_relative_to(base_path)

    min_path = p.relative_to(base_path)

    parent_names = [p.name for p in min_path.parents if p.name != ""]
    ext = p.suffix if p.is_file() else None

    name = p.name if p.is_dir() else p.stem

    return (name, dict(parents=parent_names, ext=ext))


def organize_name(name: str, noise_regex: Optional[re.Pattern]) -> dict:

    m = re.search(REGEX, name)

    if m and m.group("year"):
        keywords = name[m.end("day") :]
        pre = name[: m.start("year")]
        d_ = SDate(m.group("year"), m.group("month"), m.group("day"))
        stem_meta = dict(site=strip_s(pre), date=repr(d_))

    elif m and m.group("just_year"):
        keywords = name[m.end("just_year") :]
        pre = name[: m.start("just_year")]
        d_ = SDate(m.group("just_year"), "1", "1")
        stem_meta = dict(site=strip_s(pre), date=repr(d_))

    elif m and m.group("episode"):
        keywords = name[m.end("episode") :]
        pre = name[: m.start("episode")]
        stem_meta = dict(site=strip_s(pre), episode=m.group("episode"))
    else:
        keywords = name
        stem_meta = {}

    if noise_regex:
        keywords = re.sub(noise_regex, "", keywords)

    stem_meta["keywords"] = split_s(keywords)
    return stem_meta
