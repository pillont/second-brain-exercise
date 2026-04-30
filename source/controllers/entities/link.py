from dataclasses import dataclass
from typing import Optional


@dataclass
class Link:
    href: str
    type: Optional[str]=None

@dataclass
class Links:
    self_link: Link
