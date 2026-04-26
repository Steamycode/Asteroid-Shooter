# Asteroid-Shooter
OOP Coursework

## 1. Introduction

### 1.1 What is the Application?

**Asteroid Shooter** is an Atari "Asteroids" inspired video game where the player controls a spaceship and destroys asteroids.

### 1.2 How to Run the Program

- To install pygame, try any of the following commands in cmd:
```bash
pip install pygame
```
```bash
python -m pip install pygame
```
```bash
pip3 install pygame
```
```bash
python3 -m pip install pygame
```
```bash
py -m pip install pygame
```

- To run:
```bash
python main.py
```

### 1.3 How to Use the Program

|  Key  |    Action    |
|-------|--------------|
| ← / → | Rotate ship  |
|   ↑   | Move forward |
| SPACE | Fire bullet  |
|   m   | Toggle sound |
|  TAB  | Restart game |

**Gameplay**: You start with 3 lives, each time you get hit by an asteroid you loose life, when shooting down an asteroid you score, and the asteroid splits into two smaller ones.

**Scoring**: Big (10pts) → Medium (20pts) → Small (30pts)

---

## 2. Body/Analysis

### 2.1 OOP pillars

#### 2.1.1 Inheritance

All game object inherit from an abstract base class:

```python
class GameObject(ABC):

    @abstractmethod
    def draw(self, win):
        pass

    @abstractmethod
    def move(self, win):
        pass

    @abstractmethod
    def check_off_screen(self):
        pass
```

Different size asteroids inherit from main asteroid class:

```python
class Asteroid(GameObject):
    
    def __init__(self):
        self._rank = 0
        self._image = None
        self._width = 0
        self._height = 0
        self._assets = AssetManager()
        self.random_spawn_location(self.assets.screen_width, self.assets.screen_height)
        self.set_velocity(self.assets.screen_width, self.assets.screen_height)

class BigAsteroid(Asteroid):

    def __init__(self):
        super().__init__()
        self._rank = 3
        self._image = self.assets.big_asteroid_img
        self._width = 150
        self._height = 150
```

**Subclasses**: `Player`, `Bullet`, `BigAsteroid`, `MediumAsteroid`, `SmallAsteroid`

---

#### 2.1.2 Polymorphism

Each subclass implements `draw()`, `move()`, `check_off_screen()` differently:

```python
class Player(GameObject):

    def draw(self, win):
        win.blit(self._rotated, self._rotated_rect)
    
    def move(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.update_position()

class Asteroid(GameObject):

    def draw(self, win):
        win.blit(self._image, (self._x, self._y))
    
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
```

---

#### 2.1.3 Encapsulation

Private attributes protected with property access:

```python
class GameState:

    def __init__(self):
        self._lives = 3
        self._score = 0
        self._sound_on = True
    
    @property
    def sound_on(self):
        return self._sound_on
    
    @sound_on.setter
    def sound_on(self, value):
        self._sound_on = value
    
    def toggle_sound(self):
        self.sound_on = not self.sound_on
```

---

#### 2.1.4 Abstraction

Hides complexity behind simple interfaces:

```python
class GameObject(ABC):

    @abstractmethod
    def draw(self, win):
        pass

    @abstractmethod
    def move(self, win):
        pass

class Game:

    def run(self):
        while self.game_state.run:
            self.update_gui()
            self.game_events()
            self.draw_window()
```

---

### 2.2 Design patterns 

`AsteroidFactory` creates different asteroid types:

```python
class AsteroidFactory:

    @staticmethod
    def create_asteroid(self, rank):
        if rank == 3:
            return BigAsteroid()
        elif rank == 2:
            return MediumAsteroid()
        elif rank == 1:
            return SmallAsteroid()
```

`AssetManager` ensures theres only one asset manager instance:

```python
class AssetManager:
        
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

### 2.3 Composition/Aggregation

Game class aggregates multiple components:

```python
class Game:

    def __init__(self):
        self._assets = AssetManager()
        self._game_state = GameState()
        self._player = Player()
        self._collision = Collision()
        self._asteroids = []
        self._asteroid_factory = AsteroidFactory()
```

---

### 2.4 Reading from/writing to file

High scores saved to `scores.csv`:

```python
def load_high_score(self):
    try:
        with open('scores.csv', 'r') as score_file:
            self.game_state.high_score = int(score_file.readline().strip())
    except (FileNotFoundError, ValueError):
        print('Error loading scores file')
        self.game_state.high_score = 0

def save_high_score(self, score):
    try:
        with open('scores.csv', 'w') as score_file:
            score_file.write(str(score))
            self.game_state.high_score = score
    except (FileNotFoundError, ValueError):
        print(f'Error saving high score: {score}')
```

---

## 3. Results and Summary

### 3.1 Results

**All Requirements Successfully Implemented:**

- **Functional Game**: Complete, playable asteroid shooter with all mechanics working (spaceship control, collision detection, scoring, lives system).

- **OOP Principles**: All four pillars (Inheritance, Polymorphism, Encapsulation, Abstraction) properly integrated.

- **Design Patterns**: Factory Method pattern in `AsteroidFactory` handles different asteroid types. Singleton pattern in `AssetManager` manages resources.

- **Aggregation**: Multiple classes aggregate different components

- **Testing**: 59 unit tests that pass. **Challanges**: coming up with tests.

- **Data Persistence**: CSV-based high score storage with error handling.

---

### 3.2 Conclusion

**What Was Achieved:**

1. **Working Game**: A functional asteroids game with score tracking, high scores, sound effects, and collision detection
2. **Better Understanding of OOP Pillars** inheritance for reuse, polymorphism for flexibility, encapsulation for data integrity, abstraction for simplicity
3. **Using Cleaner Architecture**: Separating classes with different responsibilities into files
4. **Ensuring Quality**: 59 passing tests

---

### 3.3 Possible Extensions

- **Game Features**: Power-ups, enemy ships, levels, boss battles
- **Data**: Statistics tracking, leaderboards, session logging
- **UI**: Main menu, settings, particle effects, score displays
- **Audio/Visual**: Background music, themes, screen shake, animations
- **Multiplayer**: Network play, co-op, cloud leaderboards

---

## 4. References

- **YouTube Tutorial**: https://www.youtube.com/watch?v=XKMjMGbdrpY
