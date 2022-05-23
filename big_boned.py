import math
import random
import time

# add_library("VideoExport")


width = 800
height= 400

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
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, carcass, fish, state):
        pass

    def apply(self, carcass, state):
        pass

    def draw(self, carcass, state):
        pass

# MoveTowardsCenterOfNearbyFish(closeness=50.0, threshold=25.0, speedfactor=100.0, weight=20.0)


class MoveTowardsCarcass(Behavior):
    def setup(self, fish, carcass, state):

        if fish is carcass:
            return



        if 'closecount' not in state:
            state['closecount'] = 0.0
        if 'center' not in state:
            state['center'] = [0.0, 0.0]

        # closeness = self.parameters['closeness']
        # print("[ this is original closeness: ] ")
        # print(self.parameters['closeness'])
        # print("[ this is fish.detection_range closeness: ]")

        closeness = fish.detection_range[0]

        # print(fish.detection_range)

        for carcass in allcarcasses:
            carcass.position[0] = carcass.position[0]
            carcass.position[1] = carcass.position[1]
            if in_circle(center_x=fish.position[0], center_y=fish.position[1], radius=closeness, x=carcass.position[0], y=carcass.position[1]):

                print("\n[ carcass in detected! closeness: ]")
                print(closeness)

                print("[ carcass position ]")

                print(carcass.position)
                print("[ carcass energy ]")
                print(carcass.energy)
                distance_to_carcass = dist(carcass.position[0], carcass.position[1], fish.position[0], fish.position[1])
                print("[ distance to carcass ]")
                print(distance_to_carcass)
                print("[ --dominance-- ]")
                print(fish.dominance)
                print("[ --binocular_vision-- ]")
                print(fish.binocular_vision)


                if state['closecount'] == 0:

                    state['center'] = carcass.position
                    state['closecount'] =state['closecount']+ 1.0
                    state['closest_carcass'] = carcass.position

                    print(state)



                    if distance_to_carcass<self.parameters['threshold']:

                        print("[ allosaur energy ]")
                        print(fish.energy)
                        self.eating_carcass = 1.0

                        consumption_kg_per_day = 27
                        consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                        fish.speed=0.5
                        fish.turnrate=0

                        fish.energy = fish.energy+consumpt_step
                        print(fish.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)
                        print("[ allosar energy and detection range ]")
                        print(fish.energy)
                        print(fish.detection_range)

                    if distance_to_carcass<10:
                        print("[ allosaur energy ]")
                        print(fish.energy)
                        self.eating_carcass = 1.0

                        consumption_kg_per_day = 27
                        consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                        fish.speed=0.0
                        fish.turnrate=0

                        fish.energy = fish.energy+consumpt_step
                        print(fish.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)



                    continue

                else:

                    state['center'][0] *= state['closecount']
                    state['center'][1] *= state['closecount']

                    state['center'] = [
                        state['center'][0] + carcass.position[0],
                        state['center'][1] + carcass.position[1]
                        ]

                    state['closecount'] += 1.0

                    state['center'][0] /= state['closecount']
                    state['center'][1] /= state['closecount']

                    # print("[ state champions ]")
                    state['closest_carcass'] = carcass.position
                    print(state)
                    distance_to_carcass = dist(carcass.position[0], carcass.position[1], fish.position[0], fish.position[1])
                    if distance_to_carcass<self.parameters['threshold']:
                        # print("[ allosaur energy ]")
                        # print(fish.energy)
                        self.eating_carcass = 1.0


                        consumption_kg_per_day = 27
                        consumpt_step =  random.uniform(0.08, 0.15) * consumption_kg_per_day
                        # consumpt_step = consumption_kg_per_day

                        fish.speed=0.5
                        fish.turnrate=0

                        fish.energy = fish.energy+consumpt_step
                        # print(fish.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)
                        print("[ allosar energy and detection range ]")
                        print(fish.energy)
                        print(fish.detection_range)

                    if distance_to_carcass<10:
                        # print("[ allosaur energy ]")
                        # print(fish.energy)
                        self.eating_carcass = 1.0

                        consumption_kg_per_day = 27
                        # consumpt_step =   consumption_kg_per_day
                        consumpt_step =  random.uniform(0.05, 0.12) * consumption_kg_per_day

                        fish.speed=0.00001
                        fish.turnrate=0

                        fish.energy = fish.energy+consumpt_step
                        print(fish.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)



                    continue
            else:

                if random.random() > .995:

                    fish.direction = random.uniform(-3,3)

                if random.random()<0.00003:

                    allcarcasses.append(Carcass())


                if random.random()<0.00009:

                    print("[ reproducing... ]")

                    xlr = Fish()
                    print(xlr)
                    xlr.set_attributes(dominance=fish.dominance,
                                                           # tailfat=fish.tailfat,
                                                           detection_range=fish.detection_range,
                                                           bite_force=fish.bite_force,
                                                           binocular_vision=fish.binocular_vision,
                                                           hearing=fish.hearing,
                                                           tailfat=fish.tailfat )

                    print(xlr)

                    allfishes.append(xlr)

                    print("[ reproduced successfully ]")


                    # self.reproduce = 0



    def apply(self, fish, state):

        if state['closecount'] == 0:

            return

        center = state['center']

        distance_to_center = dist(
            center[0], center[1],
            fish.position[0], fish.position[1]
            )

        print("[ distance to center of carcass ]")

        print(distance_to_center)

        closeness = fish.detection_range[0]

        if distance_to_center < closeness:

        # if distance_to_center < self.parameters['threshold']:
            angle_to_center = math.atan2(
                fish.position[1] - center[1],
                fish.position[0] - center[0]
                )
            # print("[ angle to center ]")
            # print(angle_to_center)
            fish.turnrate=random.uniform(0,0.0001)
            fish.speed=0.002
            # fish.direction=random.uniform(-2,2)

            fish.turnrate += (angle_to_center - fish.direction) / self.parameters['weight']
            # print(fish.turnrate)
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
            # print("[ otherfish ]")
            # print(otherfish)
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

        if distance_to_otherfish < state['distance_to_closest_fish']:
            state['distance_to_closest_fish'] = distance_to_otherfish
            state['closest_fish'] = otherfish

    def apply(self, fish, state):
        closest_fish = state['closest_fish']
        if closest_fish is None:
            return

        distance_to_closest_fish = state['distance_to_closest_fish']
        if distance_to_closest_fish < self.parameters['threshold']:
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
    def setup(self, fish, otherfish, state):
        fish.speed = 2.7
        fish.turnrate = 0
        # 13 is the daily expenditure, but needs to be dynamic based on the dinosaur's mass
        # i bet the fat storage ability will limit their mass , and there will be a plateau

        daily_meat =(random.uniform(0.05, 0.12) * 13)
        # 13 kg per day baseline reptile
        if fish.energy>7500:
            mass = fish.energy/3.75
            fish.energy = fish.energy - (.0159*(mass**.92))
        else:
            fish.energy = fish.energy - daily_meat
        # put the energy burn here

    def apply(self, fish, state):
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
    size(800, 400)

    number_of_fish = 5
    number_of_carcasses= 2

    global behaviors

    behaviors = (
        MoveTowardsCarcass(closeness=75.0, threshold=75.0, speedfactor=100.0, weight=10.0),
        MoveTowardsCenterOfNearbyFish(closeness=0.5, threshold=.50, speedfactor=20.0, weight=20.0),
        # TurnAwayFromClosestFish(threshold=0.3, speedfactor=4.0, weight=20.0),
        # TurnToAverageDirection(closeness=0.3, weight=6.0),
        Swim(speedlimit=3.0, turnratelimit=math.pi / 10.0),
        WrapAroundWindowEdges(),
        CarcassBehavior()


    )


    global allfishes
    allfishes = []
    for i in xrange(0, number_of_fish):

        allfishes.append(Fish())


    global allcarcasses

    allcarcasses =[]

    for j in xrange(0, number_of_carcasses):


        print("[ carcass object created ]")
        allcarcasses.append(Carcass())
        print(Carcass().__dict__)




def draw():

    background(24)
    for fish in allfishes:
        fish.move()
        fish.draw()

    for carc in allcarcasses:
        carc.draw()


class Fish(object):
    fishcolors = (
        color(255, 145, 8),
        color(219, 69, 79),
        color(255)
    )

    # adaptation_factors = {"small":[0,0.167], "medium":[0.167,.334], "big":[.334,.5]}




    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        self.speed = 2.6
        self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0

        self.fishcolor = Fish.fishcolors[random.randrange(0, len(Fish.fishcolors))]

        self.energy = 7500
        # 7500 energy = 2000 kg = 3.5x
        # tailfat determines how much energy above 7500 the animal can store
        # but the more energy stored, the more the animal costs, it gets more expensive as it gets fatter
        # and maybe slower also!


        self.dominance        = [0.0,"medium"]
        self.tailfat          = [0.0,"medium"]
        self.detection_range  = [60.0,"medium"]
        self.bite_force       = [0.0,"medium"]
        self.binocular_vision = [0.0,"medium"]
        self.hearing          = [0.0,"medium"]

        # https://stackoverflow.com/questions/52285104/3d-scatterplots-in-python-with-hue-colormap-and-legend

        # z axis (up and down) should be magnitude of trait ? up to 100% the highest it can be?
        # i don't know how to organize this yet
        # x must be the -1.5 to +1.5 magnitude

        # i will do ectotherm, mesotherm, endotherm


        # bears gain 180 kg of fat during hyperphagia before hibernation
        # how much fat is stored in the body, how much in the tail? use boht, one fills up then the other, first body then tail
        # it must be a hereditary thing with a variable ; genotype aa = between 4 and 6, genotype bb is between 4.3 and 6.4
        # and this variable is also variable to replicate selective pressure

    def set_attributes(self, dominance,tailfat, hearing, detection_range, bite_force, binocular_vision):

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
                ,(self.hearing,"hearing")]


        # print(traits)


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

        advantage_factors =  {"extra_small" :[-.5,-.3]
                              ,"small"      :[-.3,-.1]
                              ,"medium"     :[-.1,.1]
                             , "big"        :[.1,.3]
                             , "extra_big"  :[.3,.5]}

        print("[ generating phenotype ]")


        for tr,ait in traits:



            # print(tr)
            # print(ait)

            if ait == "dominance":

                print("[ --dominance-- ]")

                print(self.dominance)

                print("[ --choices-- ]")

                choices = reprod[self.dominance[1]]

                print(choices)

                reproduce = random.choice(choices)

                print("[ --reproduce-- ]")

                print(reproduce)

                self.dominance =  [ random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] ) , reproduce ]

                print(self.dominance)

            if ait=="detection_range":

                # print("[ --detection_range-- ]")

                # print(self.detection_range)

                # print("[ --choices-- ]")

                choices = reprod[self.detection_range[1]]

                # print(choices)

                reproduce = random.choice(choices)

                print("[ --detection phen-- ]")

                # print(reproduce)

                phen = random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] )

                print(phen)

                self.detection_range = [ 60*(1+phen), advantage_factors[reproduce][1] , reproduce ]

                print(self.detection_range)

                print("\n")

                # print(self.detection_range)

            if ait=="bite_force":

                # print("[ --bite_force-- ]")

                # print(self.bite_force)

                # print("[ --choices-- ]")

                choices = reprod[self.bite_force[1]]

                # print(choices)

                reproduce = random.choice(choices)

                # print("[ --reproduce-- ]")

                # print(reproduce)

                self.bite_force = [ random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] ) , reproduce ]

                # print(self.bite_force)

            if ait=="binocular_vision":

                # print("[ --binocular_vision-- ]")

                # print(self.binocular_vision)

                # print("[ --choices-- ]")

                choices = reprod[self.binocular_vision[1]]

                # print(choices)

                reproduce = random.choice(choices)

                # print("[ --reproduce-- ]")

                # print(reproduce)

                self.binocular_vision = [ random.uniform( advantage_factors[reproduce][0], advantage_factors[reproduce][1] ) , reproduce ]

                # print(self.binocular_vision)



    def move(self):

        global allfishes, behaviors

        global allcarcasses, carcass_behaviors

        state = {}


        for fish in allfishes:
            if fish.energy<3:
                allfishes.remove(fish)

        for carc in allcarcasses:
            if carc.energy<100:
                allcarcasses.remove(carc)

        for fish in allfishes:
            for behavior in behaviors:
                behavior.setup(self, fish, state)

        for behavior in behaviors:
            behavior.apply(self, state)
            behavior.draw(self, state)

    def draw(self):
        pushMatrix()

        translate(*self.position)
        rotate(self.direction)

        stroke(self.fishcolor)
        noFill()
        lengt = self.energy/7500

        lengt = lengt*20
        line(0,22, lengt,22)

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
        # print(self.position)
        self.speed = 0
        # self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0
        self.energy = 40000
        self.eating_carcass = 0

        self.carcasscolor = Carcass.carcass_colors[random.randrange(0, len(Carcass.carcass_colors))]
        
    def decay_equation(n):
        
        rep = ( -87/(1+ math.exp(-0.208506*n + 6.1256) ) + 100 )

        # print(rep)

        =return rep/100

    def move(self):
        # print("[ carc moving ]")

        global allcarcasses, carcass_behaviors
        global allfishes, behaviors

        state = {}
        
        self.energy = self.energy

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

        lengt = self.energy/25000

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


setup()
