class Armour:
    def __init__(self, id, name, defense, rarity):
        self.name = name
        self.damage = defense
        self.id = id
        self.rarity = rarity #1-5, common, rare, epic, legendary, mythic

armour_library = [
    Armour("1", "Wooden Sword", 10, 1),
    Armour("2", "Wooden Axe", 15, 1),
    Armour("3",  "Wooden Dagger", 15, 1),
    Armour("4", "Wooden Staff", 20, 1)
]
