import pandas as pd
from app import create_app, db
from app.models import Weapon

app = create_app()

CSV_PATH = "Skyrim_Weapons.csv"

with app.app_context():
    df = pd.read_csv(CSV_PATH)
    db.drop_all()
    db.create_all()

    for _, row in df.iterrows():
        weapon = Weapon(
            name=row["Name"],
            damage=row["Damage"],
            weight=row["Weight"],
            value=row["Gold"],
            type=row["Type"],
            upgrade=row.get("Upgrade"),
            perk=row.get("Perk"),
            category=row.get("Category"),
            speed=row.get("Speed") if not pd.isna(row.get("Speed")) else None
        )
        db.session.add(weapon)

    db.session.commit()
    print("Database seeded with Skyrim weapons!")
