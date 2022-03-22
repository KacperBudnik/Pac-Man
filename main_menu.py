import arcade
import map
from PIL import Image
import os
import webbrowser

class Menu:
    """ Main Menu class"""
    def __init__(self, width, height):
        """ Initializing main menu
            :param:
                width (int): width of screen
                height (int): height of screen"""
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        arcade.set_background_color(arcade.color.BLACK)

        self.map_size=[9,5]

        self.user_name=os.path.basename(os.path.expanduser("~"))

        self.game_prep_tick=0

        self.right_key=arcade.key.RIGHT
        self.left_key=arcade.key.LEFT
        self.down_key=arcade.key.DOWN
        self.up_key=arcade.key.UP

        self.running=False
        self.pacfont="assets/fonts/PAC-FONT"
        self.arcade_classic_font="assets/fonts/ArcadeClassic"
        self.path=["self.menu_options"]

        self.main_menu = True
        self.switch_buffor=""
        self.lets_the_game_begin=False

        self.fear_time=5
        self.ghost_number=4
        self.ghost_speed=4
        self.pacman_speed=5
        self.pacman_lives=3
        self.time_to_release=5

        self.player = 1

        self.choose = "Play"
        self.choose_number = 0
        self.menu_options = ["Play","How to Play", "Settings", "Scoreboard", "Autors", "Quit"]
        #self.menu_options = ["Play","How to Play", "Scoreboard", "Autors", "Quit"]
        self.settings_options = ["Keyboard", "Sound", "Back"]
        self.sound_options = ["Volume   10", "Music Volume   10","Back"]
        #self.play_options=["Play", "1 player", "Map", "Game settings","Back"]
        self.play_options=["Play", "Map","Game settings","Back"]
        self.game_settings=["Normal","Ghosts number   4","Ghost Speed   4","PacMan Speed   5", "PacMan Lives   3","Fear Time   5", "Back"]
        self.map_options=["Map width   9","Map height   9","Back"]
        self.keyboard_settings=["UP   UpArrow","DOWN   DownArrow","RIGHT   RightArrow","LEFT   LeftArrow","Back"]
        self.autor_options=["Autor","Kacper Budnik","Sounds","findsounds","classicgaming","Back"]
        self.options=self.menu_options

        self.changed=False
        self.switch=False
        self.switch_left=True
        self.switch_pos=-100
        self.switch_rotation=0
        self.tick=0
        self.tick_up=True


        self.rank_points=[]
        self.rank_name=[]

        try:
            with open("assets/data/rank_points","r") as f:
                self.rank_points = [int(x) for x in f]
            with open("assets/data/rank_name","r") as f:
                self.rank_name=f.read().splitlines()
        except:
            self.rank_points = [0 for i in range(5)]
            self.rank_name = ["Empty" for i in range(5)]
        
        if len(self.rank_name)<5 or len(self.rank_points)<5:
            a=min(len(self.rank_name),len(self.rank_points))
            self.rank_name = self.rank_name[:a]
            self.rank_points = self.rank_points[:a]
            for i in range(5-a):
                self.rank_name.append("Empty")
                self.rank_points.append(0)

        self.volume=10
        self.music_volume=10

        self.rank=[]
        for i in range(min(len(self.rank_points),len(self.rank_name),5)):
            self.rank.append(str(self.rank_name[i]+"    "+str(self.rank_points[i])))
        self.rank.append("Back")

    def Draw(self):
        """ Draw main menu """
        if not self.lets_the_game_begin or self.switch:
            arcade.draw_text(
                "Pac Man",
                start_x=self.SCREEN_WIDTH/2,
                start_y=self.SCREEN_HEIGHT/11*9,
                color=arcade.csscolor.YELLOW,
                font_size=48*self.SCREEN_HEIGHT/600,
                font_name=self.pacfont,
                align="center",
                anchor_x="center",
                anchor_y="center"
            )

            if self.main_menu:
                for i in range(len(self.options)-1):
                    color=arcade.csscolor.WHITE_SMOKE
                    if i == self.choose_number:
                        color=arcade.csscolor.YELLOW
                        arcade.draw_arc_filled(self.SCREEN_WIDTH/5*4,self.SCREEN_HEIGHT/11*(7-i),40,40,arcade.color.YELLOW,0,300,30)
                        arcade.draw_arc_filled(self.SCREEN_WIDTH/5,self.SCREEN_HEIGHT/11*(7-i),40,40,arcade.color.YELLOW,0,300,30)

                    arcade.draw_text(
                        self.options[i],
                        start_x=self.SCREEN_WIDTH/2,
                        start_y=self.SCREEN_HEIGHT/11*(7-i),
                        color=color,
                        font_size=40*self.SCREEN_HEIGHT/600,
                        font_name=self.arcade_classic_font,
                        align="center",
                        anchor_x="center",
                        anchor_y="center"
                    )

                    last_number=len(self.options)-1
                    color=arcade.csscolor.WHITE_SMOKE
                    if last_number == self.choose_number:
                        color=arcade.csscolor.YELLOW
                        arcade.draw_arc_filled(self.SCREEN_WIDTH/4*3,self.SCREEN_HEIGHT/11,40,40,arcade.color.YELLOW,0,300,30)
                        arcade.draw_arc_filled(self.SCREEN_WIDTH/4,self.SCREEN_HEIGHT/11,40,40,arcade.color.YELLOW,0,300,30)

                    arcade.draw_text(
                        self.options[last_number],
                        start_x=self.SCREEN_WIDTH/2,
                        start_y=self.SCREEN_HEIGHT/11,
                        color=color,
                        font_size=40*self.SCREEN_HEIGHT/600,
                        font_name=self.arcade_classic_font,
                        align="center",
                        anchor_x="center",
                        anchor_y="center"
                    )
            if self.switch:
                arcade.draw_arc_filled(self.switch_pos,self.SCREEN_HEIGHT/11*4.25,
                    self.SCREEN_HEIGHT/11*8,self.SCREEN_HEIGHT/11*8,
                    arcade.color.YELLOW,0,
                    360-self.tick*2,self.switch_rotation+self.tick)
            if self.lets_the_game_begin:
                arcade.draw_arc_filled(self.SCREEN_WIDTH/5*4,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
                arcade.draw_arc_filled(self.SCREEN_WIDTH/5,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
        else: # Start Game - animation
            if self.game_prep_tick<2:
                arcade.draw_arc_filled(self.SCREEN_WIDTH/5*4,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
                arcade.draw_arc_filled(self.SCREEN_WIDTH/5,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
                arcade.draw_text(
                    "Pac Man",
                    start_x=self.SCREEN_WIDTH/2,
                    start_y=self.SCREEN_HEIGHT/11*(9+self.game_prep_tick/2),
                    color=arcade.csscolor.YELLOW,
                    font_size=48*self.SCREEN_HEIGHT/600,
                    font_name=self.pacfont,
                    align="center",
                    anchor_x="center",
                    anchor_y="center"
                )
            elif self.game_prep_tick<=5:
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
                destination=self.SCREEN_WIDTH*0.3+self.map_im.size[1]/2*self.scale-self.map_im.size[1]*self.start_pos/len(self.map)*self.scale+self.pac_size/2
                
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4+(self.SCREEN_WIDTH/5*4-self.SCREEN_WIDTH*0.4)*(5-self.game_prep_tick)/3,
                    destination-(destination-self.SCREEN_HEIGHT/11*7)*(5-self.game_prep_tick)/3,
                    self.pac_size+24*(5-self.game_prep_tick)/3,self.pac_size+24*(5-self.game_prep_tick)/3,
                    arcade.color.YELLOW,0,300,
                    30+90*(self.game_prep_tick-2)/3)
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4+(self.SCREEN_WIDTH/5*1-self.SCREEN_WIDTH*0.4)*(5-self.game_prep_tick)/3,
                    destination-(destination-self.SCREEN_HEIGHT/11*7)*(5-self.game_prep_tick)/3,
                    self.pac_size+24*(5-self.game_prep_tick)/3,self.pac_size+24*(5-self.game_prep_tick)/3,
                    arcade.color.YELLOW,0,300,
                    30+90*(self.game_prep_tick-2)/3)
            elif self.game_prep_tick<=8:
                self.background.draw_scaled(self.SCREEN_WIDTH*0.4,self.SCREEN_HEIGHT*0.4,self.scale,0,255*(self.game_prep_tick-5)/3)
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4,
                #self.SCREEN_WIDTH*0.3+self.map_im.size[1]/2-self.map_im.size[1]*self.start_pos/len(self.map)*self.scale+self.pac_size/2,
                    self.SCREEN_WIDTH*0.3+self.map_im.size[1]/2*self.scale-self.map_im.size[1]*self.start_pos/len(self.map)*self.scale+self.pac_size/2,
                    self.pac_size,self.pac_size,
                    arcade.color.YELLOW,0,300,
                    120)
                arcade.draw_rectangle_filled(self.SCREEN_WIDTH*0.5,self.SCREEN_HEIGHT*0.9,self.SCREEN_WIDTH,self.SCREEN_HEIGHT*0.2,arcade.color.BLACK)
                arcade.draw_rectangle_filled(self.SCREEN_WIDTH*0.9,self.SCREEN_HEIGHT*0.5,self.SCREEN_WIDTH*0.2,self.SCREEN_HEIGHT,arcade.color.BLACK)
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
            elif self.game_prep_tick<=10:
                width,height=self.map_im.size
                self.background.draw_scaled(self.SCREEN_WIDTH*0.4,self.SCREEN_HEIGHT*0.4,self.scale,0)
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4,
                    self.SCREEN_WIDTH*0.3+height/2*self.scale-height*self.start_pos/len(self.map)*self.scale+self.pac_size/2,
                    self.pac_size,self.pac_size,arcade.color.YELLOW,0,300,120)
                arcade.draw_rectangle_filled(self.SCREEN_WIDTH*0.5,self.SCREEN_HEIGHT*0.9,self.SCREEN_WIDTH,self.SCREEN_HEIGHT*0.2,(0,0,15*(self.game_prep_tick-8)))
                arcade.draw_rectangle_filled(self.SCREEN_WIDTH*0.9,self.SCREEN_HEIGHT*0.5,self.SCREEN_WIDTH*0.2,self.SCREEN_HEIGHT,(0,0,15*(self.game_prep_tick-8)))
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
            else:
                self.running=True
                width,height=self.map_im.size
                self.background.draw_scaled(self.SCREEN_WIDTH*0.4,self.SCREEN_HEIGHT*0.4,self.scale,0)
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4,
                    self.SCREEN_WIDTH*0.3+height/2*self.scale-height*self.start_pos/len(self.map)*self.scale+self.pac_size/2,
                    self.pac_size,self.pac_size,arcade.color.YELLOW,0,300,120)
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
        """ Update main menu
            :param:
                delta_time (float): time since the last execution of the function"""
        change=False
        if self.switch:
            if self.tick_up:
                self.tick+=60*delta_time
                if self.tick>=30:
                    self.tick_up=False
            else:
                self.tick-=60*delta_time
                if self.tick<=0:
                    self.tick_up=True


            if self.switch_left:
                self.switch_pos+=60*delta_time*5*self.SCREEN_WIDTH/800
                if self.switch_pos > self.SCREEN_WIDTH+self.SCREEN_HEIGHT/11*4:
                    self.switch=False
                if self.switch_pos>self.SCREEN_WIDTH/2:
                    change=True
            else:
                self.switch_pos-=60*delta_time*5*self.SCREEN_WIDTH/800
                if self.switch_pos < -self.SCREEN_HEIGHT/11*4:
                    self.switch=False
                if self.switch_pos<self.SCREEN_WIDTH/2:
                    change=True


            if change and not self.changed:
                self.changed=True
                if self.lets_the_game_begin:
                    self.options=[]

                elif self.choose == "Play":
                    self.options = self.play_options
                    self.path.append("self.play_options")

                elif self.choose == "Map":
                    self.map_settings=True
                    self.options = self.map_options
                    self.path.append("self.map_options")
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]

                elif self.choose == "Settings":
                    self.options=self.settings_options
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.settings_options")

                elif self.choose == "Autors":
                    self.options=self.autor_options
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.autor_options")

                elif self.choose == "How to Play":
                    self.how_to= True
                    #self.path.append("self.how_to")

                elif self.choose == "Scoreboard":
                    self.options=self.rank
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.rank")

                elif self.choose == "Keyboard":
                    self.options=self.keyboard_settings
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.keyboard_settings")

                elif self.choose == "Sound":
                    self.options=self.sound_options
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.sound_options")

                elif self.choose == "Game settings":
                    self.options=self.game_settings
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.game_settings")

                elif self.choose == "Back":
                    exec("self.options = " + self.path[-2])
                    self.path.pop()
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]

                    
        elif self.lets_the_game_begin:
            self.game_prep_tick+=delta_time

    def key_press(self, key):
        """ Called whenever a key is pressed in main menu
            :param:
                key (int): kod of pressed key"""
        if not self.switch and not self.lets_the_game_begin:
            if key == arcade.key.DOWN:
                self.choose_number=(self.choose_number + 1)%len(self.options)
                self.choose=self.options[self.choose_number]

            elif key == arcade.key.UP:
                self.choose_number=(self.choose_number - 1)%len(self.options)
                self.choose=self.options[self.choose_number]

            elif key == arcade.key.RIGHT:
                if self.choose[:9] =="Map width":
                    self.map_size[1]+=1
                    if self.map_size[1]>10:
                        self.map_size[1]=10
                    d="   "+str(self.map_size[1]*2-1)
                    self.map_options[0]="Map width"+d[-4:]
                elif self.choose[:9] =="Map heigh":
                    self.map_size[0]+=1
                    if self.map_size[0]>14:
                        self.map_size[0]=14
                    d="   "+str(self.map_size[0])
                    self.map_options[1]="Map height"+d[-4:]
                
                if self.choose[:13]=="Ghosts number":
                    self.ghost_number+=1
                    if self.ghost_number>10:
                        self.ghost_number=10
                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                elif self.choose[:11]=="Ghost Speed":
                    self.ghost_speed+=1
                    if self.ghost_speed>7:
                        self.ghost_speed=7
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                elif self.choose[:12]=="PacMan Speed":
                    self.pacman_speed+=1
                    if self.pacman_speed>10:
                        self.pacman_speed=10
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                elif  self.choose[:12]=="PacMan Lives":
                    self.pacman_lives+=1
                    if self.pacman_lives>10:
                        self.pacman_lives=10
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                elif self.choose[:9]=="Fear Time":
                    self.fear_time+=1
                    if self.fear_time>15:
                        self.fear_time=15
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)

                if self.choose[:6]=="Volume":
                    self.volume+=1
                    if self.volume>10:
                        self.volume=10
                    self.sound_options[0]="Volume   "+str(self.volume)
                elif self.choose[:12]=="Music Volume":
                    self.music_volume+=1
                    if self.music_volume>10:
                        self.music_volume=10
                    self.sound_options[1]="Music Volume   "+str(self.music_volume)

                if self.choose == "Normal":
                    self.game_settings[0]="Hard"
                    self.ghost_number = 8
                    self.ghost_speed = 5
                    self.pacman_speed = 4
                    self.pacman_lives = 1
                    self.fear_time = 0
                    self.choose="Hard"
                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)
                elif self.choose == "Hard":
                    self.game_settings[0]="Endless"
                    self.ghost_number = 0
                    self.pacman_lives = 10
                    self.pacman_speed = 7
                    self.fear_time = 0
                    self.choose="Endless"

                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)
                elif self.choose == "Endless":
                    self.game_settings[0]="Easy"
                    self.ghost_number = 2
                    self.pacman_lives = 5
                    self.pacman_speed = 5
                    self.ghost_speed = 2
                    self.fear_time = 10
                    self.choose="Easy"

                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)
                elif self.choose == "Easy":
                    self.game_settings[0]="Normal"
                    self.fear_time=5
                    self.ghost_number=4
                    self.ghost_speed=4
                    self.pacman_speed=5
                    self.pacman_lives=3
                    self.choose="Normal"
                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)

            elif key == arcade.key.LEFT:
                if self.choose[:9] =="Map width":
                    self.map_size[1]-=1
                    if self.map_size[1]<2:
                        self.map_size[1]=2
                    d="   "+str(self.map_size[1]*2-1)
                    self.map_options[0]="Map width"+d[-4:]
                elif self.choose[:9] =="Map heigh":
                    self.map_size[0]-=1
                    if self.map_size[0]<2:
                        self.map_size[0]=2
                    d="   "+str(self.map_size[0])
                    self.map_options[1]="Map height"+d[-4:]

                if self.choose[:13]=="Ghosts number":
                    self.ghost_number-=1
                    if self.ghost_number<0:
                        self.ghost_number=0
                    self.game_settings[0]="Ghosts number   "+str(self.ghost_number)
                elif self.choose[:11]=="Ghost Speed":
                    self.ghost_speed-=1
                    if self.ghost_speed<1:
                        self.ghost_speed=1
                    self.game_settings[1]="Ghost Speed   "+str(self.ghost_speed)
                elif self.choose[:12]=="PacMan Speed":
                    self.pacman_speed-=1
                    if self.pacman_speed<1:
                        self.pacman_speed=1
                    self.game_settings[2]="PacMan Speed   "+str(self.pacman_speed)
                elif  self.choose[:12]=="PacMan Lives":
                    self.pacman_lives-=1
                    if self.pacman_lives<1:
                        self.pacman_lives=1
                    self.game_settings[3]="PacMan Lives   "+str(self.pacman_lives)
                elif self.choose[:9]=="Fear Time":
                    self.fear_time-=1
                    if self.fear_time<0:
                        self.fear_time=0
                    self.game_settings[4]="Fear Time   "+str(self.fear_time)

                if self.choose[:6]=="Volume":
                    self.volume-=1
                    if self.volume<0:
                        self.volume=0
                    self.sound_options[0]="Volume   "+str(self.volume)
                elif self.choose[:12]=="Music Volume":
                    self.music_volume-=1
                    if self.music_volume<0:
                        self.music_volume=0
                    self.sound_options[1]="Music Volume   "+str(self.music_volume)

                if self.choose == "Endless":
                    self.game_settings[0]="Hard"
                    self.ghost_number = 8
                    self.ghost_speed = 5
                    self.pacman_speed = 4
                    self.pacman_lives = 1
                    self.fear_time = 0
                    self.choose="Hard"
                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)
                elif self.choose == "Easy":
                    self.game_settings[0]="Endless"
                    self.ghost_number = 0
                    self.pacman_lives = 10
                    self.pacman_speed = 7
                    self.fear_time = 0
                    self.choose="Endless"

                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)
                elif self.choose == "Normal":
                    self.game_settings[0]="Easy"
                    self.ghost_number = 2
                    self.pacman_lives = 5
                    self.pacman_speed = 5
                    self.ghost_speed = 2
                    self.fear_time = 10
                    self.choose="Easy"

                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)
                elif self.choose == "Hard":
                    self.game_settings[0]="Normal"
                    self.fear_time=5
                    self.ghost_number=4
                    self.ghost_speed=4
                    self.pacman_speed=5
                    self.pacman_lives=3
                    self.choose="Normal"
                    self.game_settings[1]="Ghosts number   "+str(self.ghost_number)
                    self.game_settings[2]="Ghost Speed   "+str(self.ghost_speed)
                    self.game_settings[3]="PacMan Speed   "+str(self.pacman_speed)
                    self.game_settings[4]="PacMan Lives   "+str(self.pacman_lives)
                    self.game_settings[5]="Fear Time   "+str(self.fear_time)


            if key == arcade.key.ENTER or key==arcade.key.SPACE:
                self.changed=False
                self.switch=True
                self.switch_pos=-self.SCREEN_HEIGHT/11*4
                self.switch_left=True
                self.switch_rotation=0
                
                if self.choose == "Quit":
                    arcade.close_window()
                
                elif self.choose[1:]==" player":
                    self.switch=False
                    if self.player==1:
                        self.player=2
                        self.choose="2 player"
                        self.play_options[1]="2 player"
                    else:
                        self.player=1
                        self.choose="1 player"
                        self.play_options[1]="1 player"
                
                elif self.choose=="Play" and self.options==self.play_options and not self.lets_the_game_begin:
                    self.lets_the_game_begin=True
                    self.prepare_game()

                elif self.choose == "Back":
                    self.switch=True
                    self.switch_pos=self.SCREEN_WIDTH+self.SCREEN_HEIGHT/11*4
                    self.switch_left=False
                    self.switch_rotation=180
                    self.switch_buffor=self.choose

                elif self.choose=="findsounds":
                    webbrowser.open("https://www.findsounds.com/")
                    self.changed=True
                    self.switch=False

                elif self.choose=="classicgaming":
                    webbrowser.open("https://www.classicgaming.cc/")
                    self.changed=True
                    self.switch=False
                
                elif self.choose == "How to Play":
                    os.system('start assets/"How to Play.pdf"')
                    self.changed=True
                    self.switch=False

                elif self.options==self.map_options: 
                    self.changed=True
                    self.switch=False
                
                elif self.options==self.game_settings:
                    self.changed=True
                    self.switch=False
                
                elif self.options==self.keyboard_settings:
                    self.changed=True
                    self.switch=False

                elif self.options==self.sound_options:
                    self.changed=True
                    self.switch=False

                elif self.options==self.autor_options:
                    self.changed=True
                    self.switch=False

                elif self.options==self.rank:
                    self.changed=True
                    self.switch=False
                
                else:
                    self.switch_buffor=self.choose

    def prepare_game(self):
        """ Activeted when play was pressed, generating map"""
        self.map_im, self.map=map.map_background_generation(self.map_size[0],self.map_size[1])
        width, height = self.map_im.size

        self.scale=min(self.SCREEN_HEIGHT*0.8/height,self.SCREEN_WIDTH*0.8/width)

        self.background=arcade.Texture("whatever",self.map_im)
        
        n=len(self.map[0])//2
        i=int(len(self.map)//2)+1
        while True:
            i+=1
            if self.map[i][n]==1:
                self.start_pos=i+1
                break
        self.pac_size=20*self.scale


    def before_death(self, points):
        """ After pacman death save his score and write in file if he was in top5
            "param:
                points (int): score"""
        for i in range(5):
            if points>self.rank_points[i]:
                for j in range(1,5-i):
                    self.rank_points[5-j]=self.rank_points[4-j]
                    self.rank_name[5-j]=self.rank_name[4-j]
                self.rank_points[i]=points
                self.rank_name[i]=self.user_name
                break
        
        with open("assets/data/rank_points","w") as f:
            for i in self.rank_points:
                f.write(str(i)+"\n")
        with open("assets/data/rank_name","w") as f:
            for i in self.rank_name:
                f.write(str(i)+"\n")
