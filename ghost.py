import arcade
from random import choice
from PIL import Image
from numpy import array

class Ghost:
    """ Main application class. """

    def __init__(self,speed,map,pos,start_pos,scale,color):
        self.speed=speed
        self.map=map
        self.pos=pos
        pos=self.pos(start_pos)
        self.direction=5
        self.pos_on_map=start_pos
        self.right=0
        self.down=0
        self.last_choosen_on=0
        self.scale=scale
        self.way=0

        im = Image.open('img/Ghost_imag.png')
        im = im.convert('RGBA')

        data = array(im)
        red, green, blue, alpha = data.T

        white_areas = (red == 255) & (blue == 0) & (green == 0)
        data[..., :-1][white_areas.T] = color

        im = Image.fromarray(data)

        #self.sprite=arcade.Sprite(arcade.Texture("whatever",im2),center_x=pos[0],center_y=pos[1])
        self.sprite=arcade.Texture("whatever",im)

    

    def Draw(self):
        pos=self.pos([self.pos_on_map[0]+self.down,self.pos_on_map[1]+self.right])  
        self.sprite.draw_scaled(pos[0],pos[1],(-1)**(self.way//0.5)*self.scale,0,255)
        
    def Update(self, delta_time):
        #self.way+=delta_time
        self.choose_direct()




        if self.direction == 0:
            self.right+=self.speed*delta_time
        elif self.direction == 1:
            self.down-=self.speed*delta_time
        elif self.direction == 2:
            self.right-=self.speed*delta_time
        elif self.direction == 3:
            self.down+=self.speed*delta_time


        self.pos_on_map[1]+=int((self.right+1/2)//1)
        self.right=(self.right+1/2)%1-1/2
        self.pos_on_map[0]+=int((self.down+1/2)//1)
        self.down=(self.down+1/2)%1-1/2

    def choose_direct(self):
        if self.last_choosen_on != self.pos_on_map and -0.1<=self.down<=0.1 and -0.1<=self.right<=0.1:
            self.last_choosen_on=self.pos_on_map.copy()
            choises=[]
            if self.map[self.pos_on_map[0]][self.pos_on_map[1]+1] != 0 and self.direction!=2:
                choises.append(0)

            if self.map[self.pos_on_map[0]-1][self.pos_on_map[1]] != 0 and self.direction!=3:
                choises.append(1)

            if self.map[self.pos_on_map[0]][self.pos_on_map[1]-1] != 0 and self.direction!=0:
                choises.append(2)

            if self.map[self.pos_on_map[0]+1][self.pos_on_map[1]] != 0 and self.direction!=1:
                choises.append(3)


            self.direction=choice(choises)
