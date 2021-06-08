import arcade
from random import choice
from PIL import Image
from numpy import array

class Ghost:
    """ Main application class. """

    def __init__(self,speed,map,pos,start_pos,scale,color,fear_time,time_to_release):
        self.speed=speed
        self.map=map
        self.pos=pos
        #pos=self.pos([len(self.map)//3,len(self.map[0])//2])
        self.direction=5
        #if len(self.map)%3==0:
        self.pos_on_map=[(len(self.map))//3+2,len(self.map[0])//2]
        self.down=-(1)*((len(self.map)/3-1)%3)

        """elif len(self.map)%3==1:
            self.pos_on_map=[(len(self.map)-1)//3+2,len(self.map[0])//2]
        else:
            self.pos_on_map=[(len(self.map)-2)//3+2,len(self.map[0])//2]"""
        #self.pos_on_map=[1,1]
        self.right=-1/2
        #self.down=0
        self.last_choosen_on=0
        self.scale=scale
        self.way=0

        self.time_to_release=time_to_release
        self.tick_to_release=0
        self.free=False
        self.make_free=False
        self.make_captivity=False
        self.tick_to_captivity=0

        im = Image.open('assets/img/Ghost_imag.png')
        im = im.convert('RGBA')

        data = array(im)
        red, green, blue, alpha = data.T

        white_areas = (red == 255) & (blue == 0) & (green == 0)
        data[..., :-1][white_areas.T] = color

        self.im = Image.fromarray(data)
        self.im_fear=Image.open('assets/img/Ghost_imag_fear.png')

        #self.sprite=arcade.Sprite(arcade.Texture("whatever",im2),center_x=pos[0],center_y=pos[1])
        self.sprite=arcade.Texture("whatever",self.im)
        self.sprite_fear=arcade.Texture("whatrver",self.im_fear)
        self.fear=False
        self.fear_tick=0
        self.fear_time=fear_time



    

    def Draw(self):
        pos=self.pos([self.pos_on_map[0]+self.down,self.pos_on_map[1]+self.right])  
        if self.make_captivity:
            go_to=self.pos([len(self.map)//3+2,len(self.map[0])//2])
            pos[0]=pos[0]*(2-self.tick_to_captivity)/2 + go_to[0]*(self.tick_to_captivity)/2*self.scale
            pos[1]=pos[1]*(2-self.tick_to_captivity)/2 + go_to[1]*(self.tick_to_captivity)/2*self.scale
        if self.fear:
            self.sprite_fear.draw_scaled(pos[0],pos[1],self.scale,0,255)
        else:
            self.sprite.draw_scaled(pos[0],pos[1],self.scale,0,255)
        
    def Update(self, delta_time):
        #self.way+=delta_time
        if self.make_free:
            self.let_free(delta_time)
        elif self.make_captivity:
            self.take_freedom(delta_time)
        elif self.free:
            try:
                self.choose_direct()
            except:
                self.down=0
                self.right=0
                self.direction = (self.direction+2)%4

            if self.fear:
                self.fear_tick+=delta_time
                if self.fear_tick>self.fear_time:
                    self.fear=False
                    self.fear_tick=0

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
        else:
            if self.tick_to_release>self.time_to_release:
                self.free=True
                self.make_free=True
                self.tick_to_release=0
                self.pos_on_map=[len(self.map)//3+2,len(self.map[0])//2]

            

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
        if self.direction==0 or self.direction==1:
            if self.fear:
                self.sprite_fear=arcade.Texture("whatrver",self.im_fear)
            else:
                self.sprite=arcade.Texture("whatever",self.im)
        else:
            if self.fear:
                self.sprite_fear=arcade.Texture("whatrver",self.im_fear.transpose(Image.FLIP_LEFT_RIGHT))
            else:
                self.sprite=arcade.Texture("whatever",self.im.transpose(Image.FLIP_LEFT_RIGHT))


    def let_free(self,delta_tick):
        self.down-=delta_tick
        self.tick_to_release+=delta_tick
        if self.tick_to_release>2:
            self.make_free=False
            self.pos_on_map=[len(self.map)//3+2,len(self.map[0])//2]
            self.free=True
            self.direction=choice([0,2])
            self.tick_to_release=0

    def take_freedom(self, delta_tick):
        self.free=False
        self.direction=5
        if self.tick_to_captivity<2:
            self.tick_to_captivity+=delta_tick
        else:
            self.make_captivity=False
            self.tick_to_captivity=0
            self.pos_on_map=[len(self.map)//3+2,len(self.map[0])//2]
            self.down=0
            self.right=-1/2
            self.free=False










