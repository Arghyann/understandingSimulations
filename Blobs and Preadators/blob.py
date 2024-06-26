import random
from environment import Environment
import numpy as np

class Blob:
    def __init__(self, gender, age, environmentInstance,x=-1,y=-1):  #gender : true = male
        self.gender=gender
        self.age=age
        self.environment = environmentInstance
        self.birthenergy=50
        self.energy = self.birthenergy
        if x==-1:
            self.x =random.randint(0,self.environment.dimension-1)
            self.y = random.randint(0,self.environment.dimension-1)
        else:
            self.x=x
            self.y=y
        self.environment.space[self.x,self.y] = [0, 0, 150]
        self.energy_for_movement = 5
        self.food_content = 25
        self.environment.blobs.append(self)
        self.childage=5


    def movement(self):
        
        if self.energy <= 0 or self.age >= 10:
            self.environment.blobs.remove(self)
            self.environment.space[self.x,self.y] = [0,0,0]
            del(self)
            return
        if np.array_equal(self.environment.space[self.x, self.y], [255, 0, 0]):
            self.environment.blobs.remove(self)
            del(self)
            return
        if(self.energy>=200):
            self.mitosis()
        self.environment.space[self.x, self.y] = [0, 0, 0]
        
        possible_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(possible_moves)


        #RESOURCE CONSUMPTION
        # checks for food/resource first so technically gives priority to it i gave it colour green: 0,200,0
        for move in possible_moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            if 0 <= new_x < self.environment.dimension and 0 <= new_y < self.environment.dimension:
                if np.array_equal(self.environment.space[new_x, new_y], [0, 200, 0]):
                    self.x, self.y = new_x, new_y
                    self.environment.space[self.x, self.y] = [0, 0, 150]
                    self.energy += self.food_content
                    self.energy -= self.energy_for_movement
                    return

        # lets say agar resource doeesnt exist, toh itll automatically move to the available
        for move in possible_moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            if 0 <= new_x < self.environment.dimension and 0 <= new_y < self.environment.dimension:
                if np.array_equal(self.environment.space[new_x, new_y], [0, 0, 0]):
                    self.x, self.y = new_x, new_y
                    self.environment.space[self.x, self.y] = [0, 0, 150]
                    self.energy -= self.energy_for_movement
                    return

        # agar no empty it'll stay wahi; ab kuch nahi ho sakta in deadlock figure out karenge baadme what to do
        self.environment.space[self.x, self.y] = [0, 0, 150]

    def mitosis(self):
        j=0
        for i in range(-1,2):
            for j in range(-1,2):
                newx=self.x+i
                newy=self.y+j
                if 0 <= newx < self.environment.dimension and 0 <= newy < self.environment.dimension:
                    if np.array_equal(self.environment.space[newx, newy], [0, 0, 0]):
                        
                        Blob(True, self.childage, self.environment,newx,newy)
                        self.energy=self.birthenergy
                        self.environment.mitosisCount+=1


        

        