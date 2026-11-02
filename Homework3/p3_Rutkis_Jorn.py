#problem 3
"""Predator-Prey Simulation
   Five classes are defined: animal, predator, prey, human, and island
   where island is where the simulation is taking place,
   i.e. where the predator, human, and prey interact (live).
   A list of predators and prey are instantiated, and
   then their breeding, eating, and dying are simulted.
   Humans also breed, and die, however, instead of eating prey, 
   they hunt predators.
"""
import random
import time
#import pylab  # replaced by:
import matplotlib.pyplot as plt


class Island (object):
    """Island
       n X n grid where zero value indicates not occupied."""
    def __init__(self, n: int, prey_count: int=0, predator_count: int=0, count_humans: int=0) -> None: #added count_humans to init
        '''Initialize grid to all 0's, then fill with animals
        '''
        # print(n,prey_count,predator_count, count_humans)
        self.grid_size = n
        self.grid = []
        for i in range(n):
            row = [0]*n    # row is a list of n zeros
            self.grid.append(row)
        self.init_animals(prey_count,predator_count, count_humans)

    def init_animals(self,prey_count: int, predator_count: int, count_humans: int) -> None: #added count_humans to init_animals
        ''' Put some initial animals on the island
        '''
        count = 0
        # while loop continues until prey_count unoccupied positions are found
        while count < prey_count:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if not self.animal(x,y):
                new_prey=Prey(island=self,x=x,y=y)
                count += 1
                self.register(new_prey)
        count = 0
        # same while loop but for predator_count
        while count < predator_count:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if not self.animal(x,y):
                new_predator=Predator(island=self,x=x,y=y)
                count += 1
                self.register(new_predator)
        #same loop but for count_humans
        count = 0
        while count < count_humans: #while loop continues until count_humans unoccupied positions are found
            x = random.randint(0,self.grid_size-1) #using randint to place humans randomly on the grid
            y = random.randint(0,self.grid_size-1)
            if not self.animal(x,y):
                new_human=Human(island=self,x=x,y=y)
                count += 1
                self.register(new_human)
    #keeping these methods the same
    def clear_all_moved_flags(self):
        ''' Animals have a moved flag to indicated they moved this turn.
        Clear that so we can do the next turn
        '''
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()
        
    def size(self): 
        '''Return size of the island: one dimension.
        '''
        return self.grid_size

    def register(self,animal):
        '''Register animal with island, i.e. put it at the 
        animal's coordinates
        '''
        x = animal.x
        y = animal.y
        self.grid[x][y] = animal

    def remove(self,animal):
        '''Remove animal from island.'''
        x = animal.x
        y = animal.y
        self.grid[x][y] = 0

    def animal(self,x,y):
        '''Return animal at location (x,y)'''
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        else:
            return -1  # outside island boundary

    def __str__(self):
        '''String representation for printing.
           (0,0) will be in the lower left corner.
        '''
        s = ""
        for j in range(self.grid_size-1,-1,-1):  # print row size-1 first
            for i in range(self.grid_size):      # each row starts at 0
                if not self.grid[i][j]:
                    # print a '.' for an empty space
                    s+= "{:<2s}".format('.' + "  ")
                else:
                    s+= "{:<2s}".format((str(self.grid[i][j])) + "  ")
            s+="\n"
        return s

    def count_prey(self):
        ''' count all the prey on the island'''
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x,y)
                if animal:
                    if isinstance(animal,Prey):
                        count+=1
        return count

    def count_predators(self):
        ''' count all the predators on the island'''
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x,y)
                if animal:
                    if isinstance(animal,Predator):
                        count+=1
        return count

    def count_humans(self) -> int: #added the method count_humans()
        '''count all humans on the island'''
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x,y)
                if animal:
                    if isinstance(animal,Human):
                        count+=1
        return count
    
class Animal(object):
    def __init__(self, island, x=0, y=0, s="A"):
        '''Initialize the animal's and their positions
        '''
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved=False
            
    def position(self):
        '''Return coordinates of current position.
        '''
        return self.x, self.y

    def __str__(self):
        return self.name
    
    def check_grid(self,type_looking_for=int):
        ''' Look in the 8 directions from the animal's location
        and return the first location that presently has an object
        of the specified type. Return 0 if no such location exists
        '''
        # neighbor offsets
        offset = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)] 
        result = 0
        for i in range(len(offset)):
            x = self.x + offset[i][0]  # neighboring coordinates
            y = self.y + offset[i][1]
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x,y))==type_looking_for:
                result=(x,y)
                break
        return result

    def move(self):
        '''Move to an open, neighboring position '''
        if not self.moved:
            location = self.check_grid(int)
            if location:
                # print('Move, {}, from {},{} to {},{}'.format( \
                #       type(self),self.x,self.y,location[0],location[1]))
                self.island.remove(self)   # remove from current spot
                self.x = location[0]       # new coordinates
                self.y = location[1]
                self.island.register(self) # register new coordinates
                self.moved=True
    def breed(self):
        ''' Breed a new Animal.If there is room in one of the 8 locations
        place the new Prey there. Otherwise you have to wait.
        '''
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                # print('Breeding Prey {},{}'.format(self.x,self.y))
                the_class = self.__class__
                new_animal = the_class(self.island,x=location[0],y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self):
        self.moved=False

class Prey(Animal):
    def __init__(self, island, x=0,y=0,s="O"):
        Animal.__init__(self,island,x,y,s)
        self.breed_clock = self.breed_time
        # print('Init Prey {},{}, breed:{}'.format(self.x, self.y,self.breed_clock))
           
    def clock_tick(self):
        '''Prey only updates its local breed clock
        '''
        self.breed_clock -= 1
        # print('Tick Prey {},{}, breed:{}'.format(self.x,self.y,self.breed_clock))

class Predator(Animal):
    def __init__(self, island, x=0,y=0,s="X"):
        Animal.__init__(self,island,x,y,s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time
        # print('Init Predator {},{}, starve:{}, breed:{}'.format( \
        #       self.x,self.y,self.starve_clock,self.breed_clock))

    def clock_tick(self):
        ''' Predator updates both breeding and starving
        '''
        self.breed_clock -= 1
        self.starve_clock -= 1
        # print('Tick, Predator at {},{} starve:{}, breed:{}'.format( \
        #       self.x,self.y,self.starve_clock,self.breed_clock))
        if self.starve_clock <= 0:
            # print('Death, Predator at {},{}'.format(self.x,self.y))
            self.island.remove(self)

    def eat(self):
        ''' Predator looks for one of the 8 locations with Prey. If found
        moves to that location, updates the starve clock, removes the Prey
        '''
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                # print('Eating: pred at {},{}, prey at {},{}'.format( \
                #       self.x,self.y,location[0],location[1]))
                self.island.remove(self.island.animal(location[0],location[1]))
                self.island.remove(self)
                self.x=location[0]
                self.y=location[1]
                self.island.register(self)
                self.starve_clock=self.starve_time
                self.moved=True

class Human(Animal): #added the class Human, inherits moving and breeding from Animal, has its own hunt method
    '''class to represent humans, that hunt, breed, and move, 
     inhereting methods from its superclass (Animal) '''
    def __init__(self, island: object, x: int=0, y: int=0, s: str="H") -> None: 
        '''initialize humans and their locations on grid'''
        Animal.__init__(self,island,x,y,s)
        self.hunt_clock = self.hunt_time #class variables for hunt, breed, and starve times are set in main
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None: #clock_tick for humans, includes hunt timer, breed timer, and starve timer
        '''humans update hunting, breeding, and starving'''
        self.hunt_clock -= 1
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0: #if starve clock is 0, human dies and is removed 
            self.island.remove(self)

    def hunt(self) -> None: #created a hunt method for humans, closley mirros the eat method for predators
        '''human looks into 8 surrounding locations for a predator when the hunt clock is out. 
        if found, moves to that location, resets hunt and starve clock, removes predator
        hunt clock only resets when a predator is found and eaten, it will decrease till then to prevent starvation'''
        if not self.moved and self.hunt_clock <= 0: #if hunt clock is out and the human has not moved this tick, check for predators
            location = self.check_grid(Predator)
            if location: #if a predaor is found 
                self.island.remove(self.island.animal(location[0],location[1])) #remove the predator 
                self.island.remove(self) #remove from old location
                self.x=location[0] #update human location to predators
                self.y=location[1]
                self.island.register(self) #register the humans new location
                self.starve_clock=self.starve_time #reset starve clock
                self.hunt_clock=self.hunt_time #resey hunt clock
                self.moved=True

        
########################################### 
def main(predator_breed_time: int=10, predator_starve_time: int=5, initial_predators: int=10, prey_breed_time: int=8, initial_prey: int=40, \
         human_breed_time: int=11, human_starve_time: int=20, Human_hunt_time: int=5, initial_humans: int=10,size: int=10, ticks: int=1000) -> None: 
    #added parameters for human breed, starve, and hunt times, as well as initial humans
    ''' main simulation. Sets defaults, runs event loop, plots at the end
    '''
    # initialization values
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = Human_hunt_time

    # for graphing, added human_list to record human population over time
    predator_list=[]
    prey_list=[]
    human_list=[]

    # make an island
    isle = Island(size,initial_prey, initial_predators, initial_humans) #added initial_humans to constructor for island
    print(isle)

    # event loop. 
    # For all the ticks, for every x,y location.
    # If there is an animal there, try eat, move, breed and clock_tick
    for i in range(ticks):
        # important to clear all the moved flags!
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x,y)
                if animal:
                    if isinstance(animal,Predator):
                        animal.eat()
                    elif isinstance(animal,Human): #added humans so they hunt just like predators
                        animal.hunt()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()
        
        # record info for display, plotting
        prey_count = isle.count_prey()
        predator_count = isle.count_predators()
        human_count = isle.count_humans() #human_count to keep track of human population
        ####### ------- commented this code out as the simulation only stops after 1000 ticks or all three converge to constant values
        # if prey_count == 0:
        #     print('Lost the Prey population. Quiting.')
        #     break
        # if predator_count == 0:
        #     print('Lost the Predator population. Quitting.')
        #     break
        # if human_count == 0: #check for extinct human population
        #     print('Lost the Human population. Quitting.')
        #     break
        prey_list.append(prey_count)
        predator_list.append(predator_count)
        human_list.append(human_count) #append human population to list 
        
        ####### ------here i did the convergence chack
        if i >= 20: #if the prey, predator, and human pops havent chnaged in 20 ticks, there constant populations and the sim ends
            if prey_list[i] == prey_list[i-19] == prey_list[i-18] and predator_list[i] == predator_list[i-19] == predator_list[i-18] and human_list[i] == human_list[i-19] == human_list[i-18]: 
                print('Populations have converged to constant values. Quitting.')
                break

        # print out every 10th cycle, see what's going on
        if not i%10:
            print(prey_count, predator_count, human_count) #print populations
        # print the island, hold at the end of each cycle to get a look
        # print('*'*20)
        # print(isle)
        # ans = input("Return to continue")
    print('Final island:')
    print(isle)
    plt.plot(predator_list)
    plt.plot(prey_list)
    plt.plot(human_list) #plot human population
    #added labels to humans, predators, and prey
    plt.legend(['Predators', 'Prey', 'Humans'])
    plt.show()
    print('Jorn Rutkis')
    print('Z-Number: Z23737550')

if __name__ == "__main__":
    main()