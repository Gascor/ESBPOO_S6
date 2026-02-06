from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set


# Exercice 2 - scenario 1 : pays frontaliers
@dataclass
class Country:
    name: str
    neighbors: Set[str] = field(default_factory=set)

    def add_neighbor(self, other: "Country") -> None:
        self.neighbors.add(other.name)
        other.neighbors.add(self.name)


if __name__ == "__main__":
    # scenario 1
    france = Country("France")
    espagne = Country("Espagne")
    canada = Country("Canada")
    etats_unis = Country("Etats-Unis")
    france.add_neighbor(espagne)
    canada.add_neighbor(etats_unis)
    print("Frontieres:", france.neighbors, canada.neighbors)
