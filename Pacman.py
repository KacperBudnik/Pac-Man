import arcade



class Pac_man:
    """ Main hero class. """

    def __init__(self,map, up,right,down,left,pac_size, pos ,pos_on_map, scale,speed,lives):
        """ Initialize pacman. 
            :param:
                map (Vector{Vector}): game map
                up (int): pacman direction change key (up)
                right (int): pacman direction change key (right)
                down (int): pacman direction change key (down)
                left (int): pacman direction change key (left)  
                pac_size (flaot): scaled pacman size
                pos (function): function to calculate positon related to Window
                pos_on_map (int): pacman start position on map
                scale (float): scale of map image
                speed (int): pacman speed 
                lives (int): number of lives
                """     
        self.right_key=right
        self.left_key=left
        self.down_key=down
        self.up_key=up
        self.lives=lives
        
        self.pos=pos

        self.map=map

        self.down=0
        self.right=-1/2

        self.direction=5
        self.direction_buff=1

        self.mouth_tick=30

        self.pac_size=pac_size
        self.scale=scale

        self.game_running=False
        self.pause=True

        self.pac_speed=speed

        self.pos_on_map=pos_on_map


        self.up=True


    

    def Draw(self):
        """ Draw pacman"""
        pos=self.pos([self.pos_on_map[0]+self.down,self.pos_on_map[1]+self.right])
        arcade.draw_arc_filled(pos[0]-2, pos[1]-2,
        self.pac_size,self.pac_size,arcade.color.YELLOW,0,360-2*self.mouth_tick,self.mouth_tick+90*self.direction)
        
    def Update(self, delta_time):
        """ Update pacman 
            :param:
                    delta_time (float): time since the last execution of the function"""
        if self.up:
            self.mouth_tick+=60*delta_time
            if self.mouth_tick>30:
                self.up=False
        else:
            self.mouth_tick-=60*delta_time
            if self.mouth_tick<=0:
                self.up=True




        if self.direction==0:
            if self.map[self.pos_on_map[0]][self.pos_on_map[1]+1] == 0:
                if self.right>0:
                    self.direction+=4

        elif self.direction==1:
            if self.map[self.pos_on_map[0]-1][self.pos_on_map[1]] == 0:
                if self.down<=0:
                    self.direction+=4

        elif self.direction==2:
            if self.map[self.pos_on_map[0]][self.pos_on_map[1]-1] == 0:
                if self.right<=0:
                    self.direction+=4

        elif self.direction==3:
            if self.map[self.pos_on_map[0]+1][self.pos_on_map[1]] == 0:
                if self.down>=0:
                    self.direction+=4




        
        if self.direction_buff==0  and -self.pac_speed/25<=self.down<=self.pac_speed/25:
            if self.map[self.pos_on_map[0]][self.pos_on_map[1]+1] != 0:
                self.direction=self.direction_buff
                self.down=0

        elif self.direction_buff==1 and -self.pac_speed/25<=self.right<=self.pac_speed/25:
            if self.map[self.pos_on_map[0]-1][self.pos_on_map[1]] != 0:
                self.direction=self.direction_buff
                self.right=0

        elif self.direction_buff==2 and -self.pac_speed/25<=self.down<=self.pac_speed/25:
            if self.map[self.pos_on_map[0]][self.pos_on_map[1]-1] != 0:
                self.direction=self.direction_buff
                self.down=0

        elif self.direction_buff==3 and -self.pac_speed/25<=self.right<=self.pac_speed/25:
            if self.map[self.pos_on_map[0]+1][self.pos_on_map[1]] != 0:
                self.direction=self.direction_buff
                self.right=0

        if self.direction == 0:
            self.right+=self.pac_speed*delta_time
        elif self.direction == 1:
            self.down-=self.pac_speed*delta_time
        elif self.direction == 2:
            self.right-=self.pac_speed*delta_time
        elif self.direction == 3:
            self.down+=self.pac_speed*delta_time


        self.pos_on_map[1]+=int((self.right+1/2)//1)
        self.right=(self.right+1/2)%1-1/2
        self.pos_on_map[0]+=int((self.down+1/2)//1)
        self.down=(self.down+1/2)%1-1/2



    def Key_press(self, key):
        """ Called whenever a key is pressed while playing
            :param:
                key (int): kod of pressed key"""
        if key == self.right_key:
            self.direction_buff=0
        elif key == self.left_key:
            self.direction_buff=2
        elif key == self.up_key:
            self.direction_buff=1
        elif key == self.down_key:
            self.direction_buff=3
