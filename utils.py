from storage import load_data

def calculate_adherence():
    data = load_data()

    total = 0
    taken = 0

    for med in data:
        for entry in med["history"]:
            total += 1
            if entry["status"] == "taken":
                taken += 1

    if total == 0:
        return 0

    return round((taken / total) * 100, 2)