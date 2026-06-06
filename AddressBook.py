# Version 1.0.0
"""
class AddressBook:
    def __init__(self):
        self.book=[]
    def AddContact(self,Cont):
        self.book.append(Cont)
    def RemoveContact(self,name):
        if len(self.book)==0:
            print("Le répértoire est vide")
        else:
            for i, contact in enumerate(self.book):
                if contact.nom.lower() == name.lower():
                    del self.book[i]
                    print(f"Contact '{name}' supprimé avec succès.")
                else :
                    print("Contact inexsiste")         
    def desplayContact(self,name):
         if len(self.book)==0:
            print("Le répértoire est vide")
         else:
            for contact in self.book:
                if contact.nom==name:
                    print(contact)
                else:
                     print("Contact inexsiste")
"""
#V 3.0 (DB)
import sqlite3
from contact import Contact

class AddressBook:
    def __init__(self, db_file="contacts.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.create_table()
        self.book = []  # Optionnel : garder une copie en mémoire (ou tout gérer via SQL)
        self.load_contacts_to_memory()  # Si vous voulez garder self.book

    def create_table(self):
        """Crée la table contacts si elle n'existe pas"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE,
                num_tel TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def load_contacts_to_memory(self):
        """Charge tous les contacts dans self.book (optionnel mais pratique pour l'interface)"""
        self.book = self.get_all_contacts()

    def get_all_contacts(self):
        """Retourne la liste de tous les contacts (objets Contact)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nom, num_tel, email FROM contacts ORDER BY nom COLLATE NOCASE")
        rows = cursor.fetchall()
        return [Contact(row[0], row[1], row[2]) for row in rows]

    def AddContact(self, contact):
        """Ajoute un contact à la base de données (vérifie les doublons via UNIQUE)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO contacts (nom, num_tel, email) VALUES (?, ?, ?)",
                (contact.nom, contact.num_tel, contact.email)
            )
            self.conn.commit()
            self.book = self.get_all_contacts()  # Mise à jour mémoire
            print(f"Contact '{contact.nom}' ajouté avec succès.")
            return True
        except sqlite3.IntegrityError:
            print(f" Le contact '{contact.nom}' existe déjà.")
            return False

    def RemoveContact(self, name):
        """Supprime un contact par son nom (insensible à la casse)"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE LOWER(nom) = LOWER(?)", (name,))
        self.conn.commit()
        if cursor.rowcount > 0:
            self.book = self.get_all_contacts()
            print(f" Contact '{name}' supprimé avec succès.")
            return True
        else:
            print(f"Contact '{name}' non trouvé.")
            return False

    def displayContact(self, name):
        """Retourne le contact correspondant au nom (insensible à la casse)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nom, num_tel, email FROM contacts WHERE LOWER(nom) = LOWER(?)", (name,))
        row = cursor.fetchone()
        if row:
            return Contact(row[0], row[1], row[2])
        return None

    def export_to_csv(self, csv_file="contacts_export.csv"):
        """Exporte tous les contacts dans un fichier CSV"""
        import csv
        contacts = self.get_all_contacts()
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["nom", "num_tel", "email"])
            for contact in contacts:
                writer.writerow([contact.nom, contact.num_tel, contact.email])
        print(f" {len(contacts)} contacts exportés vers {csv_file}")

    def close(self):
        """Ferme la connexion à la base de données (appeler à la fermeture de l'app)"""
        self.conn.close()