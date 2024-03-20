class item:
    def __init__(self, id, name, type, damage, defense, rarity):
        self.name = name
        self.damage = damage
        self.defense = defense
        self.type = type
        self.id = id
        self.rarity = rarity #1-5, common, rare, epic, legendary, mythic

item_library = [
    item("1", "Wooden Sword", "weapon", 10, 0, 1),
    item("2", "Wooden Axe", "weapon", 15, 0, 1), 
    item("3",  "Wooden Dagger", "weapon", 15, 0, 1),
    item("4", "Wooden Staff", "weapon", 20, 0, 1),
    item("5", "Broken Robe", "armour", 0, 10, 1),
    item("6", "Broken Plate", "armour", 0, 15, 1),
    item("7", "Ordinary Cloak", "armour", 0, 20, 1),
    item("8", "Used Plate", "armour", 0, 25, 1)
]
