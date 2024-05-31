import pygame, random
p = pygame

class Game:
    def __init__(self, screen, fps):
        self.screen = screen
        self.fps = fps
        self.background = 'black'
        self.actual_screen = 'welcome'
        self.MARGIN_Y = 100

        # menu
        self.welcome_screen = p.image.load("assets/Welcome_screen.png")
        self.loose_screens = {"sad": p.image.load("assets/Loose_screen_sad.png"), "happy": p.image.load("assets/Loose_screen_happy.png")}
        self.button_x = 296
        self.button_y = 440
        self.button_width = 210
        self.button_height = 170
        self.button_extension_coef = 1.1
        self.play_button = Button(self, "Play", self.button_x, self.button_y)
        self.replay_button = Button(self, "Replay", self.button_x, self.button_y)
        self.loose_font = p.font.SysFont("Poppins", 65)
        self.loose_font_y = 230
        self.loose_font_color = 'orange'

        # timer
        self.TIMER_MAX = 45*self.fps
        self.TIME_PUNITION = 25*self.fps
        self.timer = self.TIMER_MAX
        self.rect_height = 110
        self.rect_x = 0
        self.rect_y = 65


        # apples
        self.MAX_ROUND = 6
        self.ADD_SAD = 3
        self.BLINK_TIMER_OF = (2, 6)
        self.BLINK_TIMER_ON = (0.1, 1.2)
        self.BLINK_START_TIMER = (0, 2.5)
        self.apple_size = 100
        self.apples = []
        self.apple_width = 2
        self.apple_height = 2
        self.num_apples = self.apple_height*self.apple_width
        self.orientations = [0, 90, 180, 270]
        self.number_sad = 1
        self.new_happy = 0
        self.apple_happy = 0
        self.colors_apples = ["red", "yellow", "orange", "lightgreen", "green", "pink", "purple", "blue"]

        self.start()

        # score
        self.point = 0
        self.score_text = pygame.font.SysFont("Arial",  65)
        self.score_text_color = "white"
        self.score_text_x = 0
        self.score_text_y = 0

    def reset(self):
        self.point = -1
        self.number_sad = 1
        self.apple_happy = 0
        self.restart()

    def set_coos(self, number_width, number_height):
        x = []
        y = []
        coos = []
        if number_width % 2 == 0:
            num_apple = int(number_width/2) # number of apple on the left side (the same on the right side)
            for i in range(1, num_apple+1)[::-1]:
                # create the left x
                x.append(self.screen.get_width()/2-self.apple_size*i)
                # create the right x
                x.append(self.screen.get_width()/2+self.apple_size*(i-1))
        if number_height % 2 == 0:
            num_apple = int(number_height / 2)  # number of apple on the top side (the same on the bottom side)
            for i in range(1, num_apple + 1)[::-1]:
                # create the top y
                y.append(self.screen.get_height() / 2 - self.apple_size * i + self.MARGIN_Y)
                # create the bottom y
                y.append(self.screen.get_height() / 2 + self.apple_size * (i - 1) + self.MARGIN_Y)
            # sort coos
            x.sort()
            y.sort()
            # create all the coos (combinaisons)
            for x_ in x:
                for y_ in y:
                    coos.append((x_, y_))
            return coos
    def restart(self):
        self.timer = self.TIMER_MAX
        self.apples = []
        self.apple_happy += self.new_happy
        self.new_happy = 0
        self.point += 1
        self.coos = []
        if self.point % self.ADD_SAD == 0:
            self.number_sad += 1
            if self.number_sad > 3:
                if self.num_apples <= 5*5:
                    self.number_sad = 1
                    self.apple_width += 2
                    self.apple_height += 2
                elif self.num_apples == 6*6:
                    self.number_sad = 1
                    self.apple_width += 2
                self.num_apples = self.apple_height * self.apple_width

        self.start()
    def start(self):
        color = ""
        color_ = ""
        self.coos = self.set_coos(self.apple_width, self.apple_height)
        for coo in self.coos:
            while color == color_:
                color = random.choice(self.colors_apples)
            color_ = color
            self.apples.append(Apple(self, "happy", color, coo[0], coo[1]))
        for n in range(self.number_sad):
            apple = random.choice(self.apples)
            while apple.state == 'sad':
                apple = random.choice(self.apples)
            apple.state = 'sad'
            apple.imgs = apple.imgs_sad


    def update(self):
        self.screen.fill(self.background)
        if self.actual_screen == 'welcome':
            self.screen.blit(self.welcome_screen, (0, 0))
            self.screen.blit(self.play_button.image, (self.play_button.rect.x, self.play_button.rect.y))
        elif self.actual_screen == 'game':
            for apple in self.apples:
                apple.blink()
                self.screen.blit(apple.img, (apple.rect.x, apple.rect.y))
            if self.new_happy == self.number_sad:
                self.restart()
            rect_width = (self.timer/self.TIMER_MAX)*self.screen.get_width()
            rect = pygame.draw.rect(self.screen, self.rect_color(rect_width), (self.rect_x, self.rect_y, rect_width, self.rect_height))
            self.screen.blit(self.score_text.render(str(self.point), True, self.score_text_color), (self.score_text_x, self.score_text_y))
            self.timer -= 1
            if self.timer <= 0:
                self.actual_screen = "loose"
        elif self.actual_screen == 'loose':
            if self.apple_happy == 0:
                screen = "sad"
            else:
                screen = "happy"
            self.screen.blit(self.loose_screens[screen], (0, 0))
            self.screen.blit(self.replay_button.image, (self.replay_button.rect.x, self.replay_button.rect.y))
            if self.apple_happy > 1:
                s = "s"
            else:
                s = ""
            if not self.apple_happy == 0:
                text = f"Cool ! You made {self.apple_happy} apple{s} happy"
            else:
                text = "Apples are still sad :("
            font_x, font_y = self.loose_font.size(text)
            self.screen.blit(self.loose_font.render(text, True, self.loose_font_color),
                             (self.screen.get_width()/2 - font_x/2, self.loose_font_y))

            if not self.apple_happy == 0:
                text2 = f'in only {self.point} round{s}'
                font_x, y = self.loose_font.size(text2)
                self.screen.blit(self.loose_font.render(text2, True, self.loose_font_color),
                                 (self.screen.get_width()/2-font_x/2, self.loose_font_y + font_y))

    def rect_color(self, width):
        if width > self.screen.get_width()*2/3:
            R = self.screen.get_width() -width
        else:
            R = 255
        G = 255 * (width / self.screen.get_width())
        B = 0
        if R > 255:
            R = 255
        if R < 0:
            R = 0
        if G < 0:
            G = 0
        return(R,G,B)

class Apple(p.sprite.Sprite):
    def __init__(self, game, state, color, x, y):
        super().__init__()
        self.g = game
        self.orientation = random.choice(self.g.orientations)
        self.img_happy = p.transform.scale(p.image.load("assets/Apple_happy_" + color + ".png"), (self.g.apple_size, self.g.apple_size))
        self.img_happy = p.transform.rotate(self.img_happy, self.orientation)
        self.img_happy_blink = p.transform.rotate(
            p.transform.scale(p.image.load("assets/Apple_happy_" + color + "_blink.png"),
                              (self.g.apple_size, self.g.apple_size)), self.orientation)
        self.img_sad = p.transform.scale(p.image.load("assets/Apple_sad_" + color + ".png"), (self.g.apple_size, self.g.apple_size))
        self.img_sad = p.transform.rotate(self.img_sad, self.orientation)
        self.img_sad_blink = p.transform.rotate(
            p.transform.scale(p.image.load("assets/Apple_sad_" + color + "_blink.png"),
                              (self.g.apple_size, self.g.apple_size)), self.orientation)
        self.imgs_sad = {"idle": self.img_sad, "blink": self.img_sad_blink}
        self.imgs_happy = {"idle": self.img_happy, "blink": self.img_happy_blink }
        self.blink_timer_of_max = random.uniform(*self.g.BLINK_TIMER_OF) * self.g.fps
        self.blink_timer_of = self.blink_timer_of_max
        self.blink_timer_on_max = random.uniform(*self.g.BLINK_TIMER_ON) * self.g.fps
        self.blink_timer_on = self.blink_timer_on_max
        self.blink_start_timer = random.uniform(*self.g.BLINK_START_TIMER) * self.g.fps

        self.state = state
        if state == 'happy':
            self.imgs = self.imgs_happy
        else:
            self.imgs = self.imgs_sad
        self.img = self.imgs["idle"]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def make_happy(self):
        self.imgs = self.imgs_happy
        self.state = "happy"
        self.g.new_happy += 1

    def blink(self):
        if self.blink_timer_of <= 0:
            self.blink_timer_on -= 1
            self.img = self.imgs["blink"]
            if self.blink_timer_on <= 0:
                self.blink_timer_on = self.blink_timer_on_max
                self.blink_timer_of = self.blink_timer_of_max
        else:
            if self.blink_start_timer <= 0:
                self.blink_timer_of -= 1
            else:
                self.blink_start_timer -= 1
            self.img = self.imgs['idle']

class Button:

    def __init__(self, game, name, x, y):
        self.game = game
        self.original_image = p.image.load("assets/" + name + "_button.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def resize(self, mode):
        if mode == 'extension':
            if self.rect.width == self.game.button_width:
                self.image = p.transform.scale(self.image, (self.rect.width*self.game.button_extension_coef, self.rect.height*self.game.button_extension_coef))
                self.rect = self.image.get_rect()
                self.rect.x = self.x-((self.rect.width - self.game.button_width))/2
                self.rect.y = self.y-((self.rect.height - self.game.button_height))/2
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y


