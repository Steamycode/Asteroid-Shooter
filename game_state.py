from assets import AssetManager

class GameState:

    def __init__(self):
        self._run = True
        self._gameover = False
        self._lives = 3
        self._score = 0
        self._sound_on = True
        self._high_score = 0
        self._high_score_name = ""
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
    def lives(self):
        return self._lives
    
    @property
    def score(self):
        return self._score
    
    @property
    def sound_on(self):
        return self._sound_on
    
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
        self._score += points

    def lose_life(self):
        self._lives -= 1
        if self._sound_on:
            assets = AssetManager()
            assets.explosion_sound.play()
        if self._lives <= 0:
            self._gameover = True

    def toggle_sound(self):
        self._sound_on = not self._sound_on

    def restart(self):
        self._run = True
        self._gameover = False
        self._lives = 3
        self._score = 0
        self._sound_on = True
        self._count = 0
