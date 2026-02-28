import os
from fpdf import FPDF
from datetime import datetime

# Créer le dossier
os.makedirs("data/raw", exist_ok=True)

class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            self.set_font("helvetica", "B", 12)
            self.cell(0, 10, "Reglement Officiel - UniHelp University", align="C")
            self.ln(5)
            self.line(10, 20, 200, 20)
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 9)
        self.cell(0, 10, f"Page {self.page_no()} | Document officiel UniHelp - {datetime.now().year}", align="C")

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 14)
        self.set_fill_color(230, 230, 250)
        self.cell(0, 10, title, ln=True, fill=True)
        self.ln(5)

    def chapter_body(self, text):
        self.set_font("helvetica", "", 12)
        self.multi_cell(0, 8, text)
        self.ln()

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

# ==========================
# PAGE DE COUVERTURE
# ==========================
pdf.add_page()
pdf.set_font("helvetica", "B", 22)
pdf.cell(0, 20, "REGLEMENT OFFICIEL", ln=True, align="C")
pdf.set_font("helvetica", "", 18)
pdf.cell(0, 15, "Scolarite & Procedures Administratives", ln=True, align="C")
pdf.ln(20)
pdf.set_font("helvetica", "I", 12)
pdf.cell(0, 10, f"Edition {datetime.now().year}", ln=True, align="C")
pdf.ln(30)
pdf.set_font("helvetica", "", 12)
pdf.multi_cell(0, 8,
    "Ce document definit les regles officielles applicables aux etudiants inscrits "
    "a UniHelp University. Toute inscription implique l'acceptation integrale "
    "du present reglement."
)

# ==========================
# TABLE DES MATIERES
# ==========================
pdf.add_page()
pdf.chapter_title("TABLE DES MATIERES")

toc = """
1. Absences et Justificatifs
2. Bourses et Aides Financieres
3. Stages et Conventions
4. Examens et Rattrapages
5. Paiement des Frais de Scolarite
6. Discipline et Sanctions
7. Vie Etudiante
8. Dispositions Finales
"""
pdf.chapter_body(toc)

# ==========================
# CONTENU DETAILLE
# ==========================

pdf.add_page()
pdf.chapter_title("1. ABSENCES ET JUSTIFICATIFS")

pdf.chapter_body("""
Toute absence a un TP, TD ou examen doit etre justifiee dans un delai de 48 heures ouvrées.
Les justificatifs acceptes sont :
- Certificat medical avec cachet officiel
- Convocation administrative ou judiciaire
- Certificat de deces d'un proche au 1er degre

Un retard superieur a 15 minutes est considere comme une absence.
Au-dela de 3 absences injustifiees dans un module, l'etudiant peut etre exclu de l'examen final.
""")

pdf.chapter_title("2. BOURSES ET AIDES FINANCIERES")

pdf.chapter_body("""
Les bourses au merite sont attribuees selon les criteres suivants :
- Moyenne generale >= 14/20
- Aucune absence injustifiee
- Comportement disciplinaire irreprochable

Versement le 5 de chaque mois.
Montants :
- Excellence (>=16/20) : 800 DT/mois
- Merite (14-15.99) : 500 DT/mois

Les aides sociales peuvent etre accordees apres etude du dossier par la commission.
""")

pdf.chapter_title("3. STAGES ET CONVENTIONS")

pdf.chapter_body("""
La convention doit etre signee avant le debut du stage par :
- L'entreprise
- L'etudiant
- L'administration

Duree minimale : 8 semaines consecutives.
Un rapport detaille doit etre remis 2 semaines apres la fin du stage.
Une soutenance devant jury est obligatoire.
""")

pdf.chapter_title("4. EXAMENS ET RATTRAPAGES")

pdf.chapter_body("""
Note eliminatoire : 08/20.
Compensation possible si moyenne generale > 10/20.

Fraude = exclusion immediate + passage en commission disciplinaire.

La session de rattrapage est organisee dans un delai de 4 semaines apres la session principale.
""")

pdf.chapter_title("5. PAIEMENT DES FRAIS")

pdf.chapter_body("""
Date limite : 30 septembre.
Paiement en 3 fois possible sur demande avant le 15 septembre.

Retard > 30 jours :
- Suspension acces plateforme
- Blocage resultats
""")

pdf.chapter_title("6. DISCIPLINE ET SANCTIONS")

pdf.chapter_body("""
Sont interdits :
- Plagiat
- Violence verbale ou physique
- Degradation du materiel

Sanctions possibles :
- Avertissement ecrit
- Blame
- Exclusion temporaire
- Exclusion definitive
""")

pdf.chapter_title("7. VIE ETUDIANTE")

pdf.chapter_body("""
Les associations doivent etre declarees.
Les evenements doivent etre autorises par l'administration.

Les etudiants ont acces :
- Bibliotheque (8h-20h)
- Laboratoires informatiques
- Plateforme e-learning
""")

pdf.chapter_title("8. DISPOSITIONS FINALES")

pdf.chapter_body("""
Le present reglement entre en vigueur a compter de sa publication.
Il peut etre modifie par decision du conseil universitaire.

Fait a Tunis.
""")

pdf.ln(20)
pdf.set_font("helvetica", "I", 11)
pdf.cell(0, 10, "Signature du Directeur Pedagogique", ln=True)
pdf.cell(0, 10, "______________________________", ln=True)

# ==========================
# EXPORT
# ==========================
output_path = "data/raw/reglement_officiel_premium.pdf"
pdf.output(output_path)

print(f"PDF premium généré avec succès dans : {output_path}")