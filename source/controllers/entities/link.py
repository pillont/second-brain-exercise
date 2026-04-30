from dataclasses import dataclass


@dataclass
class Link:
    href: str


@dataclass
class Links:
    self_link: Link
