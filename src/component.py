from abc import ABCMeta, abstractmethod

import pygame
from math import *

import game
import mode
from vec2d import Vec2d


FACING = ['right', 'down', 'left', 'up']


class Component:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def add(self, entity):
        pass
    
    @abstractmethod
    def remove(self, entity):
        pass


class ExampleComponent(Component):
    
    def add(self, entity):
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        print '%f seconds have elapsed!' % (dt,)


class AnimationComponent(Component):
    
    def add(self, entity):
        entity.register_handler('update', self.on_update)
        entity.register_handler('play-animation', self.on_play_animation)
        
        entity.current_animation = 'default'
        entity.animation_pos = 0
        entity.animation_should_loop = True

        entity.image = getattr(entity.animations, entity.current_animation).frames[0]
        
    def remove(self, entity):
        entity.unregister_handler('update', self.on_update)
        entity.unregister_handler('play-animation', self.on_play_animation)
        
    def on_update(self, entity, dt):
        entity.animation_pos += dt
        if entity.animation_pos >= getattr(entity.animations, entity.current_animation).duration:
            if entity.animation_should_loop:
                entity.animation_pos = entity.animation_pos % getattr(entity.animations, entity.current_animation).duration
            else:
                entity.handle('animation-finished', entity.current_animation)
                entity.current_animation = 'default'
                entity.animation_pos = 0
                entity.animation_should_loop = True
        frame_number = int(entity.animation_pos / getattr(entity.animations, entity.current_animation).duration * len(getattr(entity.animations, entity.current_animation).frames))
        entity.image = getattr(entity.animations, entity.current_animation).frames[frame_number]
        
    def on_play_animation(self, entity, animation, loop=False):
        if animation == entity.current_animation and entity.animation_should_loop and loop:
            pass
        else:
            entity.current_animation = animation
            entity.animation_should_loop = loop
            entity.animation_pos = 0


class MovementComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height', ('last_good_x', entity.x), ('last_good_y', entity.y), 'speed'])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.dx or entity.dy:
            entity.last_good_x = entity.x
            entity.last_good_y = entity.y
            entity.x += entity.dx * dt * entity.speed
            entity.y += entity.dy * dt * entity.speed
            bound = lambda a,b,x : min(b,max(a,x))
            res = game.get_game().screen_size
            entity.x = bound(0, res[0] - entity.width, entity.x)
            entity.y = bound(0, res[1] - entity.height, entity.y)
            game.get_game().entity_manager.update_position(entity)
            
        collisions = game.get_game().entity_manager.get_in_area('collision', (entity.x, entity.y, entity.width, entity.height)) - {entity} 
        for collided_entity in collisions:
            entity.handle('collision', collided_entity)


class InputMovementComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 0), ('dy', 0)])
        entity.facing = 1
              
        entity.register_handler('input', self.handle_input)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
    
    def handle_input(self, entity, event):
        if event.action == 'RIGHT':
            entity.dx = event.value
        elif event.action == 'UP':
            entity.dy = -1 * event.value
        elif event.action == 'LEFT':
            entity.dx = -1 * event.value
        elif event.action == 'DOWN':
            entity.dy = event.value
        
        if entity.dx != 0 or entity.dy != 0:
            direction = Vec2d(entity.dx, entity.dy)
            entity.facing = int(((direction.get_angle() + 45) % 360) / 90)          


class DrawComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('image_x', 0), ('image_y', 0), 'x', 'y'])
        
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface, transform):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.image), transform(entity.x + entity.image_x, entity.y + entity.image_y))


class DrawHitBoxComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height'])
        
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        pygame.draw.rect(surface, (255, 0, 255), (entity.x, entity.y, entity.width, entity.height))

                
class MouseMovementComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y'])
        entity.register_handler('input', self.handle_input)
    
    def remove(self, entity):
        entity.unregister_handler('intput', self.handle_input)
        
    def handle_input(self, entity, event):
        if event.action == 'MOUSE_POSITION':
            entity.x = event.value[0]
            entity.y = event.value[1]


class HumanGrabberComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'grab_range', ('grabbed_human', None)])
        entity.register_handler('input', self.handle_input)
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
        entity.unregister_handler('update', self.handle_update)
        
    def handle_input(self, entity, event):
        if event.action == 'CLICK':
            if event.value == 1:
                humans = game.get_game().entity_manager.get_by_tag('human')
                my_pos = Vec2d(entity.x, entity.y)
                closest = None
                distance = 0
                for h in humans:
                    other_pos = get_midpoint(h)
                    if closest == None:
                        closest = h
                        distance = my_pos.get_distance(other_pos)
                    else:
                        new_distance = my_pos.get_distance(other_pos)
                        if new_distance < distance:
                            closest = h
                            distance = new_distance
                if distance < entity.grab_range:
                    entity.grabbed_human = closest
                    closest.handle('grabbed', entity)
            elif event.value == 0:
                entity.grabbed_human.handle('released', entity)
                entity.grabbed_human = None
    
    def handle_update(self, entity, dt):
        if entity.grabbed_human:
            entity.grabbed_human.x = entity.x - entity.grabbed_human.width/2
            entity.grabbed_human.y = entity.y - entity.grabbed_human.height/2


class HumanPlacementComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['x','y', 'width', 'height'])
        entity.register_handler('grabbed', self.handle_grabbed)
        entity.register_handler('released', self.handle_released)

    def remove(self, entity):
        entity.remove_handler('grabbed', self.handle_grabbed)
        entity.remove_handler('released', self.handle_released)
        
    def handle_grabbed(self, entity, grabber):
        pass
    
    def handle_released(self, entity, releaser):
        locations = game.get_game().entity_manager.get_in_area('location', (entity.x, entity.y, entity.width, entity.height))
        for location in locations:
            location.handle('human_placed', entity)
            break # Just send the even to the first location in the set


class HumanAcceptor(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', []), 'human_x', 'human_y'])
        entity.register_handler('human_placed', self.handle_human_placed)
    
    def remove(self, entity):
        entity.remove_handler('human_placed', self.handle_human_placed)
        
    def handle_human_placed(self, entity, human):
        entity.humans.append(human)
    

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
