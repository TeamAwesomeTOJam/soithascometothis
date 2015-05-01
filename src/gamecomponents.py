import game
import pygame
from component import verify_attrs
from vec2d import Vec2d
from entity import Entity
from component import get_midpoint

class SmokeScreenComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['smoke_screen_rad', 'smoke_screen_cooldown_time', 'color', 'x', 'y', 'width', 'height', ('smoke_screen_cooldown', 0)])
        entity.register_handler('action', self.handle_action)
        entity.register_handler('update', self.handle_update)
 
    def remove(self, entity):
        entity.unregister_handler('action', self.handle_action)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_action(self, entity, action):
        if action == 'SMOKE_SCREEN' and entity.smoke_screen_cooldown <= 0:
            p = get_midpoint(entity)
            game.get_game().renderer.appendCircle( 
                    entity.color,int(p[0]), int(p[1]), entity.smoke_screen_rad
                    )

            #pygame.draw.circle(game.get_game().screen, entity.color, (int(p[0]), int(p[1])), entity.smoke_screen_rad)
            entity.smoke_screen_cooldown = entity.smoke_screen_cooldown_time
    
    def handle_update(self, entity, dt):
        if entity.smoke_screen_cooldown >= 0:
            entity.smoke_screen_cooldown -= dt
            
class TrapComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['trap_in_rad', 'trap_out_rad', 'trap_cooldown_time', 'color', 'x', 'y', 'width', 'height', ('trap_cooldown', 0)])
        entity.register_handler('action', self.handle_action)
        entity.register_handler('update', self.handle_update)
 
    def remove(self, entity):
        entity.unregister_handler('action', self.handle_action)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_action(self, entity, action):
        if action == 'TRAP' and entity.trap_cooldown <= 0:
            p = get_midpoint(entity)
            game.get_game().renderer.appendRing( 
                    entity.color,int(p[0]), int(p[1]), entity.trap_out_rad, entity.trap_in_rad
                    )

            #pygame.draw.circle(game.get_game().screen, entity.color, (int(p[0]), int(p[1])), entity.smoke_screen_rad)
            entity.trap_cooldown = entity.trap_cooldown_time
    
    def handle_update(self, entity, dt):
        if entity.trap_cooldown >= 0:
            entity.trap_cooldown -= dt

class SpawnDecoyComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['decoy_cooldown_time', 'x', 'y', 'dx', 'dy',('decoy_cooldown',0), 'color'])
        entity.register_handler('update', self.handle_update)
        entity.register_handler('action', self.handle_action)
    
    def remove(self, entity):
        entity.unregister_handler('action', self.handle_action)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.decoy_cooldown >= 0:
            entity.decoy_cooldown -= dt
    
    def handle_action(self, entity, action):
        if action == 'CREATE_DECOY' and entity.decoy_cooldown <= 0:
            if entity.dx or entity.dy:
                d = (entity.dx,entity.dy)
            else:
                d = (1,0)
            game.get_game().entity_manager.add_entity(Entity("decoy",follow_entity = entity, color = entity.color, mirror_dir = d, x = entity.x, y = entity.y))
            entity.decoy_cooldown = entity.decoy_cooldown_time
        
        
class DecoyMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 0), ('dy', 0), 'follow_entity','mirror_dir'])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        v = Vec2d(entity.follow_entity.dx, entity.follow_entity.dy)
        projection = v.projection(Vec2d(entity.mirror_dir))
        a = projection - v
        d = v +  (2 * a)
        entity.dx = d[0]
        entity.dy = d[1]

class  SelfDestructComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['liveness'])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        
    def handle_update(self, entity, dt):
        entity.liveness -= dt
        if entity.liveness <= 0:
            game.get_game().entity_manager.remove_entity(entity)
            
class MinefieldComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['minefield_ang_density', 'minefield_rad_density', 'minefield_max_rad', 'minefield_min_rad', 'minefield_cooldown_time', 'x', 'y', 'dx', 'dy', 'width', 'height', ('minefield_cooldown',0), 'color'])
        entity.register_handler('update', self.handle_update)
        entity.register_handler('action', self.handle_action)
    
    def remove(self, entity):
        entity.unregister_handler('action', self.handle_action)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.minefield_cooldown >= 0:
            entity.minefield_cooldown -= dt
    
    def handle_action(self, entity, action):
        if action == 'PLACE_MINEFIELD' and entity.minefield_cooldown <= 0:
            m = get_midpoint(entity)
            for r in range(entity.minefield_min_rad, entity.minefield_max_rad, entity.minefield_rad_density):
                anglestart = 0
                angleend = 360
                for a in xrange(anglestart, angleend, entity.minefield_ang_density):
                    v = Vec2d(0, 1)
                    v.length = r
                    v.angle = a
                    p = m + v
                    #pygame.draw.circle(game.get_game().screen, entity.color, (int(p[0]), int(p[1])), 5)
                    game.get_game().renderer.appendPlayerCircle( entity.color,int(p[0]), int(p[1]), 5)
            entity.minefield_cooldown = entity.minefield_cooldown_time
    
class SpeedBoostComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['speed_boost_activation_cooldown_time', 'speed_boost_duration_time', 'speed_boost_speed', 'speed', ('speed_boost_activation_cooldown',0), ('base_speed', entity.speed), ('speed_boost_time', 0)])
        entity.register_handler('update', self.handle_update)
        entity.register_handler('action', self.handle_action)
    
    def remove(self, entity):
        entity.unregister_handler('action', self.handle_action)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.speed_boost_activation_cooldown >= 0:
            entity.speed_boost_activation_cooldown -= dt
        if entity.speed_boost_time >= 0:
            entity.speed_boost_time -= dt
            if entity.speed_boost_time <= 0:
                entity.speed = entity.base_speed
    
    def handle_action(self, entity, action):
        if action == 'SPEED_BOOST' and entity.speed_boost_activation_cooldown <= 0:
            entity.speed = entity.speed_boost_speed
            entity.speed_boost_time = entity.speed_boost_duration_time
            entity.speed_boost_activation_cooldown = entity.speed_boost_activation_cooldown_time
            
class HideComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('invisibility_time', 0), 'invisibility_duration', 'invisibility_cooldown_time', 'visible', ('invisibility_cooldown',0)])
        entity.register_handler('update', self.handle_update)
        entity.register_handler('action', self.handle_action)
    
    def remove(self, entity):
        entity.unregister_handler('action', self.handle_action)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.invisibility_cooldown >= 0:
            entity.invisibility_cooldown -= dt
        if entity.invisibility_time >= 0:
            entity.invisibility_time -= dt
            if entity.invisibility_time <= 0:
                entity.visible = True
    
    def handle_action(self, entity, action):
        if action == 'HIDE' and entity.invisibility_cooldown <= 0:
            entity.visible = False
            entity.invisibility_time = entity.invisibility_duration
            entity.invisibility_cooldown = entity.invisibility_cooldown_time
            
class ButtonInterpreterComponent(object):
    
    def add(self, entity):
        verify_attrs(entity,['chasing'])
        entity.register_handler('input', self.handle_input)
    
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
        
    def handle_input(self, entity, event):
        if event.action == 'BUTTON1' and event.value:
            if entity.chasing:
                entity.handle('action', 'SPEED_BOOST')
            else:
                entity.handle('action', 'SMOKE_SCREEN')
        elif event.action == 'BUTTON2' and event.value:
            if entity.chasing:
                entity.handle('action', 'PLACE_MINEFIELD')
            else:
                entity.handle('action', 'CREATE_DECOY')
        elif event.action == 'BUTTON3' and event.value:
            if entity.chasing:
                entity.handle('action', 'TRAP')
            else:
                entity.handle('action','HIDE')
                
     
