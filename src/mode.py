from abc import ABCMeta, abstractmethod

import game
import entity
from entity import Entity
from _pyio import __metaclass__


class Mode:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def enter(self):
        pass
    
    @abstractmethod
    def leave(self):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    

class AttractMode(Mode):
    
    def enter(self):
        self.music = game.get_game().resource_manager.get('sound', 'Prelude.ogg')
        self.music.play()
        game.get_game().entity_manager.add_entity(Entity('aiplayer1'))
        game.get_game().entity_manager.add_entity(Entity('aiplayer2'))
        game.get_game().renderer.cleanup()
    
    def leave(self):
        self.music.stop()
        for decoy in game.get_game().entity_manager.get_by_tag('decoy'):
            game.get_game().entity_manager.remove_entity(decoy)
            
        game.get_game().entity_manager.remove_entity(game.get_game().entity_manager.get_by_name('aiplayer1'))
        game.get_game().entity_manager.remove_entity(game.get_game().entity_manager.get_by_name('aiplayer2'))
        game.get_game().entity_manager.commit_changes()
        
        game.get_game().renderer.draw_modes = []
        game.get_game().renderer.player_draw_modes = []
    
    def handle_event(self, event):
        if event.action not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            game.get_game().change_mode(BetweenRoundMode(1.7))
        
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('aiplayer'):
            entity.handle('update', dt)
        for entity in game.get_game().entity_manager.get_by_tag('decoy'):
            entity.handle('update', dt)
    
    def draw(self):
        game.get_game().view.draw()
        game.get_game().renderer.render_title()
    
    
class GameOverMode(Mode):
    pass


class MorningMode(Mode):
    
    def __init__(self):
        pass
    
    def enter(self):
        humans = game.get_game().entity_manager.get_by_tag('human')
        for h in humans:
            h.handle('go_home')
    
    def leave(self):
        pass
    
    def handle_event(self, event):
        entity = game.get_game().entity_manager.get_by_name(event.target)
        entity.handle('input', event)
    
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
    
    def draw(self):
        game.get_game().view.draw()
        

class DayMode(Mode):
    
    def __init__(self):
        self.time_elapsed = 0
        self.ttl = 4
    
    def enter(self):
        self.time_elapsed = 0
    
    def leave(self):
        for location in game.get_game().entity_manager.get_by_tag('location'):
            location.handle('day')
        for location in game.get_game().entity_manager.get_by_tag('human'):
            location.handle('day')
            
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
        
        self.time_elapsed += dt
        if self.time_elapsed > self.ttl:
            game.get_game().change_mode(EveningMode())
    
    def draw(self):
        game.get_game().view.draw()
        
        
class EveningMode(Mode):

    def enter(self):
        pass    

    def leave(self):
        pass
    
    def handle_event(self, event):
        entity = game.get_game().entity_manager.get_by_name(event.target)
        entity.handle('input', event)
    
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
    
    def draw(self):
        game.get_game().view.draw()