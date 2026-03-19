import tkinter as tk
from tkinter import ttk
from tracker import add_medicine
from utils import calculate_adherence

def add_med():
    name = name_entry.get()
    dosage = dosage_entry.get()
    times = time_entry.get().split(",")

    add_medicine(name, dosage, times)

    status_label.config(text="✅ Medicine Added!", foreground="green")


def show_score():
    score = calculate_adherence()

    if score >= 90:
        msg = "🔥 Excellent"
        color = "green"
    elif score >= 70:
        msg = "⚡ Moderate"
        color = "orange"
    else:
        msg = "⚠️ Poor"
        color = "red"

    score_label.config(text=f"{score}% - {msg}", foreground=color)
    progress['value'] = score


def launch_ui():
    global name_entry, dosage_entry, time_entry, status_label, score_label, progress

    root = tk.Tk()
    root.title("MedTrack")
    root.geometry("400x500")
    root.configure(bg="#0f172a")  # dark background

    style = ttk.Style()
    style.theme_use("default")

    # Title
    tk.Label(root, text="💊 MedTrack", font=("Arial", 18, "bold"),
             bg="#0f172a", fg="white").pack(pady=10)

    # Input Frame
    frame = tk.Frame(root, bg="#1e293b", padx=10, pady=10)
    frame.pack(pady=10, fill="x", padx=20)

    tk.Label(frame, text="Medicine Name", bg="#1e293b", fg="white").pack()
    name_entry = tk.Entry(frame)
    name_entry.pack(pady=5)

    tk.Label(frame, text="Dosage", bg="#1e293b", fg="white").pack()
    dosage_entry = tk.Entry(frame)
    dosage_entry.pack(pady=5)

    tk.Label(frame, text="Times (HH:MM, comma separated)", bg="#1e293b", fg="white").pack()
    time_entry = tk.Entry(frame)
    time_entry.pack(pady=5)

    tk.Button(frame, text="➕ Add Medicine", command=add_med,
              bg="#22c55e", fg="white").pack(pady=10)

    status_label = tk.Label(root, bg="#0f172a", fg="white")
    status_label.pack()

    # Adherence Section
    tk.Label(root, text="Adherence Score", font=("Arial", 14),
             bg="#0f172a", fg="white").pack(pady=10)

    progress = ttk.Progressbar(root, length=250, mode='determinate')
    progress.pack(pady=5)

    score_label = tk.Label(root, text="", font=("Arial", 12),
                           bg="#0f172a", fg="white")
    score_label.pack()

    tk.Button(root, text="📊 Check Score", command=show_score,
              bg="#3b82f6", fg="white").pack(pady=15)

    root.mainloop()