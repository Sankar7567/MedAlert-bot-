import time
from datetime import datetime
from storage import load_data, save_data
from queue import Queue

# Shared queue between scheduler and UI
popup_queue = Queue()


def check_medicines():
    now = datetime.now().strftime("%H:%M")
    data = load_data()

    for med in data:
        if "last_triggered" not in med:
            med["last_triggered"] = None

        if now in med["times"] and med["last_triggered"] != now:
            print(f"[DEBUG] Triggering {med['name']} at {now}")
            med["last_triggered"] = now

            # ✅ Send event to UI instead of opening popup
            popup_queue.put((med["name"], med["dosage"]))

    save_data(data)


def run_scheduler():
    while True:
        check_medicines()
        time.sleep(60)