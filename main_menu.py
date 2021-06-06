import arcade
import map
from PIL import Image

class Menu:
    def __init__(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        arcade.set_background_color(arcade.color.BLACK)

        self.map_size=[9,5]

        self.game_prep_tick=0

        self.right_key=arcade.key.RIGHT
        self.left_key=arcade.key.LEFT
        self.down_key=arcade.key.DOWN
        self.up_key=arcade.key.UP

        self.running=False
        self.pacfont="fonts/PAC-FONT"
        self.arcade_classic_font="fonts/ArcadeClassic"
        self.path=["main_menu"]

        self.main_menu = True
        self.play = False
        self.scoreboard = False
        self.settings = False
        self.autor = False
        self.how_to=False
        self.switch_buffor=""
        self.lets_the_game_begin=False

        self.player = 1

        self.choose = "Play"
        self.choose_number = 0
        self.menu_options = ["Play","How to Play", "Settings", "Scoreboard", "Autors", "Quit"]
        self.settings_options = ["Keyboard", "Sound", "Back"]
        self.play_options=["Play", "1 player", "Map", "Game settings","Back"]
        self.options=self.menu_options

        self.changed=False
        self.switch=False
        self.switch_left=True
        self.switch_pos=-100
        self.switch_rotation=0
        self.tick=0
        self.tick_up=True

    def Draw(self):
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
            if self.main_menu: # and not self.switch:
                for i in range(len(self.options)-1):
                    color=arcade.csscolor.WHITE_SMOKE
                    if i == self.choose_number:
                        color=arcade.csscolor.YELLOW
                        arcade.draw_arc_filled(self.SCREEN_WIDTH/4*3,self.SCREEN_HEIGHT/11*(7-i),40,40,arcade.color.YELLOW,0,300,30)
                        arcade.draw_arc_filled(self.SCREEN_WIDTH/4,self.SCREEN_HEIGHT/11*(7-i),40,40,arcade.color.YELLOW,0,300,30)

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
                arcade.draw_arc_filled(self.SCREEN_WIDTH/4*3,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
                arcade.draw_arc_filled(self.SCREEN_WIDTH/4,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
        else:
            if self.game_prep_tick<2:
                arcade.draw_arc_filled(self.SCREEN_WIDTH/4*3,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
                arcade.draw_arc_filled(self.SCREEN_WIDTH/4,self.SCREEN_HEIGHT/11*7,40,40,arcade.color.YELLOW,0,300,30)
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
                
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4+(self.SCREEN_WIDTH/4*3-self.SCREEN_WIDTH*0.4)*(5-self.game_prep_tick)/3,
                    destination-(destination-self.SCREEN_HEIGHT/11*7)*(5-self.game_prep_tick)/3,
                    self.pac_size+24*(5-self.game_prep_tick)/3,self.pac_size+24*(5-self.game_prep_tick)/3,
                    arcade.color.YELLOW,0,300,
                    30+90*(self.game_prep_tick-2)/3)
                arcade.draw_arc_filled(self.SCREEN_WIDTH*0.4+(self.SCREEN_WIDTH/4*1-self.SCREEN_WIDTH*0.4)*(5-self.game_prep_tick)/3,
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
                    self.play = True
                    self.options = self.play_options
                    self.path.append("self.play")

                elif self.choose == "Settings":
                    self.settings = True
                    self.options=self.settings_options
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    self.path.append("self.settings")

                elif self.choose == "Autors":
                    self.autor == True
                    self.path.append("self.autor")

                elif self.choose == "How to Play":
                    self.how_to= True
                    self.path.append("self.how_to")

                elif self.choose == "Scoreboard":
                    self.scoreboard=True
                    self.path.append("self.scoreboard")

                elif self.choose == "Back":
                    self.options=self.menu_options
                    self.choose_number=len(self.options)-1
                    self.choose=self.options[self.choose_number]
                    exec(self.path[-1]+" = False")
        elif self.lets_the_game_begin:
            self.game_prep_tick+=delta_time

    def key_press(self, key):
        if not self.switch and not self.lets_the_game_begin:
            if key == arcade.key.DOWN:
                self.choose_number=(self.choose_number + 1)%len(self.options)
                self.choose=self.options[self.choose_number]
            elif key == arcade.key.UP:
                self.choose_number=(self.choose_number - 1)%len(self.options)
                self.choose=self.options[self.choose_number]

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
                
                elif self.choose=="Play" and self.play==True and not self.lets_the_game_begin:
                    self.lets_the_game_begin=True
                    self.prepare_game()

                elif self.choose == "Back":
                    self.switch=True
                    self.switch_pos=self.SCREEN_WIDTH+self.SCREEN_HEIGHT/11*4
                    self.switch_left=False
                    self.switch_rotation=180
                    self.switch_buffor=self.choose
                else:
                    #print("Zapomiałme o ", key)
                    self.switch_buffor=self.choose

    def prepare_game(self):
        self.map_im, self.map=map.map_background_generation(self.map_size[0],self.map_size[1])
        width, height = self.map_im.size
        if height/1.5>self.SCREEN_HEIGHT*0.8 or width/1.5>self.SCREEN_WIDTH*0.8:
            self.scroll=True
            self.scale=1
        else:
            #self.scroll=False
            self.scale=min(self.SCREEN_HEIGHT*0.8/height,self.SCREEN_WIDTH*0.8/width)
            #self.map_start = [self.SCREEN_WIDTH*0.4*(1-self.scale),self.SCREEN_HEIGHT*0.4*(1-self.scale)]
            #self.map_end = [self.SCREEN_WIDTH*0.4*(1+self.scale),self.SCREEN_HEIGHT*0.4*(1+self.scale)]
        self.background=arcade.Texture("whatever",self.map_im)
        
        n=len(self.map[0])//2
        i=int(len(self.map)//2)+1
        while True:
            i+=1
            if self.map[i][n]==1:
                self.start_pos=i+1
                break
        self.pac_size=20*self.scale
"""        import matplotlib.pyplot as plt
        self.map[i][n]=3
        plt.imshow(self.map,cmap='hot')
        plt.show()"""
