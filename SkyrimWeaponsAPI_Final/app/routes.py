from flask import Blueprint, request, jsonify
from .models import Weapon
from . import db

main = Blueprint("main", __name__)

@main.route("/weapons", methods=["POST"])
def add_weapon():
    data = request.get_json()
    new_weapon = Weapon(
        name=data["name"],
        damage=data["damage"],
        weight=data["weight"],
        value=data["value"],
        type=data.get("type"),
        upgrade=data.get("upgrade"),
        perk=data.get("perk"),
        category=data.get("category"),
        speed=data.get("speed")
    )
    db.session.add(new_weapon)
    db.session.commit()
    return jsonify({"message": "Weapon added successfully"}), 201

@main.route("/weapons", methods=["GET"])
def get_all_weapons():
    weapons = Weapon.query.all()
    return jsonify([{
        "id": w.id,
        "name": w.name,
        "damage": w.damage,
        "weight": w.weight,
        "value": w.value,
        "type": w.type,
        "upgrade": w.upgrade,
        "perk": w.perk,
        "category": w.category,
        "speed": w.speed
    } for w in weapons])

@main.route("/weapons/search", methods=["GET"])
def search_weapons():
    name = request.args.get("name", "").lower()
    type_ = request.args.get("type", "").lower()
    upgrade = request.args.get("upgrade", "").lower()
    perk = request.args.get("perk", "").lower()
    category = request.args.get("category", "").lower()

    min_damage = request.args.get("min_damage", type=int)
    max_damage = request.args.get("max_damage", type=int)
    min_value = request.args.get("min_value", type=int)
    max_value = request.args.get("max_value", type=int)
    min_weight = request.args.get("min_weight", type=float)
    max_weight = request.args.get("max_weight", type=float)
    min_speed = request.args.get("min_speed", type=float)
    max_speed = request.args.get("max_speed", type=float)

    query = Weapon.query
    if name:
        query = query.filter(Weapon.name.ilike(f"%{name}%"))
    if type_:
        query = query.filter(Weapon.type.ilike(f"%{type_}%"))
    if upgrade:
        query = query.filter(Weapon.upgrade.ilike(f"%{upgrade}%"))
    if perk:
        query = query.filter(Weapon.perk.ilike(f"%{perk}%"))
    if category:
        query = query.filter(Weapon.category.ilike(f"%{category}%"))
    if min_damage is not None:
        query = query.filter(Weapon.damage >= min_damage)
    if max_damage is not None:
        query = query.filter(Weapon.damage <= max_damage)
    if min_value is not None:
        query = query.filter(Weapon.value >= min_value)
    if max_value is not None:
        query = query.filter(Weapon.value <= max_value)
    if min_weight is not None:
        query = query.filter(Weapon.weight >= min_weight)
    if max_weight is not None:
        query = query.filter(Weapon.weight <= max_weight)
    if min_speed is not None:
        query = query.filter(Weapon.speed >= min_speed)
    if max_speed is not None:
        query = query.filter(Weapon.speed <= max_speed)

    results = query.all()
    return jsonify([{
        "id": w.id,
        "name": w.name,
        "damage": w.damage,
        "weight": w.weight,
        "value": w.value,
        "type": w.type,
        "upgrade": w.upgrade,
        "perk": w.perk,
        "category": w.category,
        "speed": w.speed
    } for w in results])
