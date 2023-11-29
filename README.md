# Circles

Simple 2D physics simulation of circles inside a box

- Written in **Python** as it should fullfill the requirements of an assignment like this. With libraries such as NumPy and SDL2 providing C-bindings, there is still great potential to writing code focused on performance.
 
- **SDL2** used for rendering graphics. Was chosen due to its lightweight, cross-platform accelerated 2D render API.

- **NumPy** provides strided arrays and vectorized operations. As the biggest performance concern was memory access, or more precisely spatial locality, these features were essential when using Python.


## Implementation and considerations

Initially, I aimed towards adopting an ECS architecture to create a flexible system supporting various primitives. For example, 'Circle' and 'Rectangle' class inheriting from the same base class and a separate 'Physics' component. However, incorporating NumPy for optimization posed challenges, prompting a shift towards a more cohesive design over strict modularity.

Implementing collision detection didn't take much effort, but handling collisions proved more intricate than anticipated, with managing post-collision interactions adding unexpected challenges.

While there were ideas for improvements, especially enhancing data structures easier take advantage of vectorized operations, etc. In hindsight, I believe using C++ would have been more straightforward based on its more direct and efficient approach to handling sequentially accessed data structures in contrast to NumPy's higher-level abstractions.

## Run
```bash
# Install required packages
pip install -r requirements.txt

# run script
python ./run.py [options]

# Options available:
usage: run.py [-h] [-x SIZE_X] [-y SIZE_Y] [-min_rad MIN_RAD] [-max_rad MAX_RAD] [-spawn_limit SPAWN_LIMIT]
              [-gravity GRAVITY]

options:
  -h, --help                  show this help message and exit
  -x SIZE_X, --size_x SIZE_X  Set width of window
  -y SIZE_Y, --size_y SIZE_Y  Set height of window
  -min_rad MIN_RAD            Set minimum radii of generated circles
  -max_rad MAX_RAD            Set maximum radii of generated circles
  -spawn_limit SPAWN_LIMIT    Set maximum number of circles to spawn
  -gravity GRAVITY            Set value of gravity
```
