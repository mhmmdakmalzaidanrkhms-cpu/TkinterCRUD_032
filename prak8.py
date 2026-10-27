import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_NAME = "nilai_siswa.db"

BG = "#282a36"
BTN_BG = "#44475a"
BTN_HOVER = "#50fa7b"
TITLE_COLOR = "#ff79c6"


# ---------------------------------------------------------------- Database
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def simpan_ke_db(nama, bio, fis, ing, hasil):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))

    conn.commit()
    conn.close()


# ------------------------------------------------------------------ Logika
def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"


def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka")
        return

    if not nama:
        messagebox.showerror("Error", "Nama siswa tidak boleh kosong")
        return

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)
    simpan_ke_db(nama, bio, fis, ing, hasil_prediksi)

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    for entry in (entry_nama, entry_bio, entry_fis, entry_ing):
        entry.delete(0, tk.END)


# ---------------------------------------------------------------------- UI
def on_enter(event):
    btn_submit.config(bg=BTN_HOVER, fg="black")


def on_leave(event):
    btn_submit.config(bg=BTN_BG, fg="white")


def buat_input(teks_label):
    """Buat satu pasang Label + Entry, lalu kembalikan Entry-nya."""
    tk.Label(
        root,
        text=teks_label,
        font=("Arial", 14, "bold"),
        bg=BG,
        fg="white",
    ).pack()

    entry = tk.Entry(root, font=("Arial", 13), width=30)
    entry.pack(pady=10)
    return entry


create_db()

root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("500x600")
root.configure(bg=BG)

tk.Label(
    root,
    text="Prediksi Fakultas",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=TITLE_COLOR,
).pack(pady=30)

entry_nama = buat_input("Nama Siswa")
entry_bio = buat_input("Nilai Biologi")
entry_fis = buat_input("Nilai Fisika")
entry_ing = buat_input("Nilai Inggris")

btn_submit = tk.Button(
    root,
    text="Submit Nilai",
    font=("Arial", 14, "bold"),
    bg=BTN_BG,
    fg="white",
    width=20,
    command=submit_nilai,
)
btn_submit.pack(pady=25)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()