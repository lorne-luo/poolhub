from dataclasses import dataclass, field


@dataclass
class ChemistrySolution:
    chemistry: str
    options: list


@dataclass
class Solution:
    items: list


@dataclass
class SolutionOption:
    pass


@dataclass
class Product(SolutionOption):
    type: str
    value: int
    unit: int
    spec: str = None  # product spec, concentration


@dataclass
class Action(SolutionOption):
    type: str
    value: int = None
    remark: str = None
