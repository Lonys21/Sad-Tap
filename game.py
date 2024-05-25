import pygame, random
p = pygame

class Game:
    def __init__(self, screen, fps):
        self.screen = screen
        self.fps = fps
        self.background = 'black'
        self.actual_screen = 'game'
        self.MARGIN_Y = 100

        # timer
        self.TIMER_MAX = 120*self.fps
        self.TIME_PUNITION = 25*self.fps
        self.timer = self.TIMER_MAX
        self.rect_height = 110
        self.rect_x = 0
        self.rect_y = 65


        # apples
        self.MAX_ROUND = 6
        self.ADD_SAD = 3
        self.apple_size = 100
        self.apples = []
        self.apple_width = 2
        self.apple_height = 2
        self.num_apples = self.apple_height*self.apple_width
        self.orientations = [0, 90, 180, 270]
        self.number_sad = 1
        self.new_happy = 0
        self.start()

        # score
        self.point = 0
        self.score_text = pygame.font.SysFont("Arial",  65)
        self.score_text_color = "white"
        self.score_text_x = 0
        self.score_text_y = 0

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
        self.coos = self.set_coos(self.apple_width, self.apple_height)
        for coo in self.coos:
            self.apples.append(Apple(self, "happy", coo[0], coo[1]))
        for n in range(self.number_sad):
            apple = random.choice(self.apples)
            while apple.state == 'sad':
                apple = random.choice(self.apples)
            apple.state = 'sad'
            apple.img = apple.img_sad


    def update(self):
        self.screen.fill(self.background)
        if self.actual_screen == 'game':
            for apple in self.apples:
                self.screen.blit(apple.img, (apple.rect.x, apple.rect.y))
            if self.new_happy == self.number_sad:
                self.restart()
            rect_width = (self.timer/self.TIMER_MAX)*self.screen.get_width()
            rect = pygame.draw.rect(self.screen, self.rect_color(rect_width), (self.rect_x, self.rect_y, rect_width, self.rect_height))
            self.screen.blit(self.score_text.render(str(self.point), True, self.score_text_color), (self.score_text_x, self.score_text_y))
            self.timer -= 1
            if self.timer <= 0:
                self.actual_screen = "loose_screen"
        elif self.actual_screen == 'loose_screen':
            pass

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
    def __init__(self, game, state, x, y):
        super().__init__()
        self.g = game
        self.orientation = random.choice(self.g.orientations)
        self.img_happy = p.transform.scale(p.image.load("assets/Apple_happy.png"), (self.g.apple_size, self.g.apple_size))
        self.img_happy = p.transform.rotate(self.img_happy, self.orientation)
        self.img_sad = p.transform.scale(p.image.load("assets/Apple_sad.png"), (self.g.apple_size, self.g.apple_size))
        self.img_sad = p.transform.rotate(self.img_sad, self.orientation)
        self.state = state
        if state == 'happy':
            self.img = self.img_happy
        else:
            self.img = self.img_sad
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def make_happy(self):
        self.img = self.img_happy
        self.state = "happy"
        self.g.new_happy += 1

