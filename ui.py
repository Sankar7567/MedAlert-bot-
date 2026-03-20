import tkinter as tk
from tkinter import ttk
from tracker import add_medicine, log_action
from utils import calculate_adherence
from scheduler import popup_queue
from email_service import send_email_alert
from datetime import datetime


def add_med():
    name = name_entry.get()
    dosage = dosage_entry.get()
    times = [t.strip() for t in time_entry.get().split(",")]

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


# ---------------- POPUP LOGIC ---------------- #

def show_popup(root, name, dosage):
    popup = tk.Toplevel(root)
    popup.title("Medicine Reminder")
    popup.geometry("300x180")
    popup.configure(bg="#1e293b")

    responded = {"value": False}

    def taken():
        responded["value"] = True
        print(f"[DEBUG] TAKEN: {name}")
        log_action(name, datetime.now().strftime("%H:%M"), "taken")
        popup.destroy()

    def missed():
        responded["value"] = True
        print(f"[DEBUG] MISSED (manual): {name}")
        log_action(name, datetime.now().strftime("%H:%M"), "missed")
        send_email_alert(name)
        popup.destroy()

    tk.Label(
        popup,
        text=f"💊 Take {name}\n({dosage})",
        font=("Arial", 12, "bold"),
        bg="#1e293b",
        fg="white"
    ).pack(pady=15)

    tk.Button(
        popup,
        text="✅ Taken",
        command=taken,
        bg="#22c55e",
        fg="white",
        width=15
    ).pack(pady=5)

    tk.Button(
        popup,
        text="❌ Missed",
        command=missed,
        bg="#ef4444",
        fg="white",
        width=15
    ).pack(pady=5)

    def auto_miss():
        if not responded["value"]:
            print(f"[DEBUG] AUTO MISSED: {name}")
            log_action(name, datetime.now().strftime("%H:%M"), "missed")
            send_email_alert(name)
            popup.destroy()

    popup.after(60000, auto_miss)  # 60 seconds


# ---------------- QUEUE LISTENER ---------------- #

def check_queue(root):
    while not popup_queue.empty():
        name, dosage = popup_queue.get()
        show_popup(root, name, dosage)

    root.after(1000, lambda: check_queue(root))  # check every second


# ---------------- MAIN UI ---------------- #

def launch_ui():
    global name_entry, dosage_entry, time_entry, status_label, score_label, progress

    root = tk.Tk()
    root.title("MedTrack")
    root.geometry("400x500")
    root.configure(bg="#0f172a")

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

    # 🔥 START QUEUE LISTENER
    check_queue(root)

    root.mainloop()