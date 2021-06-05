import arcade



class Pac_man:
    """ Main application class. """

    def __init__(self):
        self.right_key=arcade.key.RIGHT
        self.left_key=arcade.key.LEFT
        self.down_key=arcade.key.DOWN
        self.up_key=arcade.key.UP

        self.game_running=False
        self.pause=True



        self.test=0
        self.up=True

        self.rotation=0
        self.x_pos=400  
        self.y_pos=300
    

    def Draw(self):
        arcade.draw_arc_filled(self.x_pos,self.y_pos,50,50,arcade.color.YELLOW,0,360-self.test*2,self.rotation+self.test)

        
    def Update(self, delta_time):
        if self.up:
            self.test+=60*delta_time
            if self.test>30:
                self.up=False
        else:
            self.test-=60*delta_time
            if self.test<=0:
                self.up=True

        if self.rotation==0:
            self.x_pos+=60*delta_time
        elif self.rotation==90:
            self.y_pos+=60*delta_time
        elif self.rotation==180:
            self.x_pos-=60*delta_time
        elif self.rotation == 270:
            self.y_pos-=60*delta_time

        


    def Key_press(self, key):
        if key == self.right_key:
            self.rotation=0
        elif key == self.left_key:
            self.rotation=180
        elif key == self.up_key:
            self.rotation=90
        elif key == self.down_key:
            self.rotation=270
