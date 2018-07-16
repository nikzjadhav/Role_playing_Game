from classes.game import bcolors,player
from classes.magic import Spell
from classes.inventory import Item
import random
# Black magic
fire = Spell("Fire",10,100,"black")
thunder = Spell("Thunder",20,200,"black")
blizzard = Spell("Blizzard",10,100,"black")
meteor = Spell("Mateor",12,120,"black")
quake = Spell("Quake",14,140,"black")

# White magic
cure = Spell("Cure",25,100,"white")
cura = Spell("Cura",32,180,"white")

#Inventory creation

potion = Item("Potion","potion"," heal for 50 HP",50)
hipotion = Item("hipotion","potion"," heal for 100 HP",100)
superpotion = Item("superpotion","potion","heal for 500 HP",500)
elixer = Item("Elixer","elixer","Restores HP/MP of one member",9999)
hielixer = Item("MegaElixer","elixer","Restores HP/MP of all members",9999)

grenade = Item("Grenade","attack","Deals 500 damage",500)

# initate players
player_spells = [fire,thunder,blizzard,meteor,quake,cure,cura]
enemy_spells = [fire,meteor,cure]
player_items = [{"item": potion,"quantity": 15},{"item":hipotion,"quantity": 5},{"item": superpotion,"quantity":5},
                {"item": elixer, "quantity": 5},{"item": hielixer,"quantity":2},{"item": grenade,"quantity":5}]



person1 = player("nikhil:",3260,132,300,34,player_spells,player_items)
person2 = player("Kunal :",3211,156,311,120,player_spells,player_items)
person3 = player("Rohan :",1234,256,288,120,player_spells,player_items)

enemy1  = player("botv1.5  ",1260,505,125,325,enemy_spells,[])
enemy2  = player("Megatron ",11200,705,525,25,enemy_spells,[])
enemy3  = player("botv2.0  ",1350,600,225,325,enemy_spells,[])

players = [person1,person2,person3]
enemies = [enemy1,enemy2,enemy3]

running = True
print(bcolors.FAIL+bcolors.BOLD+"An Enemy attack !!!"+bcolors.ENDC)

while running:
       print("===================================")

       print("NAME                HP                                    MP")
       for person in players:
              person.get_stats()

       for enemy in enemies:
        enemy.enemy_stats()
       for person in players:
              person.choose_action()
              choice = input("Choose action : ")
              index = int(choice) - 1
              if index == 0:
                     dmg = person.generate_damage()

                     enemy=person.choose_target(enemies)
                     enemies[enemy].take_dmg(dmg)

                     print("You attacked "+enemies[enemy].name +"for",dmg,"points ")
                     if enemies[enemy].get_hp() == 0:
                         print(" "+enemies[enemy].name+"Died !!!")
                         del enemies[enemy]
              elif index == 1:
                     person.choose_magic()
                     magic_choice = int(input("Choose Magic :"))-1

                     if magic_choice == -1:
                            continue

                     spell = person.magic[magic_choice]
                     magic_dmg = spell.generate_damage()
                     cost=spell.cost

                     current_mp = person.get_mp()
                     if spell.cost > current_mp:
                            print(bcolors.FAIL+"\nNot enough MP\n"+bcolors.ENDC)
                            continue

                     person.reduce_mp(spell.cost)

                     if spell.type == "white":
                            person.heal(magic_dmg)
                            print(bcolors.OKBLUE+"\n"+spell.name+"heal for"+str(magic_dmg)+bcolors.ENDC)

                     elif spell.type == "black":

                         enemy = person.choose_target(enemies)
                         enemies[enemy].take_dmg(magic_dmg)
                         print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg)+" points of damage to "+enemies[enemy].name.replace(" ","") + bcolors.ENDC)

                         if enemies[enemy].get_hp() == 0:
                             print(" "+enemies[enemy].name.replace(" ","")+"Died !!!")
                             del enemies[enemy]

              elif index == 2:
                     person.choose_items()
                     item_choice=int(input("Choose Item : ")) - 1

                     if item_choice == -1:
                            continue
                     item = person.items[item_choice]["item"]

                     if person.items[item_choice]["quantity"] == 0:
                            print(bcolors.FAIL+"None Left....\n"+bcolors.ENDC)
                            continue

                     person.items[item_choice]["quantity"] -= 1

                     if item.type == "potion":
                            person.heal(item.prop)
                            print(bcolors.OKGREEN+"\n"+item.name+" heals for "+str(item.prop),"HP"+bcolors.ENDC)

                     elif item.type == "elixer":

                         if item.name == "MegaElixer":
                             for i in players:
                                 i.hp = i.maxhp
                                 i.mp = i.maxmp

                         else:
                            person.hp = person.maxhp
                            person.mp = person.maxmp

                     elif item.type == "attack":
                            enemy = person.choose_target(enemies)
                            enemies[enemy].take_dmg(item.prop)
                            print(bcolors.FAIL + "\n" + item.name + " deals for " + str(item.prop), "HP to"+enemies[enemy].name.replace(" ","") + bcolors.ENDC)

                            if enemies[enemy].get_hp() == 0:
                                print(" " + enemies[enemy].name.replace(" ","") + "Died !!!")
                                del enemies[enemy]
       defeted_enemies = 0
       defeted_players = 0

       for enemy in enemies:
           if enemy.get_hp() == 0:
               defeted_enemies += 1

       for person in players:
           if person.get_hp() == 0:
               defeted_players += 1

       if defeted_enemies == 2:
           print(bcolors.OKGREEN + bcolors.BOLD + "You win this game !!!" + bcolors.ENDC)
           running = False

       elif defeted_players == 2:
           print(bcolors.FAIL + bcolors.BOLD + "You Lost this game !!!" + bcolors.ENDC)
           running = False

       print("\n")
       for enemy in enemies:

           enemy_choice = random.randrange(0,2)
           if enemy_choice == 0:
               target = random.randrange(0,3)
               enemy_dmg = enemy.generate_damage()

               players[target].take_dmg(enemy_dmg)
               print(enemy.name.replace(" ","")+" attacked "+players[target].name.replace(":","") +" for ",enemy_dmg," points ")

           elif enemy_choice == 1:
               spell, magic_dmg = enemy.choose_enemy_spell()
               enemy.reduce_mp(spell.cost)

               if spell.type == "white":
                   enemy.heal(magic_dmg)
                   print(bcolors.OKBLUE +  spell.name + " heals "+ enemy.name +" for " + str(magic_dmg) + bcolors.ENDC)

               elif spell.type == "black":

                   target = random.randrange(0, 3)
                   players[target].take_dmg(magic_dmg)
                   print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ","") +"'s "+ spell.name + " deals " + str(magic_dmg) + " points of damage to " +
                         players[target].name.replace(" ", "") + bcolors.ENDC)

                   if players[target].get_hp() == 0:
                       print(" " + players[target].name.replace(":", "") + " has Died !!!")
                       del players[target]

               #print("Enemy Chose ",spell," damage is ",magic_dmg)


