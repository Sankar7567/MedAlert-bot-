import threading
from scheduler import run_scheduler
from ui import launch_ui

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    launch_ui()  # Tkinter runs in main thread ✅