import random

import game
from component import verify_attrs
from entity import Entity


class SpawnVortexComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['spawn_period', ('spawn_timer', 0)])
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        entity.spawn_timer += dt
        if entity.spawn_timer > entity.spawn_period:
            entity.spawn_timer -= entity.spawn_period
            
            x = random.randrange(0, game.get_game().screen.get_width())
            y = random.randrange(0, game.get_game().screen.get_height())
            color = random.choice([(255,0,0), (0,255,0)])
            vortex = Entity("vortex", x=x, y=y, color=color)
            game.get_game().entity_manager.add_entity(vortex)
            

class GrowVortextComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['radius', 'max_radius', 'growth_rate'])
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        entity.previous_radius = entity.radius
        if entity.radius < entity.max_radius:
            entity.radius += dt * entity.growth_rate
            

class DrawVortextComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'color', 'radius', ('previous_radius', entity.radius)])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity):
        if entity.radius != entity.previous_radius:
            game.get_game().renderer.appendRing(entity.color, entity.x, entity.y, entity.previous_radius, entity.radius)