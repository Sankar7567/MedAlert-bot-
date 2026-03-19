from datetime import datetime
from storage import load_data, save_data

def add_medicine(name, dosage, times):
    data = load_data()

    medicine = {
        "name": name,
        "dosage": dosage,
        "times": times,  # ["09:00", "14:00"]
        "history": []
    }

    data.append(medicine)
    save_data(data)


def log_action(name, time, status):
    data = load_data()

    for med in data:
        if med["name"] == name:
            med["history"].append({
                "time": time,
                "date": str(datetime.now().date()),
                "status": status
            })

    save_data(data)