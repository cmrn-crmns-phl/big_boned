import csv
from datetime import datetime
import math
import random
import time
import uuid

width = 700
height= 700

# print("[ initializing... ]")
global starttime
starttime  = datetime.now().replace(microsecond=0)
# print(starttime)
time.sleep(1)

lap_seconds = datetime.now().replace(microsecond=0)-starttime
# print("\n[ steppe ]")
global steppe
steppe = 1

global stamp
stamp = datetime.now().replace(microsecond=0)
# print(stamp)



def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)

def in_circle(center_x, center_y, radius, x, y):

    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2

    if square_dist <= radius ** 2:

        return True

class Behavior(object):
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, fish, carcass, state):
        pass

    def apply(self, fish, state):
        pass

    def draw(self, fish, state):
        pass


class CarcassBehavior(object):
    print("carcass behavior")
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, carcass, fish, state):
        pass

    def apply(self, carcass, state):
        pass

    def draw(self, carcass, state):
        pass

# MoveTowardsCenterOfNearbyFish(closeness=50.0, threshold=25.0, speedfactor=100.0, weight=20.0)
class PreyBehavior(object):
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, prey, fish, state):
        pass

    def apply(self, prey, state):
        pass

    def draw(self, prey, state):
        pass



class MoveTowardsPrey(Behavior):

    def setup(self, fish, prey, state):

        # print("[ begin move toward prey ]")


        if fish is prey:

            # # print" is prey ")

            return

        if "prey_closecount" not in state:
            # # print"prey closecount")
            state["prey_closecount"]=0.0

        if "center" not in state:

            state["center"] = [0.0,0.0]


        if "closest_carcass" not in state:
            
            state["closest_carcass"]=[0.0,0.0]

        closeness = fish.binocular_vision[0]



        for prey in allprey:

            prey.position[0] = prey.position[0]

            prey.position[1] = prey.position[1]

            if in_circle(center_x = prey.position[0], center_y=prey.position[1], radius=closeness, x=fish.position[0], y=fish.position[1]):

                print("[ prey detected! ]")

                distance_to_prey = dist(prey.position[0], prey.position[1], fish.position[0], fish.position[1])
 

                if distance_to_prey < closeness:

                    consumption_kg_per_day = fish.tailfat[0]

                    consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                    prey.set_attributes(speed=prey.speed*(1+fish.hearing[0]))
                    
                    # print("set prey attributes")

                    # printprey.speed)

                    if state['closecount'] == 0:

                        state['center'] = prey.position

                        state['prey_closecount'] += 1.0
                        
                        if random.random()<(.05*(1+fish.bite_force[0])):
                            print("killed one")
                            allprey.remove(prey)
                            el = Carcass()
                            el.set_attributes(energy=prey.energy,position=prey.position)
                            allcarcasses.append(Carcass())

                        else:
                            
                            continue

                    else:


                        state['center'][0] *= state['prey_closecount']

                        state['center'][1] *= state['prey_closecount']

                        # state['center'][0] += prey.position[0]
                        # state['center'][1] += prey.position[1]

                        state['center'] = [
                            state['center'][0] + prey.position[0],
                            state['center'][1] + prey.position[1]
                            ]

                        state['prey_closecount'] += 1.0

                        state['center'][0] /= state['prey_closecount']

                        state['center'][1] /= state['prey_closecount']

                    continue

            else:

                if random.random() > .995:

                    prey.direction = random.uniform(-3,3)

            if len(allprey)<20:
                # print("\n\n\n[ you betta prey ]")

                allprey.append(Prey())

    def apply(self, fish, state):

        if state['prey_closecount'] == 0:

            # # print"--- prey closecount == 0 ---")

            return

        center = state['center']

        distance_to_center = dist(center[0], center[1],fish.position[0], fish.position[1])

        closeness = fish.binocular_vision[0]

        if distance_to_center < closeness:



            angle_to_center = math.atan2(
                fish.position[1] - center[1],
                fish.position[0] - center[0]
                )


            fish.turnrate += (angle_to_center - fish.direction) / self.parameters['weight']

            stroke(200, 200, 255)

            line(fish.position[0], fish.position[1], center[0], center[1])



    def draw(self, fish, state):
        # # print"draw")
        closeness = fish.binocular_vision[0]
        # # printcloseness)

        stroke(200, 200, 255)
        noFill()
        ellipse(fish.position[0], fish.position[1], closeness * 2, closeness * 2)
        #print" --| end move towards prey |--")


class PreySwim(Behavior):
    #print("this is preyswim 826")

    def setup(self, prey, state):
        prey.speed = 2.7
        prey.turnrate = 0


    def apply(self, prey, state):
        # Move forward, but not too fast.
        if prey.speed > self.parameters['speedlimit']:
            prey.speed = self.parameters['speedlimit']
        prey.position[0] -= math.cos(prey.direction) * prey.speed
        prey.position[1] -= math.sin(prey.direction) * prey.speed

        # Turn, but not too fast.
        if prey.turnrate > self.parameters['turnratelimit']:
            prey.turnrate = self.parameters['turnratelimit']
        if prey.turnrate < -self.parameters['turnratelimit']:
            prey.turnrate = -self.parameters['turnratelimit']
        prey.direction += prey.turnrate


        # Fix the angles.
        if prey.direction > math.pi:
            prey.direction -= 2 * math.pi

        if prey.direction < -math.pi:
            prey.direction += 2 * math.pi
            
    def draw(self, fish, state):
        # print("drawing prey")
        # print(self.__dict__)
        # closeness = fish.detection_range[0]
        # print(closeness)
        # closeness = self.parameters['closeness']
        # print(state['closest_carcass'])


        # print(closest)
        # print("stroke")
        stroke(200, 200, 255)
        # print("nofill")
        noFill()
        # print("ellipse")
        # print(fish)
        # ellipse(fish.position[0], fish.position[1], closeness * 2, closeness * 2)
        # print("state")
        # if closest
        # line(fish.position[0], fish.position[1], closest[0], closest[1])
        # print(state)
        # if state['closecount'] != 0:
        
        # closest = state['closest_carcass']
        # print("closest")
        # print(closest)
        # print(closest[0])
        # if closest[0]!=0:

        #     line(fish.position[0], fish.position[1], closest[0], closest[1])

        # sys.exit()



class MoveTowardsCarcass(Behavior):
    
    print("mtc")

    def setup(self, fish, carcass, state):
       
        print("setup")

        global starttime
        global stamp
        global lap_seconds
        global steppe

        # print("[ begin move toward carcass 035 ]")
        # print(fish)
        # # print(state)

        if fish is carcass:
            # print(" fish is carcass ?")
            # print(fish)
            # print(carcass)
            # sys.exit()
            return


        if 'closecount' not in state:
            state['closecount'] = 0.0
        if 'center' not in state:
            state['center'] = [0.0, 0.0]

        closeness = fish.detection_range[0]

        # print("[ go ]")

        global eaters
        eaters = list([])

        for carcass in allcarcasses:
            global eaters
           
            # print("carcasses")

            carcass.position[0] = carcass.position[0]
            carcass.position[1] = carcass.position[1]

            if in_circle(center_x=fish.position[0], center_y=fish.position[1], radius=closeness, x=carcass.position[0], y=carcass.position[1]):

                el = fish
  
                eaters.append(el)
 
                distance_to_carcass = dist(carcass.position[0], carcass.position[1], fish.position[0], fish.position[1])
  

                if state['closecount'] == 0:

                    state['center'] = carcass.position
                    state['closecount'] =state['closecount']+ 1.0
                    state['closest_carcass'] = carcass.position

                    # # print(state)



                    if distance_to_carcass<self.parameters['threshold']:

                        #print("[ allosaur speed 0 ]")
                        # print(fish.energy)
                        self.eating_carcass = 1.0

#                         # print(fish.detection_range)

#                         # print("[ tailfat ]")

#                         # print(fish.tailfat)

#                         consumption_kg_per_day = fish.tailfat[0]
#                         consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                        fish.speed=0.0
                        fish.turnrate=0
                        
                        consumpt_step = fish.tailfat[0] * .18  #random.uniform(.009,.022)

                        # print(fish.energy)

                        fish.energy = fish.energy + consumpt_step

                    

                        # print("[ carcass energy ]")

                        # print(carcass.energy)# # print(
                        #print(carcass.energy)
                        carcass.energy = carcass.energy - consumpt_step
                        #print("carcass energy consumed")
                        #print(carcass.energy)
                        # sys.exit()

#                         fish.energy = fish.energy+consumpt_step
#                         # print(fish.energy)
#                         # print("[ carcass energy ]")
#                         # print(carcass.energy)
#                         carcass.energy = carcass.energy-consumpt_step
#                         # print(carcass.energy)
#                         # print("[ allosaur energy and detection range ]")
#                         # print(fish.energy)
#                         # print(fish.detection_range)

                    if distance_to_carcass<10:
                        # print("[ allosaur energy ]")
                        # print(fish.energy)
                        # self.eating_carcass = 1.0

                        # consumption_kg_per_day = fish.tailfat[0]
                        # consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                        fish.speed=0.0
                        fish.turnrate=0

                        # fish.energy = fish.energy+consumpt_step
                        # # print(fish.energy)
                        # # print("[ carcass energy ]")
                        # # print(carcass.energy)
                        # carcass.energy = carcass.energy-consumpt_step
                        # # print(carcass.energy)
                        # # print(fish.energy)
                        # sys.exit()



                    continue

                else:

                    # print("[ else okay ]")

                    state['center'][0] *= state['closecount']
                    state['center'][1] *= state['closecount']

                    state['center'] = [
                        state['center'][0] + carcass.position[0],
                        state['center'][1] + carcass.position[1]
                        ]

                    state['closecount'] += 1.0

                    state['center'][0] /= state['closecount']

                    state['center'][1] /= state['closecount']


                    state['closest_carcass'] = carcass.position

                    # print(state)

                    distance_to_carcass = dist(carcass.position[0], carcass.position[1], fish.position[0], fish.position[1])

                    if distance_to_carcass<self.parameters['threshold']:

                        self.eating_carcass = 1.0


                        # consumption_kg_per_day = fish.tailfat[0]
                        # consumpt_step =  random.uniform(0.08, 0.15) * consumption_kg_per_day
                        # # consumpt_step = consumption_kg_per_day

                        fish.speed=0.0
                        fish.turnrate=0

                        # fish.energy = fish.energy+consumpt_step
                        # # # print(fish.energy)
                        # # print("[ carcass energy ]")
                        # # print(carcass.energy)
                        # carcass.energy = carcass.energy-consumpt_step
                        # # print(carcass.energy)
                        # # print("[ allosaur energy and detection range ]")
                        # # print(fish.energy)
                        # # print(fish.detection_range)

                    if distance_to_carcass<10:
                        # # print("[ allosaur energy ]")
                        # print(fish.energy)
                        self.eating_carcass = 1.0

#                         consumption_kg_per_day = 27
#                         # consumpt_step =   consumption_kg_per_day
#                         consumpt_step =  random.uniform(0.05, 0.12) * consumption_kg_per_day

                        fish.speed=0.00001
                        fish.turnrate=0

#                         fish.energy = fish.energy+consumpt_step
#                         # print(fish.energy)
#                         # print("[ carcass energy ]")
#                         # print(carcass.energy)
#                         carcass.energy = carcass.energy-consumpt_step
#                         # print(carcass.energy)



                    continue
            else:
               
                # print("else 274")

                if random.random() > .995:

                    fish.direction = random.uniform(-3,3)
                    
                if (1 < steppe <90) or (180<steppe<270) or (320<steppe<365):

                    if len(allcarcasses) < 5:

                            # set max carcasses to 5?
                            # use the alaskan paper about wolf scavenging to support number of carcasses per sqkm in low yield season

                        
                        allcarcasses.append(Carcass())
                        
                    if len(allcarcasses) < 3:
                        if random.random() > .995:

                            # set max carcasses to 5?
                            # use the alaskan paper about wolf scavenging to support number of carcasses per sqkm in low yield season

                            allcarcasses.append(Carcass())



            lap = datetime.now() - stamp

            stamp = datetime.now().replace(microsecond=0)

            if lap > lap_seconds:

                steppe = steppe+1

                if len(allfishes)<30:

                    for fish in allfishes:
                        fish.direction = random.uniform(-3,3)
                    
                        if fish.energy<6900:

                            allfishes.remove(fish)

                        # print("\n step")
                        # print(fish)
                        # print(fish.energy)
                        mass = fish.energy/3.75

                        fish.energy = fish.energy - .161*(mass**.682)

                        # print(steppe)

                        # print("lap")

                        # print(lap)

                        # print("lap seconds")

                        # print(lap_seconds)

                        if random.random()<.02:

                            # print("[ population ]")

                            # print(len(allfishes))


                            xlr = Fish()
                        
                            # print("[ new allosaur ]")
                        
                            # print(xlr)

                            xlr.set_attributes(dominance=fish.dominance,
                                                        tailfat=fish.tailfat,
                                                            detection_range=fish.detection_range,
                                                        bite_force=fish.bite_force,
                                                        binocular_vision=fish.binocular_vision,
                                                        hearing=fish.hearing,
                                                        parent = fish.idd,
                                                        idd = "")


                            allfishes.append(xlr)

                            # print("[ reproduced! ]")


                if len(eaters)>0:
                    #print("eaters")

                    for fish in eaters:
                       
                        distance_to_carcass = dist(carcass.position[0], carcass.position[1], fish.position[0], fish.position[1])
                        
                        #print(distance_to_carcass)
                        #print(fish.position)
                        #print(carcass.position)
                        #print(closeness)
                       
                        if closeness<distance_to_carcass:
                            
                            if in_circle(center_x=fish.position[0], center_y=fish.position[1], radius=closeness, x=carcass.position[0], y=carcass.position[1]):
                           
                                consumpt_step = fish.tailfat[0] * .0042 #random.uniform(.009,.022)
    
                                fish.speed=0.0
    
                                fish.turnrate=0
                            
                                fish.energy = fish.energy + consumpt_step

                                carcass.energy = carcass.energy - consumpt_step
            
                        # # print(carcass.energy)

                        # # print(fish.energy)
                        # sys.exit()


                if steppe>365:

                    sys.exit()

                if len(allcarcasses)>=4:
                    if random.random()<0.000025:

                        allcarcasses.remove(allcarcasses[0])


    def apply(self, fish, state):

        if state['closecount'] == 0:

            return

        center = state['center']

        distance_to_center = dist(
            center[0], center[1],
            fish.position[0], fish.position[1]
            )

        # # print("[ distance to center of carcass ]")

        # # print(distance_to_center)
       
        # # print(fish.detection_range[0])

        closeness = fish.detection_range[0]

        if distance_to_center < closeness:
            # # print("in range!")
        # if distance_to_center < self.parameters['threshold']:
            angle_to_center = math.atan2(
                fish.position[1] - center[1],
                fish.position[0] - center[0]
                )
            # # print("[ angle to center ]")
            # # print(angle_to_center)
            fish.turnrate=random.uniform(0,0.0001)
            fish.speed=0.002
            # fish.direction=random.uniform(-2,2)

            fish.turnrate += (angle_to_center - fish.direction) / self.parameters['weight']
            # # print(fish.turnrate)
            # set fish direction to be toward center at as long as in sauropod carcass

            stroke(200, 200, 255)
            line(fish.position[0], fish.position[1], center[0], center[1])




    def draw(self, fish, state):
        closeness = fish.detection_range[0]
        # closeness = self.parameters['closeness']
        # closest = state['closest_carcass']
        stroke(200, 200, 255)
        noFill()
        ellipse(fish.position[0], fish.position[1], closeness * 2, closeness * 2)
        # line(fish.position[0], fish.position[1], closest[0], closest[1])

        # stroke(100, 255, 100)
        # noFill()
        #






# MoveTowardsCenterOfNearbyFish(closeness=50.0, threshold=25.0, speedfactor=100.0, weight=20.0)
class MoveTowardsCenterOfNearbyFish(Behavior):
    
    def setup(self, fish, otherfish, state):
        
        if fish is otherfish:

            return
        
        if 'closecount' not in state:
            state['closecount'] = 0.0
            
        if 'center' not in state:
            state['center'] = [0.0, 0.0]

        closeness = self.parameters['closeness']
        
        distance_to_otherfish = dist(
            otherfish.position[0], otherfish.position[1],
            fish.position[0], fish.position[1]
            )

        # if fish.eating_carcass==0:
        # 122
        if distance_to_otherfish < closeness:
            if state['closecount'] == 0:
                state['center'] = otherfish.position
                state['closecount'] += 0.0
            else:
                state['center'][0] *= state['closecount']
                state['center'][1] *= state['closecount']

                # state['center'][0] += otherfish.position[0]
                # state['center'][1] += otherfish.position[1]
                state['center'] = [
                    state['center'][0] + otherfish.position[0],
                    state['center'][1] + otherfish.position[1]
                    ]

                state['closecount'] += 0.0

                state['center'][0] /= state['closecount']
                state['center'][1] /= state['closecount']

    def apply(self, fish, state):
        
        if state['closecount'] == 0:
            
            return

        center = state['center']
        
        distance_to_center = dist(
            center[0], center[1],
            fish.position[0], fish.position[1]
            )

        if distance_to_center > self.parameters['threshold']:
            angle_to_center = math.atan2(
                fish.position[1] - center[1],
                fish.position[0] - center[0]
                )
            # fish.turnrate += (angle_to_center - fish.direction) / self.parameters['weight']
            # fish.speed += distance_to_center / self.parameters['speedfactor']


    def draw(self, fish, state):
        closeness = self.parameters['closeness']
        stroke(200, 200, 255)
        noFill()
        ellipse(fish.position[0], fish.position[1], closeness * 2, closeness * 2)



class TurnAwayFromClosestFish(Behavior):
    
    
    
    def setup(self, fish, otherfish, state):
        if fish is otherfish:
            return
        
        if 'closest_fish' not in state:
            state['closest_fish'] = None
        if 'distance_to_closest_fish' not in state:
            state['distance_to_closest_fish'] = 1000000

        distance_to_otherfish = dist(
            otherfish.position[0], otherfish.position[1],
            fish.position[0], fish.position[1]
            )
        print("distance to other fish")
        print(distance_to_otherfish)
        if distance_to_otherfish < state['distance_to_closest_fish']:
            state['distance_to_closest_fish'] = distance_to_otherfish
            state['closest_fish'] = otherfish

    def apply(self, fish, state):
        print("turn away")
        closest_fish = state['closest_fish']
        if closest_fish is None:
            return

        distance_to_closest_fish = state['distance_to_closest_fish']
        print("distance to closest fish")
        if distance_to_closest_fish < self.parameters['threshold']:
            if otherfish.dominance > fish.dominance:
                print("dominated!")
                angle_to_closest_fish = math.atan2(
                    fish.position[1] - closest_fish.position[1],
                    fish.position[0] - closest_fish.position[0]
                    )
                fish.turnrate -= (angle_to_closest_fish - fish.direction) / self.parameters['weight']
                fish.speed += self.parameters['speedfactor'] / distance_to_closest_fish

    def draw(self, fish, state):
        stroke(100, 255, 100)
        closest = state['closest_fish']
        # line(fish.position[0], fish.position[1], closest.position[0], closest.position[1])


class TurnToAverageDirection(Behavior):
    def setup(self, fish, otherfish, state):
        if fish is otherfish:
            return
        if 'average_direction' not in state:
            state['average_direction'] = 0.0
        if 'closecount_for_avg' not in state:
            state['closecount_for_avg'] = 0.0

        distance_to_otherfish = dist(
            otherfish.position[0], otherfish.position[1],
            fish.position[0], fish.position[1]
            )

        closeness = self.parameters['closeness']
        if distance_to_otherfish < closeness:
            if state['closecount_for_avg'] == 0:
                state['average_direction'] = otherfish.direction + random.uniform(0,0.6)
                state['closecount_for_avg'] += 1.0
            else:
                state['average_direction'] *= state['closecount_for_avg']
                state['average_direction'] += otherfish.direction  + random.uniform(0,0.6)
                state['closecount_for_avg'] += 1.0
                state['average_direction'] /= state['closecount_for_avg']

    def apply(self, fish, state):
        if state['closecount_for_avg'] == 0:
            return
        average_direction = state['average_direction']
        fish.turnrate += (average_direction - fish.direction) / self.parameters['weight']


class Swim(Behavior):


    print("swimming")


    def setup(self, fish, otherfish, state):
        global lap_seconds
        global steppe

        global starttime
        global stamp

        fish.speed = 1.7
        fish.turnrate = 0

        lap = datetime.now().replace(microsecond=0) - stamp
       
        if steppe>600:
            print("done complete, --0098")
           
            sys.exit()
        else:
            print("Running")
            print(steppe)
        # print(fish)
        # print(otherfish)
        # print(state)
        # print(fish.__dict__)
 

    def apply(self, fish, state):

        print("apply")
        # Move forward, but not too fast.
        if fish.speed > self.parameters['speedlimit']:
            fish.speed = self.parameters['speedlimit']
        fish.position[0] -= math.cos(fish.direction) * fish.speed
        fish.position[1] -= math.sin(fish.direction) * fish.speed

        # Turn, but not too fast.
        if fish.turnrate > self.parameters['turnratelimit']:
            fish.turnrate = self.parameters['turnratelimit']
        if fish.turnrate < -self.parameters['turnratelimit']:
            fish.turnrate = -self.parameters['turnratelimit']
        fish.direction += fish.turnrate


        # Fix the angles.
        if fish.direction > math.pi:
            fish.direction -= 2 * math.pi

        if fish.direction < -math.pi:
            fish.direction += 2 * math.pi
           
        print(" 01-24")









class WrapAroundWindowEdges(Behavior):
    def apply(self, fish, state):
        if fish.position[0] > width:
            fish.position[0] = 0
        if fish.position[0] < 0:
            fish.position[0] = width
        if fish.position[1] > height:
            fish.position[1] = 0
        if fish.position[1] < 0:
            fish.position[1] = height


def setup():
    # size(800, 400)
    size(700,700)
    number_of_fish = 12
    number_of_carcasses= 5
    number_of_prey = 16

    global behaviors

    behaviors = (
        MoveTowardsCarcass(closeness=75.0, threshold=75.0, speedfactor=100.0, weight=10.0),
        MoveTowardsCenterOfNearbyFish(closeness=0.5, threshold=.50, speedfactor=20.0, weight=20.0),
        MoveTowardsPrey(closeness=10, threshhold=.5, speedfactor=20.0, weight=20.0),
        TurnAwayFromClosestFish(threshold=0.3, speedfactor=4.0, weight=20.0),
        # TurnToAverageDirection(closeness=0.3, weight=6.0),
        Swim(speedlimit=2.0, turnratelimit=math.pi / 10.0),
        
        WrapAroundWindowEdges(),
        CarcassBehavior()



    )
    global prey_behaviors
    prey_behaviors = [ PreySwim(speedlimit=3.0, turnratelimit=math.pi / 10.0) ]



    global allfishes
    allfishes = []
    for i in xrange(0, number_of_fish):

        allfishes.append(Fish())
        # # print("[ allosaur created ]")


    global allcarcasses

    allcarcasses =[]

    for j in xrange(0, number_of_carcasses):


        # # print("[ carcass object created ]")
        allcarcasses.append(Carcass())
        # # print(Carcass().__dict__)


    global allprey

    allprey =[]

    for k in xrange(0,number_of_prey):

        # print"[ prey object created ]")

        allprey.append(Prey())
        print(Prey().__dict__)
        # sys.exit()
        


def draw():

    background(24)
    for fish in allfishes:
        fish.move()
        fish.draw()

    for carc in allcarcasses:
        carc.draw()
        
    for prey in allprey:
        prey.move()
        prey.draw()


class Fish(object):
    fishcolors = (
        color(255, 145, 8),
        color(219, 69, 79),
        color(255)
    )


    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        self.speed = 2.6
        self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0

        self.fishcolor = Fish.fishcolors[random.randrange(0, len(Fish.fishcolors))]

        self.energy = 7500
       
        self.parent = ""
        self.idd = uuid.uuid4()


        # 7500 energy = 2000 kg = 3.5x
        # tailfat determines how much energy above 7500 the animal can store
        # but the more energy stored, the more the animal costs, it gets more expensive as it gets fatter
        # and maybe slower also!

        li = ["extra_small","small","medium","big","extra_big"]


        advgs =  {"extra_small"    :[-.5,-.3]
                    ,"small"       :[-.3,-.1]
                    ,"medium"      :[-.1,.1]
                    , "big"        :[.1,.3]
                    , "extra_big"  :[.3,.5]}

        trts = ["dominance"
                , "detection_range"
                , "bite_force"
                , "binocular_vision"
                , "tailfat"
                , "hearing"]
        chc = []
        for j in trts:
            t = random.choice(li)
            s = [ random.uniform(advgs[t][0], advgs[t][1]), t ]
            chc.append(s)

        # # print(chc)

        self.dominance        = random.choice(chc)

        self.bite_force       = random.choice(chc)
        self.binocular_vision = random.choice(chc)
        self.hearing          = random.choice(chc)

        for k in trts:

            t = random.choice(li)
            phen = random.uniform(advgs[t][0], advgs[t][1])
            # # print(phen)
            # [ 50*(1+phen), phen , reproduce ]
            self.tailfat          = [38*(1+phen), phen, t]

            sn = random.choice(li)
            phen = random.uniform(advgs[sn][0], advgs[sn][1])
            
            # self.detection_range  = [round_to_multiple(50*(1+phen), 10), phen, sn]

            self.detection_range  = [50*(1+phen), phen, sn]
           
            snn = random.choice(li)

            phen = random.uniform(advgs[sn][0], advgs[sn][1])

            self.binocular_vision = [5*(1+phen), phen, snn]

        # # print("[ initialized allosaur ]")
        # # print(self.hearing)
        # # print(self.detection_range)



        # https://stackoverflow.com/questions/52285104/3d-scatterplots-in-python-with-hue-colormap-and-legend

        # z axis (up and down) should be magnitude of trait ? up to 100% the highest it can be?
        # i don't know how to organize this yet
        # x must be the -1.5 to +1.5 magnitude

        # i will do ectotherm, mesotherm, endotherm


        # bears gain 180 kg of fat during hyperphagia before hibernation
        # how much fat is stored in the body, how much in the tail? use boht, one fills up then the other, first body then tail
        # it must be a hereditary thing with a variable ; genotype aa = between 4 and 6, genotype bb is between 4.3 and 6.4
        # and this variable is also variable to replicate selective pressure

    def set_attributes(self, dominance,tailfat, hearing, detection_range, bite_force, binocular_vision, parent, idd):
        reprod = {  "extra_small":["extra_small","small","small"]
                  , "small":      ["extra_small","small","medium"]
                  , "medium":     ["small","medium","big"]
                  , "big":        ["medium","big","extra_big"]
                  , "extra_big":  ["big","big","extra_big"] }

        # print("[ setting traits: ]")

        traits = [(self.dominance, "dominance")
                , (self.detection_range,"detection_range")
                , (self.bite_force, "bite_force")
                , (self.binocular_vision,"binocular_vision")
                , (self.tailfat,"tailfat")
                , (self.hearing,"hearing")]


        # print(traits)
        self.parent = parent
        self.idd = uuid.uuid4()
       


        # labels "big" and factors .5
        adaptations       = {"dominance":dominance
                             , "detection_range":detection_range
                             ,"tailfat":tailfat
                             , "bite_force":bite_force
                             , "binocular_vision":binocular_vision
                             ,"hearing":hearing}

        # advantage_factors = {"extra_small" :[-.167,0]
        #                      ,"small"      :[0,.167]
        #                      ,"medium"     :[0,.5]
        #                      , "big"       :[.334,.5]
        #                      , "extra_big" :[.5,5.167]}

        advantage_factors =  {"extra_small" :[-.7,-.35]
                              ,"small"      :[-.35,-.1]
                              ,"medium"     :[-.1,.1]
                              , "big"        :[.1,.35]
                              , "extra_big"  :[.35,.7]}

        # print("[ generating phenotype ]")
       
        items_probability = [0.1, 0.8, 0.1]


        for tr,ait in traits:

            if ait == "tailfat":

                # print("[ --tailfat-- ]")

                # # print(self.tailfat)

                # # print(self.tailfat[0])

                # # print("[ --choices-- ]")

                choices = reprod[self.tailfat[2]]

                # print(choices)

                shoyces = sum([[element] * int(weight * 100)for element, weight in zip(choices, items_probability)], [])
               
                reproduce = random.choice(shoyces)

                # print(reproduce)

                phen = random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] )

                # # print(phen)

                # self.tailfat affects how much food the animal can eat/store per day when on a carcass

                self.tailfat = [ 38*(1+phen), phen , reproduce ]

                # # print(self.tailfat)

                # # print("\n")

                # # # print(self.detection_range)

            if ait == "hearing":

                # print("[ --hearing-- ]")

                # # print(self.hearing)
                # self.hearing = self.hearing

                # # print("[ --choices-- ]")

                choices = reprod[self.hearing[1]]

                # print(choices)
                items_probability = [0.1, 0.8, 0.1]

                shoyces = sum([[element] * int(weight * 100)for element, weight in zip(choices, items_probability)], [])
               
                reproduce = random.choice(shoyces)

                # # print("[ --hearing-- ]")

                # # print(hearing)

                self.hearing =  [ random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] ) , reproduce ]

                # # print(self.hearing)

            if ait == "dominance":

                # print("[ --dominance-- ]")

                # # print(self.dominance)
                # self.dominance = self.dominance[0]

                # # print(self.dominance[0])

                # # print("[ --choices-- ]")

                choices = reprod[self.dominance[1]]
                # # print(sys.version)

                # print(choices)
                items_probability = [0.1, 0.8, 0.1]
               
               
               
                shoyces = sum([[element] * int(weight * 100)for element, weight in zip(choices, items_probability)], [])
               
                reproduce = random.choice(shoyces)
                # print(reproduce)

                # reproduce = random.choices(population=choices,weights=[0.1,0.8,0.1],k=1)[0]

                # print("[ --reproduce-- ]")

                # # print(reproduce)

                # # print("[ advantage factors ]")

                # # print(advantage_factors[reproduce][0])
                # # print(advantage_factors[reproduce][1])

                phen = random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] )

                # # print(reproduce)

                # # print(phen)

                self.dominance =  [ phen , reproduce ]

                # # print(self.dominance)

            if ait=="detection_range":

                # print("[ --detection_range-- ]")

                # # print(self.detection_range)

                # # print("[ --choices-- ]")

                choices = reprod[self.detection_range[2]]
                items_probability = [0.1, 0.8, 0.1]

                # print(choices)
               
                shoyces = sum([[element] * int(weight * 100)for element, weight in zip(choices, items_probability)], [])
               
                reproduce = random.choice(shoyces)
               
                # print(reproduce)
         

                # # print("[ --detection phen-- ]")

                # # # print(reproduce)

                phen = random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] )

                # # print(phen)

                self.detection_range =  [ 50*(1+phen), phen , reproduce ]

                # # print(self.detection_range)

                # # print("\n")

                # # # print(self.detection_range)

            if ait=="bite_force":

                # print("[ --bite_force-- ]")

                # self.bite_force = self.bite_force[0]

                # # print(self.bite_force)

                # # print("[ --choices-- ]")

                choices = reprod[self.bite_force[1]]
               
                items_probability = [0.1, 0.8, 0.1]

                # print(choices)
               
                shoyces = sum([[element] * int(weight * 100)for element, weight in zip(choices, items_probability)], [])
               
                reproduce = random.choice(shoyces)
                # print(reproduce)

                self.bite_force = [ random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] ) , reproduce ]

                # # # print(self.bite_force)

            if ait=="binocular_vision":

                # print("[ --binocular_vision-- ]")

                # self.binocular_vision = self.binocular_vision[0]

                # # print(self.binocular_vision)

                # print("[ --choices-- ]")

                choices = reprod[self.binocular_vision[2]]

                # print(choices)

                shoyces = sum([[element] * int(weight * 100)for element, weight in zip(choices, items_probability)], [])
               
                reproduce = random.choice(shoyces)

                # print("[ --reproduce-- ]")

                # # print(reproduce)

                phen = random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] )

                self.binocular_vision = [ 5*(1+phen) , phen ,reproduce ]

                # # print(self.binocular_vision)



    def move(self):

        global allfishes, behaviors

        global allcarcasses, carcass_behaviors
        
        global allprey, prey_behaviors

        global steppe

        state = {}

        # print("[ move step ]")
        # # print(steppe)


        for fish in allfishes:

            now = datetime.now()

            now = now.strftime("%H:%M:%S,%f")

            # # print(vars(fish))

            dct = [{"dominance":fish.dominance # affects how other individuals react at carcass sites
                    , "detection_range":fish.detection_range # affects distance they can smell dead bodies
                    ,"tailfat":fish.tailfat # affects consumption rate * 27 or 1.5x of fmr -- i want it to also be how much ta?x free energy they can store
                    , "bite_force":fish.bite_force # affects predator success because it is power
                    , "binocular_vision":fish.binocular_vision # binocular_vision affects predator detection radius
                    ,"hearing":fish.hearing # hearing affects predator success b/c stealth
                    ,"id" : fish #fish object id
                    ,"energy":fish.energy #how much energy the agent has
                    ,"timestamp":now
                    ,"allosaur_population":str(len(allfishes))
                    ,"sauropod_carcasses":str(len(allcarcasses))
                    ,"steppe":steppe
                    ,"parent":fish.parent
                    ,"idd":fish.idd}]

            with open("big_boned_data.csv", "a") as csvfile:
                # # print("[ writing data... ]")

                writer = csv.DictWriter(csvfile,fieldnames=["dominance"
                                                            ,"detection_range"
                                                            ,"tailfat"
                                                            ,"bite_force"
                                                            ,"binocular_vision"
                                                            ,"hearing"
                                                            ,"id"
                                                            ,"energy"
                                                            ,"timestamp"
                                                            ,"allosaur_population"
                                                            ,"sauropod_carcasses"
                                                            ,"steppe"
                                                            ,"parent"
                                                            ,"idd"])

                # writer.writeheader()



                writer.writerows(dct)


            if fish.energy<6900:

                allfishes.remove(fish)
               
            if len(allfishes)>30:
                # allfishes = allfishes.pop(0)
                allfishes.remove(allfishes[0])




        for carc in allcarcasses:
            if carc.energy<carc.energy*.2:
                allcarcasses.remove(carc)

        for fish in allfishes:
            print(fish)
            for behavior in behaviors:
                print(behavior)
                behavior.setup(self, fish, state)
                print("setup done")

        for behavior in behaviors:
            print("new beh")
            print(behavior)
            
            behavior.apply(self, state)
            print("new apply")
            behavior.draw(self, state)
        # output.close()

    def draw(self):
        pushMatrix()

        translate(*self.position)
        rotate(self.direction)

        stroke(self.fishcolor)
        noFill()
        lengt = self.energy/7500
        lengt = round(lengt,2)
        text(str(lengt),25,22)
        # print("drawing line 09876")
        lengt = lengt*20
        line(0,22, lengt,22)
        # print("drawing line")
       
 

        # if lengt >1:
            # stroke("#FF007F")
            # line(20,0,lengt*20,0)

        # lower jaw
        line(0.28, 16.36, 7.16, 15.40)
        line(7.16, 15.40, 8.52, 14.68)
        line(8.52, 14.68, 20.16, 12.56)

        line(20.16, 12.56, 20.92, 13.00)
        line(20.92, 13.00, 12.20, 17.8)
        line(12.20, 17.8, 7.48, 17.36)
        line(7.48, 17.36, .76, 17.4)
        line(.76, 17.4, 0.112, 16.36)

        # skull
        line(0, 12.64, 0.1, 7.48)
        line(0.1, 7.48, 12.6, 4.20)
        line(12.6, 4.20, 13.06, 5.52)
        line(13.06, 5.5, 15.96, 5.6)

        line(0, 12.64, 11.04, 10.96)
        line(11.04, 10.96, 13.8, 12.24)

        line(15.96, 5.6, 16.64, 5.12)
        line(16.64, 5.12, 19.42, 9.76)
        line(19.42, 9.76, 18.48, 9.76)
        line(18.48, 9.76, 18.40, 10.84)
        line(18.40, 10.84, 19.44, 12.04)

        # fenestrae and orbit
        # nose
        line(1.52, 7.84, 1.84, 7.28)
        line(1.84, 7.28, 4.16, 6.72)
        line(4.16, 6.72, 4.24, 7.88)
        line(4.24, 7.88, 1.75, 8.28)

        # aofe
        line(5.52, 7.6, 6.24, 7.8)
        line(6.24, 7.8, 8.64, 6.16)
        line(8.64, 6.16, 10.56, 8.20)
        line(10.56, 8.20, 10.76, 8.28)
        line(10.76, 8.28, 9.24, 9.52)
        line(9.24, 9.52, 6.726, 8.32)

        # orbit
        # line(11.68, 7.0, 6.24, 7.8)
        # line(6.24, 7.8, 14.52, 6.32)
        line(14.52, 6.32, 13.24, 10.34)
        # line(13.24, 10.34, 11.68, 7.0)


        # line(16.24, 6.8, 17.44, 7.68)
        line(17.44, 7.68, 17.48, 10.56)
        line(17.48, 10.56, 16.04, 11.6)
        # line(17.48, 10.56, 14.64, 10.56)
        # line(14.64, 10.56, 16.24, 6.8)






        popMatrix()

class Carcass(object):
    carcass_colors = (
                      color(138, 43, 226),
                      color(122, 197, 205),
                      color(124,252,0)
                      )

    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        # # print(self.position)
        self.speed = 0
        # self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0
        self.energy = random.uniform(10000,40000)
        self.eating_carcass = 0

        self.carcasscolor = Carcass.carcass_colors[random.randrange(0, len(Carcass.carcass_colors))]


    def set_attributes(self, energy, position):

        self.energy = energy
        self.position = position
        
        
    def move(self):
        # # print("[ carc moving ]")

        global allcarcasses, carcass_behaviors
        global allfishes, behaviors

        state = {}

        for carc in allcarcasses:
            for carcass_behavior in carcass_behaviors:
                carcass_behavior.setup(self, carc, state)

        for carcass_behavior in carcass_behaviors:
            carcass_behavior.apply(self, state)

    def draw(self):
        pushMatrix()

        translate(*self.position)
        # rotate(self.direction)

        stroke(self.carcasscolor)
        noFill()

        lengt = self.energy/40000

        lengt = round(lengt,2)
        text(str(lengt), -25,22)
        text(str(self.energy), 0,22)

        lengt = lengt*20
        line(0,0, lengt,0)

        # arc(0,0, 15,0, -5,PI*2)

        line(11.4,-33.0,-6.6,-20.4)

        line(14.0,-32.6,11.4,-33.0)
        line(23.0,-45.2,14.0,-32.6)
        line(25.0,-64.8,23.0,-45.2)
        line(31.0,-70.0,25.0,-64.8)
        line(33.2,-67.6,31.0,-70.0)
        line(27.6,-61.6,33.2,-67.6)
        line(27.0,-42.6,27.6,-61.6)
        line(19.2,-24.4,27.0,-42.6)
        line(16.0,-15.6,19.2,-24.4)
        line(16.2,-5.8,16.0,-15.6)
        line(16.2,-5.8,16.2,-5.8)
        line(10.4,-4.4,16.2,-5.8)
        line(8.8,-14.0,10.4,-4.4)
        line(6.6,-13.8,8.8,-14.0)
        line(7.8,-5.2,6.6,-13.8)
        line(2.6,-5.0,7.8,-5.2)
        line(1.6,-13.4,2.6,-5.0)
        line(-0.8,-12.8,1.6,-13.4)
        line(-2.0,-8.6,-0.8,-12.8)
        line(-1.2,-5.8,-2.0,-8.6)
        line(10.4,-4.4,-1.2,-5.8)
        line(8.8,-14.0,10.4,-4.4)
        line(6.6,-13.8,8.8,-14.0)
        line(7.8,-5.2,6.6,-13.8)
        line(2.6,-5.0,7.8,-5.2)
        line(1.6,-13.4,2.6,-5.0)
        line(-0.8,-12.8,1.6,-13.4)
        line(-2.0,-8.6,-0.8,-12.8)
        line(-1.2,-5.8,-2.0,-8.6)
        line(-5.6,-5.0,-1.2,-5.8)
        line(-5.2,-14.8,-5.6,-5.0)
        line(-17.4,-17.2,-5.2,-14.8)
        line(-23.8,-14.8,-17.4,-17.2)
        line(-14.2,-18.6,-23.8,-14.8)
        line(-14.2,-18.6,-14.2,-18.6)
        line(-6.6,-20.4,-14.2,-18.6)







        popMatrix()


class Prey(object):
    prey_colors = (
                      color(138, 43, 226),
                      color(122, 197, 205),
                      color(124,252,0)
                      )


    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        # # printself.position)
        self.speed = 2.7
        self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0.5
        self.energy = 2000 # prey energy must be calories available, not life energy, because prey won't metabolize

        self.preycolor = Prey.prey_colors[random.randrange(0, len(Carcass.carcass_colors))]



    def set_attributes(self, speed):
        # print"[ prey slowed down ]")

        self.speed = speed






    def move(self):

        # print("[ prey move ]")

        global allfishes, behaviors

        global allcarcasses, carcass_behaviors

        global allprey, prey_behaviors

        state = {}

        # print"[ prey state ]")

        # printallprey)

        for prey in allprey:
            # print"\n[ preys ]")
            # printprey)
            # printprey_behaviors)

            for prey_behavior in prey_behaviors:
                # printprey_behavior.__dict__)
                # print"[ prey behaviors 1xx ]")

                prey_behavior.setup(self, state)
                prey_behavior.draw(self,state)

        for prey_behavior in prey_behaviors:
            prey_behavior.apply(self,state)
            prey_behavior.draw(self, state)


    def draw(self):
        print("draw 1715")
        # sys.exit()
        pushMatrix()
        # print"draw 1636")
        print(self.preycolor)

        translate(*self.position)
        # rotate(self.direction)

        stroke(self.preycolor)
        noFill()

        print("[ drawing from scratch ]")

        lengt = self.energy/2000
        # printlengt)
        lengt = lengt*20
        # printlengt)
        line(0,0, lengt,0)
        # print"line")

        # arc(0,0, 15,0, -5,PI*2)

        line(3.5,8.366,1.7,9.566)
        line(4.1,7.4,3.5,8.366)
        line(4.3,8.4,4.1,7.4)
        line(4.866,7.666,4.3,8.4)
        line(5.2,8.6,4.866,7.666)
        line(5.8,7.666,5.2,8.6)
        line(6.2,8.166,5.8,7.666)
        line(6.6,7.6,6.2,8.166)
        line(7,8.1,6.6,7.6)
        line(7.2,7.7,7,8.1)
        line(7.4,6.866,7.2,7.7)
        line(8.0,6.6,7.4,6.866)
        line(8.2,5.7,8.0,6.6)
        line(9,5.7,8.2,5.7)
        line(9.166,4.066,9,5.7)
        line(10.5,4.7,9.166,4.066)
        line(11.1,3.2,10.5,4.7)
        line(12.46,4.2,11.1,3.2)
        line(14.4,2.966,12.46,4.2)
        line(14.96,3.9,14.4,2.966)
        line(16.93,2.9,14.96,3.9)
        line(17.,3.966,16.93,2.9)
        line(19.4,2.4,17.,3.966)
        line(19.9,4.2,19.4,2.4)
        line(21.76,3.6,19.9,4.2)
        line(22.26,4.8,21.76,3.6)
        line(25.26,4.7,22.26,4.8)
        line(24.,5.966,25.26,4.7)
        line(26.7,5.566,24.,5.966)
        line(26.46,7.0,26.7,5.566)
        line(27.56,6.866,26.46,7.0)
        line(27.6,7.8,27.56,6.866)
        line(28.7,7.7,27.6,7.8)
        line(28.,8.766,28.7,7.7)
        line(29.53,8.966,28.,8.766)
        line(31.23,6.2,29.53,8.966)
        line(30.16,8.566,31.23,6.2)
        line(32.76,6.666,30.16,8.566)
        line(30.73,9.3,32.76,6.666)
        line(33.16,8.666,30.73,9.3)
        line(30.86,9.3,33.16,8.666)
        line(25.5,9.2,30.86,9.3)
        line(21.56,9.0,25.5,9.2)
        line(17.7,9.966,21.56,9.0)
        line(17.26,11.36,17.7,9.966)
        line(18.3,13.53,17.26,11.36)
        line(18.13,14.7,18.3,13.53)
        line(16.83,14.9,18.13,14.7)
        line(17.23,13.73,16.83,14.9)
        line(15.73,11.7,17.23,13.73)
        line(15.5,14.6,15.73,11.7)
        line(13.96,14.8,15.5,14.6)
        line(14.46,13.66,13.96,14.8)
        line(13.83,11.8,14.46,13.66)
        line(11.86,11.86,13.83,11.8)
        line(12.03,14.83,11.86,11.86)
        line(10.9,14.76,12.03,14.83)
        line(11.2,13.96,10.9,14.76)
        line(10.93,12.26,11.2,13.96)
        line(9.666,14.83,10.93,12.26)
        line(8.666,14.76,9.666,14.83)
        line(8.966,13.9,8.666,14.76)
        line(9.6,12.43,8.966,13.9)
        line(9.7,11.7,9.6,12.43)
        line(8.566,10.5,9.7,11.7)
        line(5.7,10.2,8.566,10.5)
        line(4.7,9.7,5.7,10.2)
        line(3.166,9.7,4.7,9.7)
        line(1.7,9.5,3.166,9.7)


        popMatrix()
        print("drawn!")
        print(self.__dict__)
        # sys.exit()

setup()
