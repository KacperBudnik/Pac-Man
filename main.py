import random
import arcade
import os

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

        self.pacman=Pacman.Pac_man()
    


        #self.background = arcade.load_texture(arcade.Texture("vso",map.map_background_generation()))
        #print(map.map_background_generation())

        #self.background=arcade.Texture("whatever",map.map_background_generation(50,25))



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
            arcade.draw_lrwh_rectangle_textured(self.camera_pos[0], self.camera_pos[1], self.SCREEN_WIDTH, self.SCREEN_HEIGHT,self.background)
            self.pacman.Draw()

        
    def on_update(self, delta_time):
        if self.game_running:
            self.pacman.Update(delta_time)


            if not self.pause:
                if self.rotation == 0:
                    self.camera_pos[0]-=60*delta_time
                elif self.rotation == 90:
                    self.camera_pos[1]-=60*delta_time
                elif self.rotation == 180:
                    self.camera_pos[0]+=60*delta_time
                else:
                    self.camera_pos[1]+=60*delta_time
        else:
            self.menu.on_update(delta_time)

    def on_key_press(self, key, cos):
        if self.game_running:
            if not self.pause:
                self.pacman.Key_press(key)
        else:
            self.menu.key_press(key)
            if self.menu.running:
                self.start_game()

        if key==arcade.key.ESCAPE:
            self.game_running = not self.game_running
        if key==arcade.key.SPACE:
            self.pause = not self.pause

    def start_game(self):
        print("Let's the game begin!")


def main():
    """ Start the game """
    window = MyGame(800, 600, "Pac-man")
    arcade.run()


if __name__ == "__main__":
    main()