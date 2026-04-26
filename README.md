# Asteroid-Shooter
OOP Coursework

## 1. Introduction

### 1.1 What is the Application?

**Asteroid Shooter** is a game inspired by classic Atari "Asteroids" video game where the player controls a spaceship and destroys asteroids.

### 1.2 How to Run the Program

```bash
pip install pygame
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

**Scoring**: Small (30pts) → Medium (20pts) → Big (10pts). 3 lives. High score saves automatically.

---

## 2. Body/Analysis

### 2.1 Inheritance

All drawable objects inherit from an abstract base class:

```python
class GameObject(ABC):
    @abstractmethod
    def draw(self, win):
        pass
```

**Subclasses**: `Player`, `Bullet`, `BigAsteroid`, `MediumAsteroid`, `SmallAsteroid`

---

### 2.2 Polymorphism

Each subclass implements `draw()` differently:

```python
class Player(GameObject):
    def draw(self, win):
        win.blit(self._rotated, self._rotated_rect)

class Asteroid(GameObject):
    def draw(self, win):
        win.blit(self._image, (self._x, self._y))
```

Used polymorphically in game loop:
```python
for obj in [self._player] + self._asteroids + self._player.bullets:
    obj.draw(self._window)  # Calls appropriate draw() method
```

---

### 2.3 Encapsulation

Private attributes protected with property access:

```python
class Player(GameObject):
    def __init__(self):
        self._x = 0
        self._angle = 0
        self._bullets = []
    
    @property
    def angle(self):
        return self._angle
    
    def lose_life(self):
        self._lives -= 1
        if self._lives <= 0:
            self._gameover = True  # State automatically updated
```

---

### 2.4 Abstraction

Hides complexity behind simple interfaces:

```python
class GameObject(ABC):
    @abstractmethod
    def draw(self, win):  # Forces subclasses to implement
        pass

class AssetManager:
    @property
    def WIDTH(self):  # Hides internal screen dimensions
        return self._screen_width
```

---

### 2.5 Design Pattern: Factory Method

`AsteroidFactory` creates different asteroid types:

```python
class AsteroidFactory:
    def create_asteroid(self, rank):
        if rank == 3:
            return BigAsteroid()
        elif rank == 2:
            return MediumAsteroid()
        elif rank == 1:
            return SmallAsteroid()

# Usage:
new_asteroid = self._asteroid_factory.create_asteroid(rank)
```

---

### 2.6 Composition

Game class aggregates multiple components:

```python
class Game:
    def __init__(self):
        self._assets = AssetManager()          # Asset management
        self._game_state = GameState()         # Score & lives
        self._player = Player()                # Player control
        self._collision = Collision()          # Collision detection
        self._asteroids = []                   # Asteroid list
        self._asteroid_factory = AsteroidFactory()  # Creation
```

---

### 2.7 Data Persistence

High scores saved to `scores.csv`:

```python
def load_high_score(self):
    try:
        with open('scores.csv', 'r') as f:
            self._game_state._high_score = int(f.readline().strip())
    except:
        self._game_state._high_score = 0

def save_high_score(self, score):
    with open('scores.csv', 'w') as f:
        f.write(str(score))
```

---

## 3. Results and Summary

### 3.1 Results

**All Requirements Successfully Implemented:**

- **Fully Functional Game**: Complete, playable asteroid shooter with all mechanics working (spaceship control, collision detection, scoring, lives system).

- **OOP Principles**: All four pillars (Inheritance, Polymorphism, Encapsulation, Abstraction) properly integrated.

- **Design Patterns**: Factory Method pattern in `AsteroidFactory` handles different asteroid types. Singleton pattern in `AssetManager` manages resources.

- **Composition**: 

- **Testing**: 59 unit tests that pass.

- **Data Persistence**: CSV-based high score storage with error handling. **Challenge**: Coordinating interactions between components.

---

### 3.2 Conclusion

**What Was Achieved:**

1. **Working Game**: Fully functional asteroids game with score tracking, high scores, sound effects, and collision detection
2. **Clean Architecture**: Proper separation of concerns with each class having a single responsibility
3. **OOP Integration**: All four pillars working cohesively (inheritance for reuse, polymorphism for flexibility, encapsulation for data integrity, abstraction for simplicity)
4. **Quality Assurance**: 59 passing tests.
5. **Industry Standards**: Factory Method and Singleton patterns properly implemented


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
