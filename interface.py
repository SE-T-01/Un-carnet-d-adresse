import tkinter as tk
from tkinter import messagebox
from contact import Contact
from AddressBook import AddressBook

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Gestion des contacts")
        self.root.geometry("650x600")
        self.root.resizable(True, True)

        # Carnet d'adresses
        self.carnet = AddressBook("Mescontacts.txt")

        # Création de l'interface
        self.create_widgets()

        # Chargement initial des contacts
        self.refresh_listbox()

    def create_widgets(self):
        # ==================== FRAME SUPÉRIEURE (TITRE) ====================
        self.frame_top = tk.Frame(self.root, bg='lightblue', height=80)
        self.frame_top.pack(fill='x', pady=(0, 10))

        self.label_titre = tk.Label(
            self.frame_top,
            text="📒 GESTION DES CONTACTS",
            font=('Arial', 20, 'bold'),
            bg='lightblue'
        )
        self.label_titre.pack(pady=20)

        # ==================== FRAME DES DÉTAILS ====================
        self.frame_details = tk.Frame(self.root, bg='lightyellow', height=100, relief='sunken', bd=1)
        self.frame_details.pack(fill='x', padx=10, pady=5)

        self.label_details = tk.Label(
            self.frame_details,
            text="Sélectionnez un contact pour voir ses détails",
            font=('Arial', 11),
            bg='lightyellow',
            anchor='w',
            justify='left'
        )
        self.label_details.pack(fill='both', expand=True, padx=10, pady=10)

        # ==================== FRAME MÉDIANE (LISTE DES CONTACTS) ====================
        self.frame_list = tk.Frame(self.root)
        self.frame_list.pack(fill='both', expand=True, padx=10, pady=5)

        self.label_list = tk.Label(
            self.frame_list,
            text="Contacts (par ordre alphabétique) :",
            font=('Arial', 12)
        )
        self.label_list.pack(anchor='w')

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.pack(side='right', fill='y')

        # Listbox
        self.listbox = tk.Listbox(
            self.frame_list,
            font=('Arial', 11),
            yscrollcommand=self.scrollbar.set
        )
        self.listbox.pack(fill='both', expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Événements
        self.listbox.bind('<Double-Button-1>', self.supprimer_contact)
        self.listbox.bind('<<ListboxSelect>>', self.on_select_contact)

        # ==================== FRAME INFÉRIEURE (BOUTONS) ====================
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(fill='x', padx=10, pady=10)

        # Bouton Ajouter
        self.btn_ajouter = tk.Button(
            self.frame_buttons,
            text="➕ Ajouter",
            font=('Arial', 11),
            bg='green', fg='white',
            command=self.ajouter_contact
        )
        self.btn_ajouter.pack(side='left', padx=5, fill='x', expand=True)

        # Bouton Supprimer
        self.btn_supprimer = tk.Button(
            self.frame_buttons,
            text="➖ Supprimer",
            font=('Arial', 11),
            bg='red', fg='white',
            command=self.supprimer_selection
        )
        self.btn_supprimer.pack(side='left', padx=5, fill='x', expand=True)

        # Bouton Afficher Détails
        self.btn_afficher = tk.Button(
            self.frame_buttons,
            text="🔍 Afficher Détails",
            font=('Arial', 11),
            bg='orange', fg='white',
            command=self.afficher_details
        )
        self.btn_afficher.pack(side='left', padx=5, fill='x', expand=True)

        # Bouton Rafraîchir
        self.btn_rafraichir = tk.Button(
            self.frame_buttons,
            text="🔄 Rafraîchir",
            font=('Arial', 11),
            bg='blue', fg='white',
            command=self.refresh_listbox
        )
        self.btn_rafraichir.pack(side='left', padx=5, fill='x', expand=True)
        #Bouton Quitter 
        self.btn_quitter = tk.Button(
            self.frame_buttons,
            text="🚪 Quitter",
            font=('Arial', 11),
            bg='gray', fg='white',
            command=self.fermer_application   # ← appelle une méthode
        )
        self.btn_quitter.pack(side='left', padx=5, fill='x', expand=True)

    # ==================== MÉTHODES ====================

    def ajouter_contact(self):
        """Ouvre une fenêtre pour saisir un nouveau contact"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Ajouter un contact")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Nom :", font=('Arial', 11)).pack(pady=5)
        entry_nom = tk.Entry(dialog, font=('Arial', 11), width=30)
        entry_nom.pack(pady=5)

        tk.Label(dialog, text="Téléphone :", font=('Arial', 11)).pack(pady=5)
        entry_tel = tk.Entry(dialog, font=('Arial', 11), width=30)
        entry_tel.pack(pady=5)

        tk.Label(dialog, text="Email :", font=('Arial', 11)).pack(pady=5)
        entry_email = tk.Entry(dialog, font=('Arial', 11), width=30)
        entry_email.pack(pady=5)

        def enregistrer():
            nom = entry_nom.get().strip()
            tel = entry_tel.get().strip()
            email = entry_email.get().strip()

            if not nom or not tel or not email:
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires !")
                return

            try:
                nouveau = Contact(nom, tel, email)
                ajout_reussi = self.carnet.AddContact(nouveau)

                if ajout_reussi:
                    dialog.destroy()
                    self.refresh_listbox()
                    messagebox.showinfo("Succès", f"Contact '{nom}' ajouté avec succès !")
                else:
                    messagebox.showerror("Erreur", f"Le contact '{nom}' existe déjà !")
            except AssertionError as e:
                messagebox.showerror("Erreur de validation", str(e))

        btn_enregistrer = tk.Button(
            dialog,
            text="💾 Enregistrer",
            bg='green', fg='white',
            command=enregistrer
        )
        btn_enregistrer.pack(pady=20)

    def supprimer_selection(self):
        """Supprime le contact sélectionné dans la Listbox"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un contact à supprimer.")
            return

        nom = self.listbox.get(selection[0])

        reponse = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer '{nom}' ?")
        if reponse:
            self.carnet.RemoveContact(nom)
            self.refresh_listbox()

    def supprimer_contact(self, event):
        self.supprimer_selection()

    def refresh_listbox(self):
        """Rafraîchit la liste des contacts"""
        self.listbox.delete(0, tk.END)
        contacts_tries = sorted(self.carnet.book, key=lambda c: c.nom.lower())
        for contact in contacts_tries:
            self.listbox.insert(tk.END, contact.nom)
        if not contacts_tries:
            self.listbox.insert(tk.END, "📭 Aucun contact.")

    def afficher_details(self):
        """Affiche les détails du contact sélectionné"""
        selection = self.listbox.curselection()
        if not selection:
            self.label_details.config(text="⚠️ Veuillez sélectionner un contact.")
            return

        nom = self.listbox.get(selection[0])
        contact = self.carnet.desplayContact(nom)

        if contact:
            self.label_details.config(
                text=f"📇 Nom : {contact.nom}\n"
                     f"📞 Téléphone : {contact.num_tel}\n"
                     f"✉️ Email : {contact.email}"
            )
        else:
            self.label_details.config(text=f"❌ Contact '{nom}' non trouvé.")

    def on_select_contact(self, event):
        self.afficher_details()
    def fermer_application(self):
        """Ferme proprement l'application"""
        self.root.destroy()


# ==================== LANCEMENT DE L'APPLICATION ====================
"""
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
"""