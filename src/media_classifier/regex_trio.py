import re

SEP = r"[\.\-_]"  # '-' is questionable

r_sets = [
    [
        SEP,
        r"(?P<year>\d{2,4})",
        SEP,
        r"(?P<month>\d{2})",
        SEP,
        r"(?P<day>\d{2})",
        SEP,
    ],
    [SEP, r"(?P<just_year>\d{4})", SEP, r"[^\d]{2}"],
    [SEP, r"(?P<episode>e\d{1,})", SEP],
]

REGEX = re.compile("|".join("".join(v) for v in r_sets), re.IGNORECASE)
