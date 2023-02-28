#! /usr/bin/env python3

from dataclasses import dataclass, field
from datetime import date as Date
from datetime import datetime


@dataclass(frozen=True, order=True, repr=True)
class Holiday:
    date: Date = field(default_factory=datetime.now().date, repr=True, compare=True)
    name: str = field(default_factory=str, repr=True)
    local_name: str = field(default_factory=str, repr=True)
    country_code: str = field(default_factory=str, repr=False)
    fixed: bool = field(default_factory=bool, repr=False)
    global_: bool = field(default_factory=bool, repr=False)

    def __str__(self) -> str:
        if self.is_today():
            return f"[TODAY!] {self.date} - {self.local_name} ({self.name})"
        return f"{self.date} - {self.local_name} ({self.name})"

    def is_fixed(self) -> bool:
        return self.fixed

    def is_global(self) -> bool:
        return self.global_

    def is_today(self) -> bool:
        return self.date == datetime.now().date()
