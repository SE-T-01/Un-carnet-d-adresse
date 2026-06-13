Carnet d’adresses – Gestion de contacts Allo SMS

Application de gestion de contacts (carnet d’adresses) Allo SMS développée en Python  dans le cadre d'un projet universitaire.  
Elle permet d’ajouter, supprimer, afficher et rechercher des contacts, avec persistance des données (fichier texte puis SQLite), interface graphique (Tkinter), authentification sécurisée (SHA‑256), et gestion de projet avec Jira.

---

Fonctionnalités

-  Ajouter un contact (nom, téléphone, email)
-  Supprimer un contact
-  Afficher les détails d’un contact
-  Authentification (création de compte / connexion)
-  Stockage dans un fichier texte  puis dans une base de données SQLite 
-  Interface graphique Tkinter
-   Application web Flask
-   Envoi d’emails / WhatsApp(Maroc)
-   Catégories, adresse, fonction, entreprise
-  Gestion de rendez‑vous (calendrier)

Technologies utilisées

| Technologie | Rôle |
|-------------|------|
| Python  | Langage principal |
| Tkinter | Interface graphique |
| SQLite | Base de données |
| hashlib | Hachage des mots de passe (SHA‑256) |
| Flask | Application web |

Configuration et installation:
-Python 3.8 ou supérieur
- Compte Gmail avec **vérification en deux étapes activée** et **mot de passe d'application** généré
- Navigateur web (Chrome recommandé)
Créer un environnement virtuel
  -Installer Flask : pip install flask
  -Déplacer dans votre dossier avec invite command :
  -Créer un environnement : python -m venv Nom_environment
  -Activer l'environnement :Nom_environment\Scripts\activate
 Installer les dépendances
  -Installer  La bibliothèque pywhatkit afin d' utiliser  WhatsApp : pip install pywhatkit
 Configuration de l’envoi d’emails (Gmail):
 Dans le fichier app.py, remplacez les lignes suivantes :
        EMAIL_EXPEDITEUR = "votre_email@gmail.com"
        EMAIL_MOT_DE_PASSE = "votre_mot_de_passe_application"
    Par :
        EMAIL_EXPEDITEUR : votre adresse Gmail valide.
        EMAIL_MOT_DE_PASSE : mot de passe d’application (et non votre mot de passe habituel).
    Pour générer un mot de passe d’application : https://myaccount.google.com/apppasswords

Lancer l’application:
  Exécuter python app.py



