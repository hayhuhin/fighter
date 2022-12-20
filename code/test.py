class Hero:
    def __init__(self,hp,mana):
        self.hp = 10
        self.mana = 20

    def attack(self,amount,target):
        target.hp -= amount
        print(target.name,"took ",amount ," damage")




class Monster:
    def __init__(self,name):
        self.name = name
        self.hp = 100
        self.damage = 20

    
arti = Hero(100,50)

monster1 = Monster("monster")

arti.attack(5,monster1)
print(monster1.hp)

