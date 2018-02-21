import wx
import numpy as np
import random
import sys

class Tetris(object):
    def __init__(self):
        self.col = 12
        self.row = 20
        self.grid = np.zeros((self.row,self.col),dtype=int)
        self.grid[self.row-1,:] = 2 # bottom
        self.grid[:,0] = 1 # left wall
        self.grid[:,self.col-1] = 1 # right wall
        
        self.block_x = 5
        self.block_y = 0
        self.rot = 0
        self.block_status = False
        self.block_right = True
        self.block_left = True
        self.block_down = True
        self.block_rot = True
        self.blocktype = 0
        self.block_coordinates = np.zeros((4,2),dtype=int)
        
        self.erase_comparison = np.full(self.col-2,2)
        self.newrow = np.zeros((1,self.col),dtype=int)
        self.newrow[0][0] = 1
        self.newrow[0][self.col-1] = 1
        

        Block_data = [[[[0,0],[1,0],[0,1],[1,1]], [[0,0],[1,0],[0,1],[1,1]], [[0,0],[1,0],[0,1],[1,1]], [[0,0],[1,0],[0,1],[1,1]]],\
                [[[0,0],[0,1],[0,2],[0,3]], [[0,0],[1,0],[2,0],[3,0]], [[0,0],[0,1],[0,2],[0,3]], [[0,0],[1,0],[2,0],[3,0]]],\
                [[[0,0],[1,0],[2,0],[1,1]], [[1,0],[1,1],[1,2],[0,1]], [[1,1],[0,2],[1,2],[2,2]], [[1,1],[0,2],[1,2],[2,2]]],\
                [[[0,0],[0,1],[1,1],[1,2]], [[1,0],[2,0],[0,1],[1,1]], [[0,0],[0,1],[1,1],[1,2]], [[1,0],[2,0],[0,1],[1,1]]],\
                [[[1,0],[1,1],[0,1],[0,2]], [[0,0],[1,0],[1,1],[2,1]], [[1,0],[1,1],[0,1],[0,2]], [[0,0],[1,0],[1,1],[2,1]]],\
                [[[0,0],[1,0],[2,0],[2,1]], [[1,0],[1,1],[1,2],[0,2]], [[0,0],[0,1],[0,2],[1,2]], [[0,0],[0,1],[1,0],[2,0]]],\
                [[[0,0],[1,0],[2,0],[0,1]], [[0,0],[1,0],[1,1],[1,2]], [[0,1],[1,1],[2,1],[2,0]], [[0,0],[0,1],[0,2],[1,2]]]]
        self.block_data = np.array(Block_data)

    def reach_bottom(self):
        for i in range(4):
            if self.grid[self.block_coordinates[i][1]+1,self.block_coordinates[i][0]] == 2:
                self.rewrite_grid()
                self.block_status = False
                return True
        return False
    
    def movement_check(self):  
        self.block_down = True
        self.block_right = True
        self.block_left = True
        self.block_rot = True

        for i in range(4):
            if self.grid[self.block_coordinates[i][1],self.block_coordinates[i][0]+1] == 1:
                self.block_right = False
            if self.grid[self.block_coordinates[i][1],self.block_coordinates[i][0]+1] == 2:
                self.block_right = False
            if self.grid[self.block_coordinates[i][1],self.block_coordinates[i][0]-1] == 1:
                self.block_left = False
            if self.grid[self.block_coordinates[i][1],self.block_coordinates[i][0]-1] == 2:
                self.block_left = False
        
        block_rot_coordinates = np.array(self.block_data[self.blocktype][(self.rot+1)%4])
        for i in range(4):
            block_rot_coordinates[i] = [self.block_x+block_rot_coordinates[i][0],self.block_y+block_rot_coordinates[i][1]]
            if block_rot_coordinates[i][0] < 0 or block_rot_coordinates[i][0] > self.col-1:
                self.block_rot = False
            else:
                if self.grid[block_rot_coordinates[i][1],block_rot_coordinates[i][0]] == 1:
                    self.block_rot = False
                if self.grid[block_rot_coordinates[i][1],block_rot_coordinates[i][0]] == 2:
                    self.block_rot = False


               
    
    def rewrite_grid(self):
        for i in range(4):
            x = self.block_coordinates[i][0]
            y = self.block_coordinates[i][1]
            self.grid[y][x] = 2
    
    def calc_block(self):
        block_relcoordinates = np.array(self.block_data[self.blocktype][self.rot])
        for i in range(4):
            self.block_coordinates[i] = [self.block_x+block_relcoordinates[i][0],self.block_y+block_relcoordinates[i][1]]

    def drop_block(self):
        if self.block_status == False:
            self.block_x = 5
            self.block_y = 0
            self.rot = 0
            self.block_status = True
            self.blocktype = random.randint(0,6)

    def execute_grid(self):
        
        self.grid_display = np.array(self.grid)
        self.calc_block()
        self.reach_bottom()
        self.gameover()
        self.erase_block()
        self.drop_block()
        self.movement_check()
        for i in range(4):
            x =self.block_coordinates[i][0]
            y = self.block_coordinates[i][1]
            self.grid_display[y][x] = 3
        for i in range(self.col):
            self.grid_display[self.row-1][i] = 1
        #print(self.grid_display)    
        
    
    def erase_block(self):
        for i in list(range(self.row-1)):
            grid_cropped = self.grid[i][1:self.col-1]
            #print(grid_cropped)
            if np.allclose(grid_cropped,self.erase_comparison):
                self.grid = np.delete(self.grid,i,0)
                print(i)
                self.grid = np.concatenate([self.newrow,self.grid])
                
    
    def move_block(self,command):
        if command == b"s":
            if self.block_down == True:
                self.block_y = self.block_y + 1
        if command == b"a":
            if self.block_left == True:
                self.block_x = self.block_x - 1
        if command == b"d":
            if self.block_right == True:
                self.block_x = self.block_x + 1
        if command == b"r":
            if self.block_rot == True:
                self.rot = (self.rot + 1)%4

    def gameover(self):
        if 2 in self.grid[1]:
            print("gameover")
            sys.exit()

    
if __name__ == '__main__':
    tetris = Tetris()
    while(True):
        if not tetris.block_status:
            tetris.drop_block()
            array = tetris.calc_block()
            tetris.execute_grid(array)
        else:
            array_before = np.array(array)
            pre_block_x = tetris.block_x
            pre_block_y = tetris.block_y
            pre_rot = tetris.rot
            tetris.move_block(input())
            array = tetris.calc_block()
            if tetris.hit_wall(array):
                tetris.block_x = pre_block_x
                tetris.block_y = pre_block_y 
                tetris.rot = pre_rot 
                array = array_before
            if tetris.reach_bottom(array):
                tetris.rewrite_grid(array_before)
                tetris.block_status = False
            tetris.erase_block()
            tetris.execute_grid(array)