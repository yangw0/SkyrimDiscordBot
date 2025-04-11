import requests

API_URL = "http://127.0.0.1:5000"

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_menu():
    print(f"\n{Color.HEADER}{Color.BOLD}Skyrim Weapons API CLI{Color.ENDC}")
    print("1. Add Weapon")
    print("2. View Weapons")
    print("3. Update Weapon")
    print("4. Delete Weapon")
    print("5. Exit")

def add_weapon():
    name = input("Name: ")
    damage = int(input("Damage: "))
    weight = float(input("Weight: "))
    value = int(input("Value: "))
    type_ = input("Type: ")
    upgrade = input("Upgrade: ")
    perk = input("Perk: ")
    category = input("Category: ")
    speed = input("Speed: ")
    data = {
        "name": name,
        "damage": damage,
        "weight": weight,
        "value": value,
        "type": type_,
        "upgrade": upgrade,
        "perk": perk,
        "category": category,
        "speed": float(speed) if speed else None
    }
    r = requests.post(f"{API_URL}/weapons", json=data)
    print(r.json())

def view_weapons():
    print("1. View All Weapons")
    print("2. Search Weapons")
    choice = input("Choose an option: ")
    if choice == "1":
        r = requests.get(f"{API_URL}/weapons")
        for w in r.json():
            print_weapon(w)
    else:
        filters = {}
        filters["name"] = input("Name: ")
        filters["type"] = input("Type: ")
        filters["upgrade"] = input("Upgrade: ")
        filters["perk"] = input("Perk: ")
        filters["category"] = input("Category: ")
        filters["min_damage"] = input("Min Damage: ")
        filters["max_damage"] = input("Max Damage: ")
        filters["min_value"] = input("Min Value: ")
        filters["max_value"] = input("Max Value: ")
        filters["min_weight"] = input("Min Weight: ")
        filters["max_weight"] = input("Max Weight: ")
        filters["min_speed"] = input("Min Speed: ")
        filters["max_speed"] = input("Max Speed: ")
        query = {k: v for k, v in filters.items() if v}
        r = requests.get(f"{API_URL}/weapons/search", params=query)
        for w in r.json():
            print_weapon(w)

def print_weapon(w):
    print(f"{Color.OKGREEN}{w['id']}: {w['name']}{Color.ENDC} | Dmg: {w['damage']} | Wgt: {w['weight']} | "
          f"Val: {w['value']} | Type: {w['type']} | Upg: {w['upgrade']} | Perk: {w['perk']} | "
          f"Cat: {w['category']} | Spd: {w['speed']}")

def update_weapon():
    id_ = int(input("Weapon ID: "))
    data = {}
    for field in ["name", "damage", "weight", "value", "type", "upgrade", "perk", "category", "speed"]:
        val = input(f"{field.capitalize()}: ")
        if val:
            data[field] = float(val) if field in ["damage", "weight", "value", "speed"] else val
    r = requests.put(f"{API_URL}/weapons/{id_}", json=data)
    print(r.json())

def delete_weapon():
    id_ = int(input("Weapon ID: "))
    r = requests.delete(f"{API_URL}/weapons/{id_}")
    print(r.json())

if __name__ == "__main__":
    while True:
        print_menu()
        ch = input("Choose: ")
        if ch == "1":
            add_weapon()
        elif ch == "2":
            view_weapons()
        elif ch == "3":
            update_weapon()
        elif ch == "4":
            delete_weapon()
        elif ch == "5":
            break
        else:
            print(f"{Color.FAIL}Invalid option!{Color.ENDC}")
