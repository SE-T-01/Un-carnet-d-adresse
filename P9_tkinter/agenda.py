import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AgendaRDV:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des RDV - Cabinet Médical")
        self.root.geometry("580x520")
        self.root.config(bg="#f8fafc")
        
        # Initialisation de la table SQL
        self.init_table_rdv()
        
        # Intervalles de 30 minutes (08h00 à 17h30)
        self.creneaux = [
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"
        ]
        
        # Zone de sélection supérieure
        frame_top = tk.Frame(self.root, bg="#1e293b", pady=15, padx=15)
        frame_top.pack(fill="x")
        
        # Saisie de la date
        tk.Label(frame_top, text="Date (AAAA-MM-JJ) :", fg="white", bg="#1e293b", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_date = tk.Entry(frame_top, font=("Arial", 10), width=12)
        self.entry_date.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.entry_date.grid(row=0, column=1, padx=10, pady=5)
        
        # Bouton de rafraîchissement
        btn_refresh = tk.Button(frame_top, text="📅 Charger la date", command=self.refresh_agenda, bg="#4f46e5", fg="white", font=("Arial", 9, "bold"), bd=0, padx=10, pady=2, cursor="hand2")
        btn_refresh.grid(row=0, column=2, padx=5)

        # Liste déroulante des patients
        tk.Label(frame_top, text="Sélectionner Patient :", fg="white", bg="#1e293b", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.combo_patient = ttk.Combobox(frame_top, font=("Arial", 10), state="readonly", width=30)
        self.combo_patient.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Grille d'affichage des créneaux
        self.frame_grid = tk.Frame(self.root, bg="#f8fafc", pady=20)
        self.frame_grid.pack(fill="both", expand=True)
        
        # Chargement initial
        self.load_patients()
        self.refresh_agenda()

    def init_table_rdv(self):
        """Crée la table des rendez-vous si elle n'existe pas."""
        conn = sqlite3.connect('contacts.db')
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rdv (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                date_rdv TEXT,
                heure_rdv TEXT,
                FOREIGN KEY(patient_id) REFERENCES contacts(id)
            )
        """)
        conn.commit()
        conn.close()

    def load_patients(self):
        """Récupère les contacts de catégorie 'Patient' pour la liste déroulante."""
        conn = sqlite3.connect('contacts.db')
        cursor = conn.execute("SELECT id, nom, prenom FROM contacts WHERE categorie='Patient'")
        self.patients = cursor.fetchall()
        conn.close()
        
        liste_affichage = [f"{p[1].upper()} {p[2]} (ID: {p[0]})" for p in self.patients]
        self.combo_patient['values'] = liste_affichage
        if liste_affichage:
            self.combo_patient.current(0)

    def refresh_agenda(self):
        """Met à jour les boutons en vérifiant les réservations dans la base SQL."""
        date_choisie = self.entry_date.get().strip()
        
        # Nettoyage de l'ancienne grille
        for widget in self.frame_grid.winfo_children():
            widget.destroy()
        
        # Récupération des rendez-vous bloqués
        conn = sqlite3.connect('contacts.db')
        cursor = conn.execute("SELECT heure_rdv FROM rdv WHERE date_rdv = ?", (date_choisie,))
        rdv_reserves = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Construction de la grille (4 colonnes)
        for index, heure in enumerate(self.creneaux):
            row = index // 4
            col = index % 4
            
            if heure in rdv_reserves:
                # Case occupée : Bouton rouge et désactivé
                btn = tk.Button(self.frame_grid, text=f"{heure}\n[Occupé]", bg="#ef4444", fg="white", state="disabled", font=("Arial", 10, "bold"), width=12, height=2, bd=1)
            else:
                # Case libre : Bouton vert et actif
                btn = tk.Button(self.frame_grid, text=f"{heure}\nLibre", bg="#10b981", fg="white", font=("Arial", 10, "bold"), width=12, height=2, bd=1, cursor="hand2",
                                command=lambda h=heure: self.reserver_creneau(h))
            
            btn.grid(row=row, column=col, padx=12, pady=12)

    def reserver_creneau(self, heure):
        """Enregistre le rendez-vous et désactive la case."""
        date_choisie = self.entry_date.get().strip()
        selection_patient = self.combo_patient.get()
        
        if not selection_patient:
            messagebox.showerror("Erreur", "Veuillez d'abord enregistrer un patient dans l'application Web.")
            return
            
        # Extraction de l'ID du patient
        patient_id = int(selection_patient.split("ID: ")[1].replace(")", ""))
            
        # Écriture dans la base SQLite
        conn = sqlite3.connect('contacts.db')
        conn.execute("INSERT INTO rdv (patient_id, date_rdv, heure_rdv) VALUES (?, ?, ?)", (patient_id, date_choisie, heure))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Succès", f"Créneau de {heure} réservé avec succès !")
        self.refresh_agenda()

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaRDV(root)
    root.mainloop()
