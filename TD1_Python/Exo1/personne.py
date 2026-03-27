from __future__ import annotations

from typing import Optional


class Personne:
    """Represente une personne et son etat civil."""

    def __init__(
        self,
        civilite: str,
        nom: str,
        prenom: str,
        annee_naissance: int,
        statut: str = "celibataire",
    ) -> None:
        self.civilite = civilite.strip()
        self.nom_jeune_fille = nom.strip()
        self.nom_usage = nom.strip()
        self.prenom = prenom.strip()
        self.annee_naissance = annee_naissance
        self.statut = statut.strip().lower()
        self.conjoint: Optional[Personne] = None

    def age(self, annee_reference: int) -> int:
        return annee_reference - self.annee_naissance

    def est_femme(self) -> bool:
        return self.civilite.lower().startswith("m") and "mme" in self.civilite.lower() or "mlle" in self.civilite.lower()

    def marier(self, autre: Personne) -> None:
        if autre is self:
            raise ValueError("Impossible de se marier avec soi-meme.")
        if self.conjoint is not None or autre.conjoint is not None:
            raise ValueError("Polygamie interdite : l'un des deux est deja marie.")
        self.conjoint = autre
        autre.conjoint = self
        self.statut = "marie"
        autre.statut = "marie"
        if self.est_femme():
            self.civilite = "Mme"
            self.nom_usage = f"{self.nom_jeune_fille} Epouse {autre.nom_usage}"
        if autre.est_femme():
            autre.civilite = "Mme"
            autre.nom_usage = f"{autre.nom_jeune_fille} Epouse {self.nom_usage}"

    def retourne_infos(self) -> str:
        pronoms = {"f": ("elle", "nee"), "m": ("il", "ne")}
        genre = "f" if self.est_femme() else "m"
        pronom, participe = pronoms[genre]
        etat = self.statut if self.conjoint is None else "marie"
        return f"{self.civilite} {self.nom_usage} {self.prenom} est {participe} en {self.annee_naissance}, {pronom} est {etat}."

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"Personne({self.civilite} {self.nom_usage} {self.prenom})"


if __name__ == "__main__":
    pierre = Personne("M.", "Holly", "Pierre", 1965)
    alice = Personne("Mlle", "Durant", "Alice", 1990)
    marc = Personne("M.", "Dupond", "Marc", 1988)

    alice.marier(marc)

    personnes = [pierre, alice, marc]
    for personne in personnes:
        print(personne.retourne_infos())
        print(f"Age en 2026 : {personne.age(2026)} ans")
