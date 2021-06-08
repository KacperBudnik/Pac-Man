import random
import arcade
import os
from PIL import Image

# Własne
#import map
import Pacman
import main_menu
import ghost

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self,width, height, title):
        super().__init__(width, height, title)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.set_location(400,200)
        self.camera_pos=[0,0]

        self.pause_text="Press to Start"
        self.pause=False
        self.pause_butt=arcade.key.SPACE
        self.restart=False
        self.points=0

        self.game_running=False
        self.pause=True
        self.game_over_tick=0
        self.game_over=False

        self.menu = main_menu.Menu(width, height)

    

        arcade.set_background_color(arcade.color.BLACK)

        self.test=0
        self.up=True
        self.death_tick=0
        self.dead=False
        
        self.godmod=False
        #self.point_sound = arcade.load_sound("assets/sounds/pacman_chomp.wav")
        self.point_sound_tick=True
        self.small_point_sound = arcade.load_sound("assets/sounds/munch_1.wav")
        self.big_point_sound = arcade.load_sound("assets/sounds/munch_2.wav")
        self.godmod_sound = arcade.load_sound("assets/sounds/pacman_intermission.wav")
        self.pursuit_level=0
        self.pursuit = [arcade.load_sound("assets/sounds/siren_"+str(i+1)+".wav") for i in range(5)]
        self.death_song = arcade.load_sound("assets/sounds/death_1.wav")

        self.god_song_play = arcade.play_sound(self.godmod_sound,1,0,True)
        arcade.stop_sound(self.god_song_play)
        self.play_chase = arcade.play_sound(self.pursuit[0],1,0,True)
        arcade.stop_sound(self.play_chase)


    def on_draw(self):
        arcade.start_render()

        if not self.game_running:
            self.menu.Draw()
        else:
            self.draw_background()
            if not self.dead:
                self.pacman.Draw()
            for i in range(self.ghost_num):
                    self.ghost[i].Draw()
            if self.dead:
                pos=self.pos([self.pacman.pos_on_map[0]+self.pacman.down,self.pacman.pos_on_map[1]+self.pacman.right])
                arcade.draw_arc_filled(pos[0]-2, pos[1]-2,
                    self.pac_size,self.pac_size,arcade.color.YELLOW,0,360-2*self.pacman.mouth_tick-self.death_tick*120,self.pacman.mouth_tick+90*self.pacman.direction+self.death_tick*60)

            if self.pause:
                arcade.draw_text(
                    self.pause_text,
                    start_x=self.SCREEN_WIDTH*0.4,
                    start_y=self.SCREEN_HEIGHT*0.4,
                    color=arcade.csscolor.WHITE_SMOKE,
                    font_size=48*self.SCREEN_HEIGHT/600,
                    font_name=self.arcade_classic_font,
                    align="center",
                    anchor_x="center",
                    anchor_y="center"
                )



    def draw_points(self):
        self.restart=True
        for i in range(1,self.map_size[1]-1):
            for j in range(1,self.map_size[0]-1):
                pos=self.pos([i,j])
                if self.map[i][j]==1:
                    arcade.draw_point(pos[0], pos[1], arcade.color.LIGHT_YELLOW, 3*self.scale)
                    self.restart=False
                elif self.map[i][j]==2:
                    arcade.draw_circle_filled(pos[0],pos[1],6*self.scale,arcade.color.LIGHT_YELLOW)
                    arcade.draw_circle_outline(pos[0],pos[1],6*self.scale,arcade.color.ORANGE,1)
                    self.restart=False



    def draw_background(self):
        self.background.draw_scaled(self.SCREEN_WIDTH*0.4,self.SCREEN_HEIGHT*0.4,self.scale,0)
        self.draw_points()
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
        arcade.draw_text(
            "{:06d}".format(self.points),
            start_x=self.SCREEN_WIDTH*0.9,
            start_y=self.SCREEN_HEIGHT*0.65,
            color=arcade.csscolor.WHEAT,
            font_size=24*self.SCREEN_HEIGHT/600,
            font_name=self.arcade_classic_font,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            "Lives".format(self.points),
            start_x=self.SCREEN_WIDTH*0.9,
            start_y=self.SCREEN_HEIGHT*0.55,
            color=arcade.csscolor.WHEAT,
            font_size=24*self.SCREEN_HEIGHT/600,
            font_name=self.arcade_classic_font,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )
        for i in range(self.pacman.lives):
            arcade.draw_arc_filled(self.SCREEN_WIDTH*(0.9-0.05*(i%3-1)),self.SCREEN_HEIGHT/22*(11-i//3),20,20,arcade.color.YELLOW,0,300,30)


    def on_update(self, delta_time):
        if self.game_running:
            if not self.pause and not self.dead:
                if self.godmod:
                    self.godmod_tick+=delta_time
                    if self.godmod_tick>self.godmod_time:
                        self.godmod_tick=0
                        self.godmod=False
                        arcade.stop_sound(self.god_song_play)
                self.pacman.Update(delta_time)
                self.event_on_get()
                time_to_release_incresed=False
                for i in range(self.ghost_num):
                    self.ghost[i].Update(delta_time)
                    if self.pacman.pos_on_map==self.ghost[i].pos_on_map:
                        if self.ghost[i].fear:
                            self.ghost[i].fear=False
                            self.ghost[i].fear_tick=0
                            self.ghost[i].make_captivity=True
                            self.points+=1000
                        else:
                            if self.ghost[i].free:
                                if self.pacman.lives>1:
                                    self.pacman.lives-=1
                                    arcade.stop_sound(self.god_song_play)
                                    arcade.stop_sound(self.play_chase)
                                    arcade.play_sound(self.death_song)
                                    self.dead=True
                                else:
                                    arcade.stop_sound(self.god_song_play)
                                    arcade.stop_sound(self.play_chase)
                                    arcade.play_sound(self.death_song)
                                    self.game_over=True
                                    self.dead=True
                    if not time_to_release_incresed and not self.ghost[i].free:
                        self.ghost[i].tick_to_release+=delta_time
                        time_to_release_incresed=True
            elif self.game_over:
                self.sorry_game_over(delta_time)
            elif self.dead:
                self.revive(delta_time)

            if self.restart:
                self.godmod_tick=0
                if self.godmod:
                    self.godmod=False   
                    arcade.sound.stop_sound(self.god_song_play)
                self.start_game()

        else:
            self.menu.on_update(4*delta_time)
            if self.menu.running:
                self.start_game()
                self.game_running=True

    def on_key_press(self, key, cos):
        if self.game_running:
            if key==self.pause_butt:
                self.pause=not self.pause
                if self.pause:
                    arcade.stop_sound(self.play_chase)
                else:
                    arcade.sound.stop_sound(self.play_chase)
                    self.play_chase = arcade.play_sound(self.pursuit[self.pursuit_level],self.music_volume,0,True)
            elif self.pause:
                self.pause=not self.pause
                self.play_chase = arcade.play_sound(self.pursuit[self.pursuit_level],self.music_volume,0,True)
            if not self.pause:
                self.pacman.Key_press(key)

        else:
            self.menu.key_press(key)
            

    def event_on_get(self):
        event=self.map[self.pacman.pos_on_map[0]][self.pacman.pos_on_map[1]]
        if event == 1:
            self.points +=10
            self.map[self.pacman.pos_on_map[0]][self.pacman.pos_on_map[1]]=-1
            if self.point_sound_tick:
                arcade.play_sound(self.small_point_sound,self.volume)
                self.point_sound_tick = not self.point_sound_tick
            else:
                arcade.play_sound(self.big_point_sound,self.volume)
                self.point_sound_tick = not self.point_sound_tick
        elif event == 2:
            self.points +=100
            self.map[self.pacman.pos_on_map[0]][self.pacman.pos_on_map[1]]=-1
            if not self.godmod:
                arcade.stop_sound(self.god_song_play)
                self.god_song_play = arcade.play_sound(self.godmod_sound,self.volume,0,True)
            self.godmod=True
            self.godmod_tick=0
            if self.point_sound_tick:
                arcade.play_sound(self.small_point_sound,self.volume)
                self.point_sound_tick = not self.point_sound_tick
            else:
                arcade.play_sound(self.big_point_sound,self.volume)
                self.point_sound_tick = not self.point_sound_tick
            for i in range(self.ghost_num):
                if self.ghost[i].free:
                    self.ghost[i].fear=True
                    self.ghost[i].fear_tick=0
        if self.pursuit_level/5>=self.points_left/self.points_number:
            self.pursuit_level+=1
            if self.pursuit_level>4:
                self.pursuit_level=4
            arcade.stop_sound(self.play_chase)
            self.play_chase=self.pursuit[self.pursuit_level]
            arcade.sound.stop_sound(self.play_chase)
            arcade.play_sound(self.play_chase,self.music_volume,0,True)


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
            self.scale,
            self.menu.pacman_speed,
            self.menu.pacman_lives)

        self.pacfont=self.menu.pacfont
        self.arcade_classic_font=self.menu.arcade_classic_font
        self.map_size=(len(self.map[0]),len(self.map))

        for i in range(1,self.map_size[1]-1):
            for j in range(1,self.map_size[0]-1):
                if self.map[i][j]==-1:
                    self.map[i][j]=1


        self.pause_text="Press to Start"
        self.pause=True

        self.map[self.menu.start_pos-1][len(self.map[0])//2]=-1
        self.map[self.menu.start_pos-1][len(self.map[0])//2-1]=-1
        self.map[1][1]=2
        self.map[1][-2]=2
        self.map[-2][1]=2
        self.map[-2][-2]=2

        self.points_number=sum(1 for i in range(len(self.map)) for j in range(len(self.map[0])) if self.map[i][j]>0)
        self.points_left=self.points_number

        self.ghost=[]
        self.ghost_num=self.menu.ghost_number
        color=[(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 0, 255),(255, 255, 0),(255, 255, 255),(181, 44, 0),(1, 255, 255),(164, 208, 46),(158, 58, 160)]
        for i in range(self.ghost_num):
            self.ghost.append(ghost.Ghost(self.menu.ghost_speed,self.map,self.pos,[1,1],self.scale,color[i], self.menu.fear_time,self.menu.time_to_release))

        self.volume=self.menu.volume/10
        self.music_volume = self.menu.music_volume/10
        self.godmod_time=self.menu.fear_time
        

        

    def pos(self,pos_on_map):
        
        a=self.SCREEN_WIDTH*0.3+self.im_height/2*self.scale-self.im_height*(pos_on_map[0]+1)/self.map_size[1]*self.scale+self.pac_size/2
        b=self.SCREEN_WIDTH*0.4+self.im_width/2*self.scale-self.im_width*(self.map_size[0]-pos_on_map[1])/self.map_size[0]*self.scale+self.pac_size/2
        return [b,a]

    def revive(self,delta_time):
        if self.death_tick>3:
            self.ghost=[]
            color=[(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 0, 255),(255, 255, 0),(255, 255, 255),(181, 44, 0),(1, 255, 255),(164, 208, 46),(158, 58, 160)]
            for i in range(self.ghost_num):
                self.ghost.append(ghost.Ghost(self.menu.ghost_speed,self.map,self.pos,[1,1],self.scale,color[i], self.menu.fear_time,self.menu.time_to_release))
            
            self.pacman.pos_on_map=[self.menu.start_pos-1,len(self.map[0])//2]
            self.pause=True
            self.dead=False
            self.down=0
            self.right=-1/2
            self.death_tick=0
            self.direction=1
            arcade.stop_sound(self.god_song_play)
            arcade.stop_sound(self.play_chase)
        else:
            self.death_tick+=delta_time
            
    def sorry_game_over(self,delta_tick):
        self.game_over_tick+=delta_tick
        self.pause=True
        self.pause_text="GAME OVER"
        if self.game_over_tick>3:
            self.game_over=False
            self.game_running=False
            self.dead=False
            self.menu.before_death(self.points)
            self.menu = main_menu.Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            arcade.stop_sound(self.god_song_play)
            arcade.stop_sound(self.play_chase)

def main():
    """ Start the game """
    window = MyGame(800, 600, "Pac-man")
    arcade.run()


if __name__ == "__main__":
    main()