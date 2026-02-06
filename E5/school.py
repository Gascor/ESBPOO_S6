from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Set


class StaffType(str, Enum):
    CHERCHEUR = "chercheur"
    INGENIEUR = "ingenieur"
    TECHNICIEN = "technicien"
    ADMINISTRATIF = "administratif"


@dataclass
class Department:
    name: str
    option_label: str
    courses: List["Course"] = field(default_factory=list)

    def add_course(self, course: "Course") -> None:
        self.courses.append(course)


@dataclass
class Course:
    title: str
    credits: int


@dataclass
class Person:
    name: str


@dataclass
class Staff(Person):
    staff_type: StaffType
    diplomas: Set[str]
    department: Optional[Department] = None

    def assign_department(self, department: Department) -> None:
        self.department = department


@dataclass
class Researcher(Staff):
    publications: List[str] = field(default_factory=list)
    projects: Set[str] = field(default_factory=set)

    def publish(self, title: str) -> None:
        self.publications.append(title)

    def add_project(self, project: str) -> None:
        self.projects.add(project)


@dataclass
class Engineer(Staff):
    projects: Set[str] = field(default_factory=set)

    def add_project(self, project: str) -> None:
        self.projects.add(project)


@dataclass
class Technician(Staff):
    pass


@dataclass
class Administrative(Staff):
    pass


@dataclass
class Teacher:
    staff_member: Staff
    courses: List[Course] = field(default_factory=list)

    def assign_course(self, course: Course) -> None:
        self.courses.append(course)


class StudentTrack(str, Enum):
    TRONC_COMMUN = "tronc_commun"
    OPTION = "option"


@dataclass
class Internship:
    company: str
    topic: str
    duration_months: int


@dataclass
class Student(Person):
    track: StudentTrack
    department: Optional[Department] = None
    internships: List[Internship] = field(default_factory=list)

    def assign_department(self, department: Department) -> None:
        self.department = department

    def add_internship(self, internship: Internship) -> None:
        self.internships.append(internship)


@dataclass
class School:
    name: str
    departments: List[Department] = field(default_factory=list)
    staff: List[Staff] = field(default_factory=list)
    students: List[Student] = field(default_factory=list)
    board_members: List[Staff] = field(default_factory=list)

    def add_department(self, department: Department) -> None:
        self.departments.append(department)

    def add_staff(self, member: Staff) -> None:
        self.staff.append(member)

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def add_board_member(self, member: Staff) -> None:
        if member not in self.staff:
            self.staff.append(member)
        self.board_members.append(member)


if __name__ == "__main__":
    info_dept = Department("Informatique", "Option Informatique")
    algo = Course("Algorithmique", 6)
    po = Course("Programmation OO", 6)
    info_dept.add_course(algo)
    info_dept.add_course(po)

    school = School("Ecole des Mines d'Ales")
    school.add_department(info_dept)

    chercheur = Researcher("Dr. Martin", StaffType.CHERCHEUR, {"doctorat"})
    chercheur.assign_department(info_dept)
    chercheur.publish("Recherche sur l'IA")

    ingenieur = Engineer("Ing. Lopez", StaffType.INGENIEUR, {"diplome ingenieur"})
    ingenieur.assign_department(info_dept)
    ingenieur.add_project("Projet industriel")

    technicien = Technician("Tech. Ali", StaffType.TECHNICIEN, {"BTS"})
    technicien.assign_department(info_dept)

    admin = Administrative("Mme Durand", StaffType.ADMINISTRATIF, {"licence"})

    school.add_staff(chercheur)
    school.add_staff(ingenieur)
    school.add_staff(technicien)
    school.add_staff(admin)
    school.add_board_member(admin)

    enseignant1 = Teacher(chercheur)
    enseignant1.assign_course(algo)
    enseignant2 = Teacher(ingenieur)
    enseignant2.assign_course(po)

    etu1 = Student("Alice", StudentTrack.TRONC_COMMUN)
    etu2 = Student("Bob", StudentTrack.OPTION)
    etu2.assign_department(info_dept)
    etu2.add_internship(Internship("TechCorp", "Data", 4))

    school.add_student(etu1)
    school.add_student(etu2)

    print("Departements:", [d.name for d in school.departments])
    print("Personnel enseignant:", [t.staff_member.name for t in (enseignant1, enseignant2)])
    print("Options par departement:", {d.name: d.option_label for d in school.departments})
    print("Stages de Bob:", [(s.company, s.topic) for s in etu2.internships])
