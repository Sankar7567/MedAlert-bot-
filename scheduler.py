import time
from datetime import datetime
from storage import load_data
from tracker import log_action
from email_service import send_email_alert
import tkinter as tk


def check_medicines():
    now = datetime.now().strftime("%H:%M")
    data = load_data()

    for med in data:
        if now in med["times"]:
            show_popup(med["name"], med["dosage"])


def show_popup(name, dosage):
    popup = tk.Tk()
    popup.title("Medicine Reminder")
    popup.geometry("300x180")
    popup.configure(bg="#1e293b")

    responded = {"value": False}

    # -------- BUTTON FUNCTIONS -------- #
    def taken():
        responded["value"] = True
        log_action(name, datetime.now().strftime("%H:%M"), "taken")
        popup.destroy()

    def missed():
        responded["value"] = True
        log_action(name, datetime.now().strftime("%H:%M"), "missed")
        send_email_alert(name)
        popup.destroy()

    # -------- UI -------- #
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

    # -------- AUTO TIMEOUT (10 sec) -------- #
    def auto_miss():
        if not responded["value"]:
            log_action(name, datetime.now().strftime("%H:%M"), "missed")
            send_email_alert(name)
            popup.destroy()

    popup.after(10000, auto_miss)

    popup.mainloop()


def run_scheduler():
    while True:
        check_medicines()
        time.sleep(60)