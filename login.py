# login.py
import tkinter as tk
from tkinter import messagebox
import hashlib
import os

# Fichier de stockage des utilisateurs
USER_FILE = "users.txt"

# ============================================
# FONCTIONS DE GESTION DES UTILISATEURS
# ============================================

def hash_password(password):
    """Retourne le hash SHA-256 d'un mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Charge les utilisateurs depuis le fichier"""
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    login, pwd_hash = line.split(';', 1)
                    users[login] = pwd_hash
    return users

def save_user(login, password):
    """Enregistre un nouvel utilisateur"""
    pwd_hash = hash_password(password)
    with open(USER_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{login};{pwd_hash}\n")

def user_exists(login):
    """Vérifie si un utilisateur existe déjà"""
    users = load_users()
    return login in users

# ============================================
# FENÊTRE DE CONNEXION / INSCRIPTION
# ============================================

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("🔐 Carnet d'adresses")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        # Variable pour savoir si on est en mode connexion ou inscription
        self.is_login_mode = True

        # Titre
        self.label_title = tk.Label(
            self.root, 
            text="🔐 CONNEXION", 
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        )
        self.label_title.pack(pady=15)

        # Frame pour les champs
        self.frame = tk.Frame(self.root, bg='#f0f0f0')
        self.frame.pack(pady=10)

        # Champ Nom d'utilisateur
        tk.Label(self.frame, text="Nom d'utilisateur :", bg='#f0f0f0', font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_login = tk.Entry(self.frame, font=('Arial', 11), width=20)
        self.entry_login.grid(row=0, column=1, padx=10, pady=10)
        self.entry_login.focus()

        # Champ Mot de passe
        tk.Label(self.frame, text="Mot de passe :", bg='#f0f0f0', font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_password = tk.Entry(self.frame, font=('Arial', 11), width=20, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        # Champ Confirmation (visible seulement en mode inscription)
        self.label_confirm = tk.Label(self.frame, text="Confirmer :", bg='#f0f0f0', font=('Arial', 11))
        self.entry_confirm = tk.Entry(self.frame, font=('Arial', 11), width=20, show="*")

        # Bouton principal (Connexion / Créer)
        self.btn_main = tk.Button(
            self.root,
            text="Se connecter",
            font=('Arial', 11, 'bold'),
            bg='green', fg='white',
            command=self.submit,
            width=20
        )
        self.btn_main.pack(pady=10)

        # Bouton pour basculer entre Connexion et Inscription
        self.btn_switch = tk.Button(
            self.root,
            text="Créer un compte",
            font=('Arial', 10),
            bg='blue', fg='white',
            command=self.toggle_mode,
            width=20
        )
        self.btn_switch.pack(pady=5)

        # Lier la touche Entrée
        self.entry_password.bind('<Return>', lambda event: self.submit())

    def toggle_mode(self):
        """Bascule entre mode Connexion et mode Inscription"""
        self.is_login_mode = not self.is_login_mode

        if self.is_login_mode:
            # Mode Connexion
            self.label_title.config(text="🔐 CONNEXION")
            self.btn_main.config(text="Se connecter")
            self.btn_switch.config(text="Créer un compte")
            # Cacher le champ confirmation
            self.label_confirm.grid_remove()
            self.entry_confirm.grid_remove()
        else:
            # Mode Inscription
            self.label_title.config(text="📝 CRÉATION DE COMPTE")
            self.btn_main.config(text="Créer mon compte")
            self.btn_switch.config(text="← Retour à la connexion")
            # Afficher le champ confirmation
            self.label_confirm.grid(row=2, column=0, padx=10, pady=10, sticky='e')
            self.entry_confirm.grid(row=2, column=1, padx=10, pady=10)

    def submit(self):
        """Traite le formulaire (connexion ou inscription selon le mode)"""
        login = self.entry_login.get().strip()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        if self.is_login_mode:
            # ========== MODE CONNEXION ==========
            users = load_users()
            if login in users:
                pwd_hash = hash_password(password)
                if users[login] == pwd_hash:
                    messagebox.showinfo("Succès", f"Bienvenue {login} ")
                    self.root.destroy()
                    self.on_success(login) # Passer le nom de user comme argument
                    return
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
            self.entry_login.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_login.focus()

        else:
            # ========== MODE INSCRIPTION ==========
            confirm = self.entry_confirm.get()
            if password != confirm:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                self.entry_password.delete(0, tk.END)
                self.entry_confirm.delete(0, tk.END)
                self.entry_password.focus()
                return

            if user_exists(login):
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
                self.entry_login.delete(0, tk.END)
                self.entry_login.focus()
                return

            # Création du compte
            save_user(login, password)
            messagebox.showinfo("Succès", f"Compte '{login}' créé avec succès !\nVous pouvez maintenant vous connecter.")
            # Revenir en mode connexion
            self.toggle_mode()
            self.entry_login.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_confirm.delete(0, tk.END)
            self.entry_login.focus()