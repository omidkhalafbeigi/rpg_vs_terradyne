from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

kill = 0
speed_rate = 5
total_kill = 0
passed_robots = 0


def spawn_robot(destroyed_robot):
    return duplicate(destroyed_robot, position=(-10, 0.5, random.randint(-40, 40)))


def update():
    global kill
    global total_kill
    global speed_rate
    global passed_robots
    border = 55
    passed_robots_threshold = 2

    for robot_index in range(len(robots)):
        dx = random.random() / speed_rate
        robots[robot_index].x += dx
        if robots[robot_index].x > border:
            new_robot = spawn_robot(robots[robot_index])
            destroy(robots[robot_index])
            robots.append(new_robot)
            del robots[robot_index]
            passed_robots += 1

    if ((kill % 5) == 0) and (kill is not 0):
        kill = 0
        speed_rate /= 1.2

    if passed_robots == passed_robots_threshold:
        print('-------------')
        print('You defeated!')
        print(f'Total kills: {total_kill}')
        print('-------------')
        app.userExit()

    if held_keys['left mouse']:
        gunshot_audio.play()
        gunshot_animation.start()

        for robot_index in range(len(robots)):
            if robots[robot_index].hovered:
                kill += 1
                total_kill += 1
                new_robot = spawn_robot(robots[robot_index])
                destroy(robots[robot_index], delay=0)
                robots.append(new_robot)
                del robots[robot_index]


app = Ursina()
Sky()
ground = Entity(model='cube', texture='grass', collider='box', scale=(100, 1, 100), color=color.lime)
wall_1 = Entity(model='cube', texture='brick', collider='box', color=color.white, position=(0, 1, 50),
                scale=(100, 20, 1))
wall_2 = duplicate(wall_1, position=(50, 1, 0), scale=(1, 20, 100))
wall_3 = duplicate(wall_1, position=(0, 1, -50), scale=(100, 20, 1))
wall_4 = duplicate(wall_1, position=(-50, 1, 0), scale=(1, 20, 100))
player = FirstPersonController(speed=20, position=(47, 0, 0), rotation=(0, -100, 0))
gun = Entity(model='rpg.obj', texture='sky_sunset', color=color.white, scale=0.0015, position=(0.5, -0.3, 50),
             parent=camera.ui, rotation=(0, 110, -5))
car1 = Entity(color=color.brown, model='terradyne.obj', texture='sky_sunset', position=(0, 0.5, 0), scale=0.01,
              collider='box')
robot1 = car1
# robot1 = Entity(model='robot.obj', texture='shore', position=(-10, 0, 20), rotation=(0, 90, 0), collider='box')
robot2 = duplicate(robot1, position=(-10, 0.5, 40))
robot3 = duplicate(robot1, position=(-10, 0.5, -40))
robot4 = duplicate(robot1, position=(-10, 0.5, 20))
robot5 = duplicate(robot1, position=(-10, 0.5, -20))
robots = [robot1, robot2, robot3, robot4, robot5]
gunshot_audio = Audio('gunshot.wav', autoplay=False)
gunshot_animation = Animation(name='gunshot_frames/Frame', fps=45, loop=False, autoplay=False, scale=0.3,
                              parent=camera.ui, position=(0.2, -0.16, 0))

app.run()
