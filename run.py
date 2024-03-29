import battlecode as bc
import random
import sys
import traceback

import os
print(os.getcwd())

#print("Test starting")

gc = bc.GameController()
# Initializing code
all_map_directions = [bc.Direction.Center, bc.Direction.North, bc.Direction.Northeast, bc.Direction.East,
bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest,
bc.Direction.West, bc.Direction.Northwest]

directions = [bc.Direction.North, bc.Direction.Northeast,
            bc.Direction.East, bc.Direction.Southeast, bc.Direction.South,
            bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]

tryRotate = [0,-1,-7,-2,-6]
mining = True
enemy_sensed = False
got_to_enemy_start = False
blocked = {}
miners = []
builders = []
workers = []
dukan = []
amadhya = []
knights = []
mages = []
pants = []
the_lone_ranger = []
the_neighborhood_watch = []
maploc = []
temp = []
mars_maploc = []
steps_north = 0
steps_east = 0
steps_west = 0
steps_south = 0
prev_dir = bc.Direction.Center
earthMap = gc.starting_map(bc.Planet.Earth)
marsMap = gc.starting_map(bc.Planet.Mars)
centre = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)
enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)
#print("TestStarter")

#### DIFFERENT UNITS MAX_NUMBER
max_workers = 5
max_knights = 0
max_mages = 0
random.seed(1047)
## A list of all passable locations on mars ##
i = 0
while i< marsMap.width:
    j=0
    while j < marsMap.height:
        loc = bc.MapLocation(bc.Planet.Mars, i, j)
        if marsMap.is_passable_terrain_at(loc):
            mars_maploc.append(loc)
        j+=1
    i+=1
random.shuffle(mars_maploc)

## Research
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Worker)

my_team = gc.team()
print(my_team)

def invert(loc):
    newx=earthMap.width-loc.x
    newy=earthMap.height-loc.y
    return bc.MapLocation(bc.Planet.Earth,newx,newy)

def Karbonite_Mining(id,directions,unit,mining):
    karbonite_collected = False
    for d in all_map_directions:
        if gc.can_harvest(id, d):
            gc.harvest(id, d)
            prev_dir = d
            karbonite_collected = False
            break
        else:
            karbonite_collected = True

    if  karbonite_collected == True and gc.is_move_ready(id):
        for i in [5,10,17,26,37,50]:
            for loc in gc.all_locations_within(location.map_location(),i):
                if gc.karbonite_at(loc) != 0:
                    mining = True
                    fuzzygoto(unit,loc)
                    break
                else:
                    mining = False
            if mining == True:
                break
    return(mining)

def rotate(dir,amount):
    ind = directions.index(dir)
    return directions[(ind+amount)]
# Path finding
def fuzzygoto(unit,dest):
    toward = unit.location.map_location().direction_to(dest)
    for tilt in  tryRotate:
        d = rotate(toward,tilt)
        if gc.can_move(unit.id,d):
            if unit.id not in blocked.keys():
                if d == bc.Direction.North:
                    blocked[unit.id] = [bc.Direction.South,bc.Direction.Southeast,bc.Direction.Southwest]
                elif d == bc.Direction.Northeast:
                    blocked[unit.id] = [bc.Direction.Southwest,bc.Direction.South,bc.Direction.West]
                elif d == bc.Direction.East:
                    blocked[unit.id] = [bc.Direction.West,bc.Direction.Southwest,bc.Direction.Northwest]
                elif d == bc.Direction.Southeast:
                     blocked[unit.id] = [bc.Direction.Northwest,bc.Direction.North,bc.Direction.West]
                elif d == bc.Direction.South:
                    blocked[unit.id] = [bc.Direction.North,bc.Direction.Northeast,bc.Direction.Northwest]
                elif d == bc.Direction.Southwest:
                    blocked[unit.id] = [bc.Direction.Northeast,bc.Direction.North,bc.Direction.East]
                elif d == bc.Direction.West:
                    blocked[unit.id] = [bc.Direction.East,bc.Direction.Northeast,bc.Direction.Southeast]
                elif d == bc.Direction.Northwest:
                    blocked[unit.id] = [bc.Direction.Southeast,bc.Direction.South,bc.Direction.East]
                else:
                    continue
            for values in blocked[unit.id]:
                if values == d:
                    stinky = True
                    break
                else:
                    stinky = False
            if stinky == False:
                gc.move_robot(unit.id,d)
                break
            if d == bc.Direction.North:
                blocked[unit.id] = [bc.Direction.South,bc.Direction.Southeast,bc.Direction.Southwest]
            elif d == bc.Direction.Northeast:
                blocked[unit.id] = [bc.Direction.Southwest,bc.Direction.South,bc.Direction.West]
            elif d == bc.Direction.East:
                blocked[unit.id] = [bc.Direction.West,bc.Direction.Southwest,bc.Direction.Northwest]
            elif d == bc.Direction.Southeast:
                blocked[unit.id] = [bc.Direction.Northwest,bc.Direction.North,bc.Direction.West]
            elif d == bc.Direction.South:
                blocked[unit.id] = [bc.Direction.North,bc.Direction.Northeast,bc.Direction.Northwest]
            elif d == bc.Direction.Southwest:
                blocked[unit.id] = [bc.Direction.Northeast,bc.Direction.North,bc.Direction.East]
            elif d == bc.Direction.West:
                blocked[unit.id] = [bc.Direction.East,bc.Direction.Northeast,bc.Direction.Southeast]
            elif d == bc.Direction.Northwest:
                blocked[unit.id] = [bc.Direction.Southeast,bc.Direction.South,bc.Direction.East]

def lay_blueprint(worker_id, structure):
    for d in [directions[1], directions[3], directions[5],directions[7]]:
        if gc.can_blueprint(worker_id, structure, d):
            gc.blueprint(worker_id, structure, d)
        else:
            continue

while True:
    print('pyround:', gc.round())

    try:
        for unit in gc.my_units():
            location = unit.location
            if gc.round() == 1:
                start_node = location.map_location()
                enemy_start = invert(start_node)
                miners.append(unit.id) # starting workers are miners

                if start_node.y < earthMap.height//2: # find out whether in top or bottom
                    if 'Bottom' not in maploc:
                        maploc.append('Bottom')
                if start_node.y > earthMap.height//2:
                    if 'Top' not in maploc:
                        maploc.append('Top')

                for d in directions:
                    if gc.can_replicate(unit.id, d): # try to make new workers now
                        gc.replicate(unit.id, d)
                    else:
                        continue

            elif gc.round() == 2:
                start_node = location.map_location()
                if unit.id not in miners:
                    builders.append(unit.id) # new workers initialized as builders
                if len(maploc) == 1: # find out whether in left or right
                    pos = maploc[0]
                else:
                    if start_node.x < earthMap.width//2:
                        if 'Left' not in temp:
                            temp.append('Left')
                    if start_node.x > earthMap.width//2:
                        if 'Right' not in temp:
                            temp.append('Right')

            elif gc.round() ==3:
                if len(temp)== 1:
                    pos = temp[0]
                elif len(temp) ==2:
                    pos ='Opposite'
                temp.clear()
                if pos == 'Top':
                    our_border = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,2**(earthMap.height)//3)
                    our_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height))
                    enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,0)
                elif pos == 'Bottom':
                    our_border = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//3)
                    our_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,0)
                    enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height))
                elif pos == 'Left':
                    our_border = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//3,(earthMap.height)//3)
                    our_edge = bc.MapLocation(bc.Planet.Earth,0,(earthMap.height)//2)
                    enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width),(earthMap.height)//2)
                elif pos == 'Right':
                    our_border = bc.MapLocation(bc.Planet.Earth,2**(earthMap.width)//3,(earthMap.height)//3)
                    our_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width),(earthMap.height)//2)
                    enemy_edge = bc.MapLocation(bc.Planet.Earth,0,(earthMap.height)//2)
                else:
                    enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)

            if unit.id not in workers: # the workers list
                workers.append(unit.id)
### Workers ###
            if unit.unit_type == bc.UnitType.Worker:
                if not unit.id in miners and not unit.id in builders:
                    miners.append(unit.id)

                if location.is_in_garrison():
                    rocket_id = location.structure()
                    for d in directions:
                        if gc.can_unload(rocket_id,d):
                            gc.unload(rocket_id,d)
                            gc.disintegrate_unit(rocket_id)

                if len(workers) < max_workers and (gc.round())%5 == 0: # continue replication till sufficient
                    for d in directions:
                        if gc.can_replicate(unit.id,d):
                            gc.replicate(unit.id,d)

                if unit.id in miners: # miners mine
                    mining = Karbonite_Mining(unit.id,directions,unit,mining)
                    if mining == False:
                            miners.remove(unit.id)
                            if len(miners) == 0:
                                mining = False
                            else:
                                mining = True
                            if mining == False:
                                direction_to_start_node=unit.location.map_location().direction_to(enemy_edge)
                                ind_for_this=directions.index(direction_to_start_node)
                                for tilt in  tryRotate:
                                    d = rotate(directions[ind_for_this - 4],tilt)
                                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id):
                                        if pos == 'Top' or pos == 'Bottom':
                                            if location.map_location().y != our_border.y:
                                                gc.move_robot(unit.id,d)
                                                break
                                        elif pos == 'Left' or pos == 'Right':
                                            if location.map_location().x != our_border.x:
                                                gc.move_robot(unit.id,d)
                                                break
                                if location.is_on_map():
                                    nearby = gc.sense_nearby_units(location.map_location(), 2)
                                    for other in nearby:
                                        if other.unit_type == bc.UnitType.Factory:
                                            if other.structure_is_built() and not other.id in dukan:
                                                continue
                                            elif gc.can_build(unit.id,other.id):
                                                gc.build(unit.id, other.id)
                                            elif gc.can_repair(unit.id,other.id) and other.health<other.max_health:
                                                 gc.repair(unit.id,other.id)
                                        if other.unit_type == bc.UnitType.Rocket:
                                            if other.structure_is_built() and not other.id in pants:
                                                continue
                                            elif gc.can_build(unit.id, other.id):
                                                gc.build(unit.id, other.id)
                else:
                    for d in all_map_directions:
                        if gc.can_harvest(unit.id, d):
                            gc.harvest(unit.id, d)
                            break
                    # blueprint and build
                    if location.is_on_map():
                        nearby = gc.sense_nearby_units(location.map_location(), 2)
                        for other in nearby:
                            if other.unit_type == bc.UnitType.Factory:
                                if other.structure_is_built() and not other.id in dukan:
                                    continue
                                elif gc.can_build(unit.id,other.id):
                                    gc.build(unit.id, other.id)
                                elif gc.can_repair(unit.id,other.id) and other.health<other.max_health:
                                     gc.repair(unit.id,other.id)
                            if other.unit_type == bc.UnitType.Rocket:
                                if other.structure_is_built() and not other.id in pants:
                                    continue
                                elif gc.can_build(unit.id, other.id):
                                    gc.build(unit.id, other.id)
                        if gc.karbonite() > 100 and len(pants)<4:
                            lay_blueprint(unit.id, bc.UnitType.Rocket)
                        if gc.karbonite() > 200 and len(dukan)<8:
                            lay_blueprint(unit.id, bc.UnitType.Factory)
### Rocket Science ###
            if unit.unit_type == bc.UnitType.Rocket:
                if not unit.id in pants:
                    pants.append(unit.id)
                if unit.health == 0:
                    pants.remove(unit.id)
                garrison = unit.structure_garrison()
                if len(garrison) == 0:
                    nearby = gc.sense_nearby_units(location.map_location(),2)
                    for robot in nearby:
                        if gc.is_move_ready(robot.id) and gc.can_load(unit.id, robot.id):
                            gc.load(unit.id, robot.id)
                            print('unit has been loaded!')
                elif len(garrison) != 0:
                    if location.is_on_planet(bc.Planet.Earth) and gc.current_duration_of_flight()<100:
                        for land in mars_maploc:
                            if gc.has_unit_at_location(land) == False and gc.can_launch_rocket(unit.id, land):
                                mars_maploc.remove(land)
                                gc.launch_rocket(unit.id, land)
                                print('a rocket has been launched!')
                    elif location.is_on_planet(bc.Planet.Mars):
                        print("I'm on Mars!")
                        for d in directions:
                            if gc.can_unload(unit.id,d):
                                gc.unload(unit.id,d)
### Factory Output ###
            if unit.unit_type == bc.UnitType.Factory:
                if not unit.id in dukan:
                    dukan.append(unit.id)

                garrison = unit.structure_garrison()
                if len(garrison)>0:
                    for d in directions:
                        if gc.can_unload(unit.id,d):
                            gc.unload(unit.id,d)

                else:
                    if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                        if (enemy_sensed==False and got_to_enemy_start==False) and len(amadhya)<5:
                            gc.produce_robot(unit.id, bc.UnitType.Ranger)
                            print('produced a ranger!')
                        elif (enemy_sensed==True or got_to_enemy_start==True) and len(amadhya)<7:
                            gc.produce_robot(unit.id, bc.UnitType.Ranger)
                            print('produced a ranger!')

                    if gc.can_produce_robot(unit.id, bc.UnitType.Mage) and len(mages)<max_mages:
                        gc.produce_robot(unit.id, bc.UnitType.Mage)
                        print('produced a mage!')

                    if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                        if len(knights)<max_knights and (enemy_sensed==False or got_to_enemy_start==False):
                            gc.produce_robot(unit.id, bc.UnitType.Knight)
                            print('produced a knight!')
                        elif (enemy_sensed==True or got_to_enemy_start==True) and len(knights)<10:
                            gc.produce_robot(unit.id, bc.UnitType.Knight)
                            print('produced a knight!')

### Rangers ###
            if  unit.unit_type == bc.UnitType.Ranger :
                if not unit.id in amadhya:
                    amadhya.append(unit.id)

                if location.is_on_map():
                    close_by_for_ranger= gc.sense_nearby_units(location.map_location(), 70)
                    for junta in close_by_for_ranger:
                        if junta.team != my_team and  gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, junta.id) :
                            print("attacking a thing")
                            gc.attack(unit.id, junta.id)
                            break
                        elif not gc.can_attack(unit.id,junta.id) and unit.id in the_neighborhood_watch and junta.team !=my_team:
                            enemy_sensed=True
                            need_backup_at = location.map_location()
                            print(need_backup_at)
                            continue

                    if not unit.id in the_lone_ranger and len(the_lone_ranger)==0:
                        the_lone_ranger.append(unit.id)

                    if unit.id in the_lone_ranger:
                        if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(our_edge)!= bc.Direction.Center :
                            direction_to_start_node=unit.location.map_location().direction_to(our_edge)
                            ind_for_this=directions.index(direction_to_start_node)
                            for tilt in  tryRotate:
                                d = rotate(directions[ind_for_this - 4],tilt)
                                if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id):
                                    if pos == 'Top' or pos == 'Bottom':
                                        if location.map_location().y != our_border.y:
                                            gc.move_robot(unit.id,d)
                                            break
                                    elif pos == 'Left' or pos == 'Right':
                                        if location.map_location().x != our_border.x:
                                            gc.move_robot(unit.id,d)
                                            break

                    if not unit.id in the_lone_ranger and enemy_sensed==False and len(the_neighborhood_watch)<5:
                        the_neighborhood_watch.append(unit.id)
### Knights ###
            if  unit.unit_type == bc.UnitType.Knight :
                if not unit.id in knights:
                    knights.append(unit.id)

                if location.is_on_map():
                    close_by=gc.sense_nearby_units(location.map_location(), 2)
                    for enemy in close_by:
                        if enemy.team !=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,enemy.id) :
                            print("attacking a thing")
                            gc.attack(unit.id,enemy.id)
                            break
                        else:
                            continue
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(our_border)!= bc.Direction.Center:
                            if pos == 'Top' or pos == 'Bottom':
                                if location.map_location().y != our_border.y:
                                    fuzzygoto(unit,our_border)
                            if pos == 'Left' or pos == 'Right':
                                if location.map_location().x != our_border.x:
                                    fuzzygoto(unit,our_border)
                    if unit.health == 0:
                        knights.remove(unit.id)
            ### Mages ### currently goes straight up.
            if unit.unit_type == bc.UnitType.Mage :
                if not unit.id in mages:
                    mages.append(unit.id)
                    print(len(mages))

                if location.is_on_map():
                    close_by = gc.sense_nearby_units(location.map_location(), 30)
                    for athing in close_by:
                        if athing.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, athing.id):
                            gc.attack(unit.id, athing.id)
                            print('literally attacking a thing')
                            break
                        else:
                            continue

                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(centre)!= bc.Direction.Center :
                            fuzzygoto(unit, unit.location.map_location().translate(0, earthMap.height))
    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
