import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import tempfile
import shutil
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'inventory.txt')

def adauga_produs():
    categorie = categorie_entry.get()
    produs = produs_entry.get()
    if not categorie or not produs:
        messagebox.showerror("Eroare", "Categoria și numele produsului sunt obligatorii.")
        return

    with open(file_path, 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        if not lines or lines[-1].strip() == '':
            cod = "ITEM001" 
        else:
            last_line = lines[-1].strip()
            last_code = last_line.split(',')[0]
            last_num = int(last_code[4:])
            next_num = last_num + 1
            cod = f"ITEM{next_num:03d}"
        
        file.write(f"{cod},{categorie},{produs},1\n")
        lista_produse.insert(tk.END, f"{cod} - {categorie} - {produs} - Stoc: 1")  
        messagebox.showinfo("Succes", f"Produsul {produs} a fost adăugat cu succes cu codul {cod}")


def gestioneaza_stoc():
    cod = cod_entry.get()
    cantitate_adaugata = int(cantitate_entry.get())
    if cantitate_adaugata <= 0:
        with open(file_path, 'r') as file, tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            lines = file.readlines()
            found = False
            for line in lines:
                if line.startswith(f"{cod},"):
                    found = True
                else:
                    temp_file.write(line)
            if not found:
                messagebox.showerror("Eroare", "Produsul nu a fost găsit.")
                return
        shutil.move(temp_file.name, file_path)
        messagebox.showinfo("Succes", "Produsul a fost eliminat din inventar.")
    else:
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for i, line in enumerate(lines):
                if line.startswith(f"{cod},"):
                    parts = line.strip().split(',')
                    cantitate_noua = cantitate_adaugata
                    lines[i] = f"{cod},{parts[1]},{parts[2]},{cantitate_noua}\n"
                    file.seek(0)
                    file.writelines(lines)
                    messagebox.showinfo("Succes", "Stocul a fost actualizat.")
                    break
            else:
                messagebox.showerror("Eroare", "Produsul nu a fost găsit.")
                return

    refresh_list()


def refresh_list():
    lista_produse.delete(0, tk.END)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    cod, categorie, produs, stoc = line.strip().split(',')
                    lista_produse.insert(tk.END, f"{cod} - {categorie} - {produs} - Stoc: {stoc}")
                except ValueError:
                    continue  
    except FileNotFoundError:
        messagebox.showerror("Eroare", "Fișierul de inventar nu a fost găsit.")

        
def register():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Eroare", "Numele de utilizator și parola sunt obligatorii.")
        return
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    messagebox.showinfo("Succes", "Utilizatorul a fost înregistrat cu succes.")
    register_window.destroy()

def login():
    global root
    global login_window
    
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Eroare", "Numele de utilizator și parola sunt obligatorii.")
        return
    
    with open('users.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                messagebox.showinfo("Succes", "Autentificare reușită.")
                if login_window:  
                    login_window.destroy()  
                main_menu()  
                return
        messagebox.showerror("Eroare", "Numele de utilizator sau parola incorecte.")

def main_menu():
  
    root = tk.Tk()
    root.title("Gestionare Inventar")

    
    adauga_frame = ttk.LabelFrame(root, text="Adăugare Produs")
    adauga_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    ttk.Label(adauga_frame, text="Categorie:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    global categorie_entry
    categorie_entry = ttk.Entry(adauga_frame)
    categorie_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(adauga_frame, text="Produs:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    global produs_entry
    produs_entry = ttk.Entry(adauga_frame)
    produs_entry.grid(row=1, column=1, padx=5, pady=5)

    adauga_button = ttk.Button(adauga_frame, text="Adaugă Produs", command=adauga_produs)
    adauga_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    gestioneaza_frame = ttk.LabelFrame(root, text="Gestionare Stoc")
    gestioneaza_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")

    ttk.Label(gestioneaza_frame, text="Cod Produs:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    global cod_entry
    cod_entry = ttk.Entry(gestioneaza_frame)
    cod_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(gestioneaza_frame, text="Cantitate:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    global cantitate_entry
    cantitate_entry = ttk.Entry(gestioneaza_frame)
    cantitate_entry.grid(row=1, column=1, padx=5, pady=5)

    gestioneaza_button = ttk.Button(gestioneaza_frame, text="Modifica Stoc", command=gestioneaza_stoc)
    gestioneaza_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    
    global lista_produse
    lista_produse = tk.Listbox(root, width=50)
    lista_produse.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    refresh_list()

    root.mainloop()

def show_register_window():
    global register_window
    register_window = tk.Toplevel()
    register_window.title("Înregistrare")

    ttk.Label(register_window, text="Nume utilizator:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    global username_entry
    username_entry = ttk.Entry(register_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(register_window, text="Parola:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    global password_entry
    password_entry = ttk.Entry(register_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    register_button = ttk.Button(register_window, text="Înregistrare", command=register)
    register_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

def show_login_window():
    global login_window
    login_window = tk.Toplevel()
    login_window.title("Autentificare")

    ttk.Label(login_window, text="Nume utilizator:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    global username_entry
    username_entry = ttk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(login_window, text="Parola:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    global password_entry
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = ttk.Button(login_window, text="Autentificare", command=login)
    login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

root = tk.Tk()
root.title("Autentificare")

register_button = ttk.Button(root, text="Înregistrare", command=show_register_window)
register_button.grid(row=0, column=0, padx=5, pady=5)

login_button = ttk.Button(root, text="Autentificare", command=show_login_window)
login_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
