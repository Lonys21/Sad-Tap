import pygame, random
p = pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background = 'black'
        self.MARGIN_Y = 100

        # apples
        self.MAX_ROUND = 6
        self.apple_size = 100
        self.apples = []#p.sprite.Group()
        self.apple_width = 6
        self.apple_height = 6
        self.num_apples = self.apple_height*self.apple_width
        self.orientations = [0, 90, 180, 270]
        self.number_sad = 1
        self.new_happy = 0
        self.round = 1
        self.start()

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
        self.apples = []
        self.new_happy = 0
        self.round += 1
        self.coos = []
        if self.round % 1 == 0:
            self.number_sad += 1
            if self.number_sad > 3:
                if self.num_apples <= 5*5:
                    self.number_sad = 1
                    self.apple_width += 2
                    self.apple_height += 2
                    self.round = 1
                elif self.num_apples == 6*6:
                    self.number_sad = 1
                    self.round = 1
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
        for apple in self.apples:
            self.screen.blit(apple.img, (apple.rect.x, apple.rect.y))
        if self.new_happy == self.number_sad:
            self.restart()

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

