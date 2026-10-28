from dataclasses import dataclass


@dataclass
class Plan:
    strategy: str
    produces: str
    validation: str
    steps: list[str]
