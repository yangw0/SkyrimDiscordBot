import requests

API_URL = "http://127.0.0.1:5000"

def print_menu():
    print("\nSkyrim Weapons API CLI")
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
        "upgrade": upgrade or None,
        "perk": perk or None,
        "category": category or None,
        "speed": float(speed) if speed else None
    }
    r = requests.post(f"{API_URL}/weapons", json=data)
    print(r.json())

def view_weapons():
    print("\n1. View All Weapons")
    print("2. Search Weapons")
    sub_choice = input("Choose an option: ")
    if sub_choice == "1":
        r = requests.get(f"{API_URL}/weapons")
        weapons = r.json()
        if weapons:
            for weapon in weapons:
                print_weapon(weapon)
        else:
            print("No weapons found.")
    elif sub_choice == "2":
        name = input("Search by Name (or leave blank): ")
        type_ = input("Search by Type (or leave blank): ")
        params = {}
        if name:
            params["name"] = name
        if type_:
            params["type"] = type_
        r = requests.get(f"{API_URL}/weapons/search", params=params)
        weapons = r.json()
        if weapons:
            for weapon in weapons:
                print_weapon(weapon)
        else:
            print("No weapons found matching your criteria.")
    else:
        print("Invalid option.")

def print_weapon(w):
    print(f"{w['id']}: {w['name']} | Damage: {w['damage']} | Weight: {w['weight']} | Value: {w['value']} | "
          f"Type: {w['type']} | Upgrade: {w['upgrade']} | Perk: {w['perk']} | Category: {w['category']} | Speed: {w['speed']}")

def update_weapon():
    id_ = int(input("Weapon ID to update: "))
    print("Leave a field blank to keep the current value.")
    name = input("New Name: ")
    damage = input("New Damage: ")
    weight = input("New Weight: ")
    value = input("New Value: ")
    type_ = input("New Type: ")
    upgrade = input("New Upgrade: ")
    perk = input("New Perk: ")
    category = input("New Category: ")
    speed = input("New Speed: ")
    data = {}
    if name: data["name"] = name
    if damage: data["damage"] = int(damage)
    if weight: data["weight"] = float(weight)
    if value: data["value"] = int(value)
    if type_: data["type"] = type_
    if upgrade: data["upgrade"] = upgrade
    if perk: data["perk"] = perk
    if category: data["category"] = category
    if speed: data["speed"] = float(speed)
    r = requests.put(f"{API_URL}/weapons/{id_}", json=data)
    print(r.json())

def delete_weapon():
    id_ = int(input("Weapon ID to delete: "))
    r = requests.delete(f"{API_URL}/weapons/{id_}")
    print(r.json())

if __name__ == "__main__":
    while True:
        print_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            add_weapon()
        elif choice == "2":
            view_weapons()
        elif choice == "3":
            update_weapon()
        elif choice == "4":
            delete_weapon()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
