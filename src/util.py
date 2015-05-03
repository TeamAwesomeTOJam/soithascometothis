import random
import pygame
from vec2d import Vec2d
import game

def report(name,report):
    game.get_game().entity_manager.get_by_name('report').handle('record_update', name, report)

def camp():
    return game.get_game().entity_manager.get_by_name('camp')

def clamp(v):
    return max(min(v,100),0)

def chance(c):
    return random.randrange(0,100) < c

def small():
    return random.randrange(1,5)
def mid():
    return random.randrange(5,10)
def big():
    return random.randrange(10,15)

def verify_attrs(entity, attrs):
    missing_attrs = []
    for attr in attrs:
        if isinstance(attr, tuple):
            attr, default = attr
            if not hasattr(entity, attr):
                setattr(entity, attr, default)
        else:
            if not hasattr(entity, attr):
                missing_attrs.append(attr)
    if len(missing_attrs) > 0:
        raise AttributeError("entity [%s] is missing required attributes [%s]" % (entity._static_data_name, missing_attrs))


def get_entities_in_front(entity):
    COLLIDE_BOX_WIDTH = 100
    COLLIDE_BOX_HEIGHT = 100
    collision_box = get_box_in_front(entity, COLLIDE_BOX_WIDTH, COLLIDE_BOX_HEIGHT)

    return game.get_game().entity_manager.get_in_area('collide', collision_box)

def get_box_in_front(entity, width, height):
    midpoint = get_midpoint(entity)
    player_dimensions = Vec2d(entity.width, entity.height)
    if entity.facing == 0: #right
        collision_box = (midpoint.x + player_dimensions.x/2, midpoint.y - height/2, width, height)
    elif entity.facing == 1: #down
        collision_box = (midpoint.x - width/2, midpoint.y + player_dimensions.y/2, width, height)
    elif entity.facing == 2: #left
        collision_box = (midpoint.x - player_dimensions.x/2 - width, midpoint.y - height/2, width, height)
    elif entity.facing == 3: #up
        collision_box = (midpoint.x - width/2, midpoint.y - player_dimensions.y/2 - height, width, height)

    return collision_box

def get_midpoint(entity):
    return Vec2d(entity.x + (entity.width/2), entity.y + (entity.height/2))

def get_box(entity):
    return pygame.Rect(entity.x, entity.y, entity.width, entity.height)