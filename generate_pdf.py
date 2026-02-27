import os
from fpdf import FPDF

# S'assurer que le dossier existe
os.makedirs("data/raw", exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "Reglement de Scolarite et Procedures - UniHelp", align="C")
        self.ln(20)

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", "", 12)

content = """
1. ABSENCES ET JUSTIFICATIFS
Toute absence a un Travail Pratique (TP) ou a un examen doit etre justifiee dans les 48 heures ouvrees au secretariat pedagogique par email. Les seuls justificatifs acceptes sont : certificat medical, convocation officielle (justice, permis de conduire), ou certificat de deces d'un proche. Un retard de plus de 15 minutes est considere comme une absence.

2. BOURSES ET AIDES FINANCIERES
Les bourses au merite sont versees le 5 de chaque mois. Pour etre eligible a la bourse au merite, l'etudiant doit avoir valide son semestre precedent avec une moyenne generale superieure ou egale a 14/20 et n'avoir aucune absence injustifiee.

3. STAGES ET CONVENTIONS
La convention de stage doit etre signee par l'entreprise, l'etudiant, et l'universite avant le debut effectif du stage. Aucun stage ne peut etre antidate. La duree minimale d'un stage validant pour le diplome est de 8 semaines consecutives.

4. EXAMENS ET RATTRAPAGES
La note eliminatoire a un module est de 08/20. Si un etudiant obtient une note inferieure, il est automatiquement convoque a la session de rattrapage, sauf si sa moyenne generale compense cette note (moyenne > 10/20).

5. PAIEMENT DES FRAIS DE SCOLARITE
Les frais de scolarite doivent etre regles au plus tard le 30 septembre de l'annee en cours. Des facilites de paiement en 3 fois sans frais peuvent etre accordees sur demande aupres du service comptabilite avant le 15 septembre.
"""

# fpdf2 gère automatiquement le word wrap avec multi_cell
pdf.multi_cell(0, 10, content)

output_path = "data/raw/reglement_officiel.pdf"
pdf.output(output_path)
print(f"PDF généré avec succès dans : {output_path}")
