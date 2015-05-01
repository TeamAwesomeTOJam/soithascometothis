from component import verify_attrs
from vec2d import Vec2d
from random import randrange

class AIMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 1), ('dy', 0)])
        entity.facing = 1
              
        entity.register_handler('update', self.handle_update)
 
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        d = Vec2d(entity.dx, entity.dy)
        d.length = 1
        r = randrange(-50,50)
        d.angle += r
        entity.dx = d[0]
        entity.dy = d[1]
        
class AIActionComponent(object):
    
    def add(self, entity):
        verify_attrs(entity,['chasing',('time_since_action',0)])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        
    def handle_update(self, entity, dt):
        entity.time_since_action -= dt
        if entity.time_since_action <= 0:
            entity.time_since_action = 10
            action = randrange(1,3)
            if action == 1:
                if entity.chasing:
                    entity.handle('action', 'SPEED_BOOST')
                else:
                    entity.handle('action', 'SMOKE_SCREEN')
            elif action == 2:
                if entity.chasing:
                    entity.handle('action', 'PLACE_MINEFIELD')
                else:
                    entity.handle('action', 'CREATE_DECOY')
            elif action == 3:
                if entity.chasing:
                    entity.handle('action', 'TRAP')
                else:
                    entity.handle('action','HIDE')
        
        