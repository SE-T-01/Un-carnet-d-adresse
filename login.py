# login.py Version 2.0.0
import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3

DB_NAME = "contacts.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_users_table():
    """Crée la table users si elle n'existe pas"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def user_exists(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_user(username, password):
    pwd_hash = hash_password(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pwd_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False

# ============================================
# FENÊTRE DE CONNEXION / INSCRIPTION (Tkinter)
# ============================================

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("🔐 Carnet d'adresses")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        self.is_login_mode = True

        # Initialiser la table users au démarrage
        init_users_table()

        # Titre
        self.label_title = tk.Label(self.root, text="🔐 CONNEXION", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self.label_title.pack(pady=15)

        self.frame = tk.Frame(self.root, bg='#f0f0f0')
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Nom d'utilisateur :", bg='#f0f0f0', font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_login = tk.Entry(self.frame, font=('Arial', 11), width=20)
        self.entry_login.grid(row=0, column=1, padx=10, pady=10)
        self.entry_login.focus()

        tk.Label(self.frame, text="Mot de passe :", bg='#f0f0f0', font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_password = tk.Entry(self.frame, font=('Arial', 11), width=20, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.label_confirm = tk.Label(self.frame, text="Confirmer :", bg='#f0f0f0', font=('Arial', 11))
        self.entry_confirm = tk.Entry(self.frame, font=('Arial', 11), width=20, show="*")

        self.btn_main = tk.Button(self.root, text="Se connecter", font=('Arial', 11, 'bold'), bg='green', fg='white', command=self.submit, width=20)
        self.btn_main.pack(pady=10)

        self.btn_switch = tk.Button(self.root, text="Créer un compte", font=('Arial', 10), bg='blue', fg='white', command=self.toggle_mode, width=20)
        self.btn_switch.pack(pady=5)

        self.entry_password.bind('<Return>', lambda event: self.submit())

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.label_title.config(text="🔐 CONNEXION")
            self.btn_main.config(text="Se connecter")
            self.btn_switch.config(text="Créer un compte")
            self.label_confirm.grid_remove()
            self.entry_confirm.grid_remove()
        else:
            self.label_title.config(text="📝 CRÉATION DE COMPTE")
            self.btn_main.config(text="Créer mon compte")
            self.btn_switch.config(text="← Retour à la connexion")
            self.label_confirm.grid(row=2, column=0, padx=10, pady=10, sticky='e')
            self.entry_confirm.grid(row=2, column=1, padx=10, pady=10)

    def submit(self):
        login = self.entry_login.get().strip()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        if self.is_login_mode:
            if authenticate_user(login, password):
                messagebox.showinfo("Succès", f"Bienvenue {login} !")
                self.root.destroy()
                self.on_success(login)
                return
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
            self.entry_login.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_login.focus()
        else:
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
            if save_user(login, password):
                messagebox.showinfo("Succès", f"Compte '{login}' créé avec succès !")
                self.toggle_mode()
                self.entry_login.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.entry_confirm.delete(0, tk.END)
                self.entry_login.focus()