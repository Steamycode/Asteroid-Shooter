from scripts.assets import AssetManager

class GameState:

    def __init__(self):
        self._run = True
        self._gameover = False
        self._first_launch = True
        self._lives = 3
        self._score = 0
        self._sound_on = True
        self._high_score = 0
        self._count = 0

    @property
    def run(self):
        return self._run
    
    @run.setter
    def run(self, value):
        self._run = value
    
    @property
    def gameover(self):
        return self._gameover
    
    @gameover.setter
    def gameover(self, value):
        self._gameover = value

    @property
    def first_launch(self):
        return self._first_launch
    
    @first_launch.setter
    def first_launch(self, value):
        self._first_launch = value
    
    @property
    def lives(self):
        return self._lives
    
    @lives.setter
    def lives(self, value):
        self._lives = value
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        self._score = value

    @property
    def sound_on(self):
        return self._sound_on
    
    @sound_on.setter
    def sound_on(self, value):
        self._sound_on = value
    
    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self, value):
        self._count = value
        
    @property
    def high_score(self):
        return self._high_score
    
    @high_score.setter
    def high_score(self, value):
        self._high_score = value
        

    def add_score(self, points):
        self.score += points

    def lose_life(self):
        self.lives -= 1
        if self.sound_on:
            assets = AssetManager()
            assets.explosion_sound.play()
        if self.lives <= 0:
            self.gameover = True

    def toggle_sound(self):
        self.sound_on = not self.sound_on

    def restart(self):
        self.run = True
        self.gameover = False
        self.lives = 3
        self.score = 0
        self.count = 0
