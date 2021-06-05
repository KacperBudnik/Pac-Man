import arcade


class Menu:
    def __init__(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        arcade.set_background_color(arcade.color.BLACK)
        self.running=False
        self.pacfont="fonts/PAC-FONT"
        self.arcade_classic_font="fonts/ArcadeClassic"
        self.path=["main_menu"]

        self.main_menu = True
        self.scoreboard = False
        self.settings = False
        self.autor = False
        self.how_to=False
        self.switch_buffor=""

        self.choose = "Play"
        self.choose_number = 0
        self.menu_options = ["Play","How to Play", "Settings", "Scoreboard", "Autors", "Quit"]
        self.settings_options = ["Keyboard","Sound", "Back"]
        self.options=self.menu_options

        self.changed=False
        self.switch=False
        self.switch_left=True
        self.switch_pos=-100
        self.switch_rotation=0
        self.tick=0
        self.tick_up=True

    def Draw(self):
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
                if self.choose == "Settings":
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
                    exec(self.path[-1]+"=False")
                    self.path.pop()
            


    def key_press(self, key):
        if not self.switch:
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
                
                if self.choose == "Play":
                    self.running=True

                elif self.choose == "Quit":
                    arcade.close_window()

                elif self.choose == "Back":
                    self.switch=True
                    self.switch_pos=self.SCREEN_WIDTH+self.SCREEN_HEIGHT/11*4
                    self.switch_left=False
                    self.switch_rotation=180
                    self.switch_buffor=self.choose
                else:
                    #print("Zapomiałme o ", key)
                    self.switch_buffor=self.choose




