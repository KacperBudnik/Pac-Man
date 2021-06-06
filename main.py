import random
import arcade
import os
from PIL import Image

# Własne
#import map
import Pacman
import main_menu

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self,width, height, title):
        super().__init__(width, height, title)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.set_location(400,200)
        self.camera_pos=[0,0]

        self.game_running=False
        self.pause=True

        self.menu = main_menu.Menu(width, height)


    

        arcade.set_background_color(arcade.color.BLACK)

        self.test=0
        self.up=True

        
        self.rotation=0
        self.x_pos=400  
        self.y_pos=300
    

    def on_draw(self):
        arcade.start_render()

        if not self.game_running:
            self.menu.Draw()
        else:
            self.draw_background()
            self.draw_points()
            self.pacman.Draw()


    def draw_points(self):
        pass#for i in range(1,)

    def draw_background(self):
        self.background.draw_scaled(self.SCREEN_WIDTH*0.4,self.SCREEN_HEIGHT*0.4,self.scale,0)
        arcade.draw_rectangle_filled(self.SCREEN_WIDTH*0.5,self.SCREEN_HEIGHT*0.9,self.SCREEN_WIDTH,self.SCREEN_HEIGHT*0.2,(0,0,30))
        arcade.draw_rectangle_filled(self.SCREEN_WIDTH*0.9,self.SCREEN_HEIGHT*0.5,self.SCREEN_WIDTH*0.2,self.SCREEN_HEIGHT,(0,0,30))
        arcade.draw_text(
            "Pac Man",
            start_x=self.SCREEN_WIDTH/2,
            start_y=self.SCREEN_HEIGHT/11*10,
            color=arcade.csscolor.YELLOW,
            font_size=48*self.SCREEN_HEIGHT/600,
            font_name=self.pacfont,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            "Points",
            start_x=self.SCREEN_WIDTH*0.9,
            start_y=self.SCREEN_HEIGHT*0.7,
            color=arcade.csscolor.WHEAT,
            font_size=24*self.SCREEN_HEIGHT/600,
            font_name=self.arcade_classic_font,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

    def on_update(self, delta_time):
        if self.game_running:
            self.pacman.Update(delta_time)
        else:
            self.menu.on_update(2*4*delta_time)
            if self.menu.running:
                self.start_game()
                self.game_running=True

    def on_key_press(self, key, cos):
        if self.game_running:
            if True:#not self.pause:
                self.pacman.Key_press(key)
        else:
            self.menu.key_press(key)
            


    def start_game(self):
        print("Let's the game begin!")
        self.background=self.menu.background
        self.scale=self.menu.scale
        self.map_im=self.menu.map_im
        self.im_width, self.im_height = self.map_im.size
        self.map=self.menu.map
        self.SCREEN_WIDTH=self.menu.SCREEN_WIDTH
        self.SCREEN_HEIGHT=self.menu.SCREEN_HEIGHT
        self.pac_size=self.menu.pac_size
        self.pac_pos=[self.SCREEN_WIDTH*0.4,self.SCREEN_WIDTH*0.3+self.im_height/2*self.scale-self.im_height*self.menu.start_pos/len(self.map)*self.scale+self.pac_size/2]
        self.pacman=Pacman.Pac_man(self.map,
            self.menu.up_key,self.menu.right_key,self.menu.down_key,self.menu.left_key,
            self.pac_pos,self.pac_size,
            self.pos,
            [self.menu.start_pos-1,len(self.map[0])//2],
            self.scale)

        self.pacfont=self.menu.pacfont
        self.arcade_classic_font=self.menu.arcade_classic_font

        self.map_size=(len(self.map[0]),len(self.map))

    def pos(self,pos_on_map):
        
        a=self.SCREEN_WIDTH*0.3+self.im_height/2*self.scale-self.im_height*(pos_on_map[0]+1)/self.map_size[1]*self.scale+self.pac_size/2
        b=self.SCREEN_WIDTH*0.4+self.im_width/2*self.scale-self.im_width*(self.map_size[0]-pos_on_map[1])/self.map_size[0]*self.scale+self.pac_size/2
        return [b,a]


def main():
    """ Start the game """
    window = MyGame(800, 600, "Pac-man")
    arcade.run()


if __name__ == "__main__":
    main()