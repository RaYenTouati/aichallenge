# Hackathon Pitch : UniHelp (2 minutes)

## Accroche (20 secondes)
"Bonjour à tous. Chaque jour, les secrétariats de notre université reçoivent des centaines de questions répétitives : 'Comment justifier mon absence ?', 'Quand est le versement des bourses ?'. Résultat : des étudiants stressés par les délais, et un personnel administratif au bord du burn-out. 
C'est pour cela que nous avons créé **UniHelp**."

## La Solution (40 secondes)
"UniHelp est un assistant IA souverain, conçu pour épauler les secrétariats. Contrairement à un ChatGPT public qui peut inventer des règles, UniHelp utilise la technologie **RAG (Retrieval-Augmented Generation)**. 
Il se base **exclusivement** sur la documentation interne de l'université (règlements, FAQ, notes de service). Si la réponse n'est pas dans les documents, il refuse de répondre pour éviter toute désinformation. De plus, pour chaque réponse, il affiche la source exacte et un score de pertinence, assurant une parfaite traçabilité."

## Démonstration (40 secondes)
*"Laissez-moi vous montrer."*
1. **Scénario 1 : L'information existe**
   - L'étudiant demande : "Quelles sont les conditions pour obtenir une bourse au mérite ?"
   - *L'IA répond avec précision et affiche "Source : reglement_bourses_2024.pdf, Pertinence : 88%".*
2. **Scénario 2 : L'information n'existe pas (Anti-Hallucination)**
   - L'étudiant tente de piéger le système : "Est-ce que l'université rembourse les abonnements Spotify ?"
   - *L'IA bloque et répond : "Désolé, je n'ai trouvé aucune information à ce sujet dans les documents officiels. Veuillez contacter le secrétariat."*
3. **Scénario 3 : Action administrative (Génération d'email)**
   - L'étudiant doit faire une démarche. Au lieu de chercher comment écrire, il clique sur "Générer un email type".
   - *L'IA lui fournit un email formel pré-rempli, respectant les procédures de l'école.*

## Conclusion (20 secondes)
"En 24 heures, nous avons construit un pipeline backend en Python, sécurisé, testable, et déployable sans nécessiter de coûteux serveurs dans le cloud, grâce à notre base vectorielle FAISS locale. UniHelp n'est pas juste un gadget de plus, c'est un gain de temps massif et immédiat pour l'administration et une meilleure expérience pour les étudiants. Merci !"
