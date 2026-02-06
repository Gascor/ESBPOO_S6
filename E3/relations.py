from __future__ import annotations

RELATIONS = {
    1: "aggregation",
    2: "lien",  # utilisation ponctuelle
    3: "generalisation",
    4: "aggregation",
    5: "lien",
    6: "instanciation",
    7: "aggregation",
    8: "instanciation",
}

EXPLANATIONS = {
    1: "Un pays inclut sa capitale (relation tout/partie).",
    2: "Le philosophe utilise un outil (dependance simple).",
    3: "Les postes de jeu specialisent le joueur de rugby.",
    4: "L'equipe est composee d'un nombre fixe de joueurs par poste.",
    5: "Dede interagit avec des objets (PC, langage).",
    6: "Java, C++ et Eiffel sont des instances de la categorie langage OO.",
    7: "Les etages et boulons font partie de la tour (composition).",
    8: "L'agregation est un cas particulier d'examen.",
}


def main() -> None:
    for numero in sorted(RELATIONS):
        relation = RELATIONS[numero]
        detail = EXPLANATIONS[numero]
        print(f"{numero}) {relation} - {detail}")


if __name__ == "__main__":
    main()
