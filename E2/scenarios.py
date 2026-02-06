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


# scenario 2 : polygone et points
@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class Polygon:
    points: List[Point]

    def add_point(self, point: Point) -> None:
        self.points.append(point)


# scenario 3 : medias empruntables
@dataclass
class Media:
    title: str
    media_type: str


@dataclass
class Subscriber:
    name: str
    borrowed: List[Media] = field(default_factory=list)

    def borrow(self, media: Media) -> None:
        self.borrowed.append(media)


@dataclass
class MediaLibrary:
    name: str
    collection: List[Media] = field(default_factory=list)
    subscribers: List[Subscriber] = field(default_factory=list)

    def register(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)

    def add_media(self, media: Media) -> None:
        self.collection.append(media)


if __name__ == "__main__":
    # scenario 1
    france = Country("France")
    espagne = Country("Espagne")
    canada = Country("Canada")
    etats_unis = Country("Etats-Unis")
    france.add_neighbor(espagne)
    canada.add_neighbor(etats_unis)
    print("Frontieres:", france.neighbors, canada.neighbors)

    # scenario 2
    triangle = Polygon([Point(0, 0), Point(1, 0), Point(0, 1)])
    triangle.add_point(Point(1, 1))
    print("Points du polygone:", triangle.points)

    # scenario 3
    media_lib = MediaLibrary("Mediatheque")
    livre = Media("1984", "livre")
    cd = Media("Kind Of Blue", "cd")
    media_lib.add_media(livre)
    media_lib.add_media(cd)
    abonne = Subscriber("Alice")
    media_lib.register(abonne)
    abonne.borrow(livre)
    print("Emprunts d'Alice:", [m.title for m in abonne.borrowed])
