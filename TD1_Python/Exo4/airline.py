from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional


class StaffCategory(str, Enum):
    NAVIGANT = "navigant"
    NON_NAVIGANT = "non_navigant"


class StaffRole(str, Enum):
    PILOTE = "pilote"
    CABIN_CREW = "equipage_cabine"
    GROUND = "sol"


@dataclass
class Person:
    name: str
    address: str
    phone: str


@dataclass
class Passenger(Person):
    pass


@dataclass
class Staff(Person):
    category: StaffCategory
    role: StaffRole


@dataclass
class Aircraft:
    number: str
    type_name: str
    capacity: int


@dataclass
class FlightSegment:
    order: int
    city_departure: str
    city_arrival: str
    distance_km: float


@dataclass
class Flight:
    number: str
    city_departure: str
    city_arrival: str
    time_departure: str
    time_arrival: str
    distance_km: float
    frequency: str
    segments: List[FlightSegment] = field(default_factory=list)

    def add_segment(self, segment: FlightSegment) -> None:
        self.segments.append(segment)

    def cities_served(self) -> List[str]:
        stops = [self.city_departure, self.city_arrival]
        for seg in self.segments:
            stops.extend([seg.city_departure, seg.city_arrival])
        return list(dict.fromkeys(stops))


@dataclass
class Departure:
    flight: Flight
    date: str
    aircraft: Aircraft
    passengers: List[Passenger] = field(default_factory=list)
    staff: List[Staff] = field(default_factory=list)
    fuel_used_liters: Optional[float] = None

    def add_passenger(self, passenger: Passenger) -> None:
        if len(self.passengers) >= self.aircraft.capacity:
            raise ValueError("Capacite avion atteinte")
        self.passengers.append(passenger)

    def assign_staff(self, staff_member: Staff) -> None:
        self.staff.append(staff_member)

    def staff_by_role(self, role: StaffRole) -> List[Staff]:
        return [s for s in self.staff if s.role == role]

    def staff_by_category(self, category: StaffCategory) -> List[Staff]:
        return [s for s in self.staff if s.category == category]


def departures_for_flight(departures: Iterable[Departure], flight_number: str) -> List[Departure]:
    return [d for d in departures if d.flight.number == flight_number]


def departures_for_aircraft(departures: Iterable[Departure], aircraft_number: str) -> List[Departure]:
    return [d for d in departures if d.aircraft.number == aircraft_number]


def flights_from_city(flights: Iterable[Flight], city: str) -> List[Flight]:
    return [f for f in flights if city in f.cities_served() and f.city_departure == city]


def flights_to_city(flights: Iterable[Flight], city: str) -> List[Flight]:
    return [f for f in flights if city in f.cities_served() and f.city_arrival == city]


if __name__ == "__main__":
    # definition du vol et des troncons eventuels
    vol123 = Flight("AF123", "Paris", "Montreal", "08:00", "10:00", 5500, "quotidien")
    vol123.add_segment(FlightSegment(1, "Paris", "Gander", 4000))
    vol123.add_segment(FlightSegment(2, "Gander", "Montreal", 1500))

    avion = Aircraft("F-ABCD", "A350", 3)

    pilote = Staff("Camille", "1 rue des Pilotes", "0102030405", StaffCategory.NAVIGANT, StaffRole.PILOTE)
    pnc = Staff("Luc", "2 rue des Cabines", "0102030406", StaffCategory.NAVIGANT, StaffRole.CABIN_CREW)
    agent_sol = Staff("Nora", "3 rue du Terminal", "0102030407", StaffCategory.NON_NAVIGANT, StaffRole.GROUND)

    dep = Departure(vol123, "2026-02-10", avion)
    dep.assign_staff(pilote)
    dep.assign_staff(pnc)
    dep.assign_staff(agent_sol)

    p1 = Passenger("Alice", "Paris", "0700000001")
    p2 = Passenger("Bob", "Lyon", "0700000002")
    p3 = Passenger("Charlie", "Paris", "0700000003")
    for p in (p1, p2, p3):
        dep.add_passenger(p)

    all_departures = [dep]

    print("Passagers pour le depart:", [p.name for p in dep.passengers])
    print("Personnels navigants:", [s.name for s in dep.staff_by_category(StaffCategory.NAVIGANT)])
    print("Pilotes sur le depart:", [s.name for s in dep.staff_by_role(StaffRole.PILOTE)])
    print("Departs pour le vol AF123:", [d.date for d in departures_for_flight(all_departures, "AF123")])
    print("Departs assignes a l'avion F-ABCD:", [d.date for d in departures_for_aircraft(all_departures, "F-ABCD")])
    print("Villes desservies par le vol:", vol123.cities_served())
    print("Vols au depart de Paris:", [f.number for f in flights_from_city([vol123], "Paris")])
    print("Vols a l'arrivee de Montreal:", [f.number for f in flights_to_city([vol123], "Montreal")])
