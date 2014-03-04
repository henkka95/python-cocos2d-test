# -*- coding: utf-8 -*-

import pyglet
from pyglet.window import key

import xmlmap_maker


import cocos
from cocos import tiles, actions, layer, sprite

UP = 0
RIGHT = 1
LEFT = 2
DOWN = 3


class World(cocos.layer.Layer):
    """
    Responsibilities:
        Generation: random generates a level
        Initial State: Set initial play state
        Play: updates level state, by time and user input. Detection of
        end-of-level conditions.
        Level progression.
    """
    is_event_handler = True

    def __init__(self):
        super(World, self).__init__()
        self.player = Car()
        self.newMap()
        self.map = tiles.load('tilemap.xml')['map0']
        self.blockKeys = 0.0
        self.blockKeysFull = 0.5
        self.bindings = {
            key.LEFT: 'left',
            key.RIGHT: 'right',
            key.UP: 'up',
                        }
        buttons = {}
        for k in self.bindings:
            buttons[self.bindings[k]] = 0
        self.buttons = buttons

        self.carLayer = layer.ScrollableLayer()
        self.carLayer.add(self.player)
        self.manager = layer.ScrollingManager()
        self.manager.add(self.map)
        self.manager.add(self.carLayer)
        self.add(self.manager)
        self.schedule(self.update)


    def newMap(self):
        xmlmap_maker.newMap(60, 60)

    def on_key_press(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 1
            return True
        return False

    def on_key_release(self, k, m ):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 0
            return True
        return False

    def update(self, dt):
        self.manager.set_focus(self.player.x, self.player.y)

        if self.blockKeys > 0:
            self.blockKeys -= dt

        buttons = self.buttons
        if buttons['up'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.forward()
        elif buttons['left'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.turnLeft()
        elif buttons['right'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.turnRight()


class Car(cocos.sprite.Sprite):
    carImage = pyglet.resource.image('car.png')

    def __init__(self):
        super(Car, self).__init__(Car.carImage)
        self.x = 64*7
        self.y = 64*7
        self.animTime = 0.5
        self.rotTime = 0.4
        self.orientation = UP

    def checkOrientation(self):
        # UP = 0
        # RIGHT = 1
        # LEFT = 2
        # DOWN = 3
        print "rotation:", str(self.rotation)
        if self.rotation == 0:
            self.orientation = UP
        elif self.rotation == 90:
            self.orientation = RIGHT
        elif self.rotation == 180:
            self.orientation = DOWN
        elif self.rotation == 270:
            self.orientation = LEFT
        else:
            print "bad rotation", str(self.rotation)
        print "Orientation:", str(self.orientation)

    def turnRight(self):
        self.do(actions.RotateBy(90, self.rotTime))

    def turnLeft(self):
        self.do(actions.RotateBy(-90, self.rotTime))

    def forward(self):
        self.checkOrientation()
        if self.orientation == UP:
            self.do(actions.MoveBy((0, 128), self.animTime))
        elif self.orientation == LEFT:
            self.do(actions.MoveBy((-128, 0), self.animTime))
        elif self.orientation == RIGHT:
            self.do(actions.MoveBy((128, 0), self.animTime))
        else:
            self.do(actions.MoveBy((0, -128), self.animTime))


def main():
    global keyboard, scroller

    from cocos.director import director

    director.init(width=600, height=600, do_not_scale=True, resizable=True)

    world = World()
    car_layer = layer.ScrollableLayer()
    car_layer.add(world.player)

    scene = cocos.scene.Scene()

    scene.add(world)
    director.run(scene)


if __name__ == '__main__':
    main()
