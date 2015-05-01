import game
import entity
from entity import Entity


class AttractMode(object):
    
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
    

class PlayMode(object):

    def enter(self):
        self.music = game.get_game().resource_manager.get('sound', 'Main Body.ogg')
        self.music.play(loops=-1)
        game.get_game().renderer.cleanup()
        game.get_game().entity_manager.add_entity(entity.Entity("vortexspawner"))
    
    def leave(self):
        player1 = game.get_game().entity_manager.get_by_name('player1')
        player2 = game.get_game().entity_manager.get_by_name('player2')
        timer = game.get_game().entity_manager.get_by_name('timer')
                
        if (player1.chasing and timer.time_remaining < 0) or (player2.chasing and timer.time_remaining >= 0):
            winner = player2
            player2.winner = True
            player1.winner = False
        else:
            winner = player1
            player1.winner = True
            player2.winner = False
            
        winner.score += 1
    
        for player in [player1, player2]:
            player.chasing = False if player.chasing else True   
            player.x = player.static.x
            player.y = player.static.y
            player.dx = 0
            player.dy = 0
            
        for decoy in game.get_game().entity_manager.get_by_tag('decoy'):
            game.get_game().entity_manager.remove_entity(decoy)
        
        for vortex in game.get_game().entity_manager.get_by_tag('vortex'):
            game.get_game().entity_manager.remove_entity(vortex)  
            
        for vortexspawner in game.get_game().entity_manager.get_by_tag('vortexspawner'):
            game.get_game().entity_manager.remove_entity(vortexspawner)          
            
        timer.time_remaining = timer.time_limit
        self.music.stop()
        
        game.get_game().renderer.draw_modes = []
        game.get_game().renderer.player_draw_modes = []
        
    def handle_event(self, event):
        entity = game.get_game().entity_manager.get_by_name(event.target)
        entity.handle('input', event)
            
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
            
    def draw(self):
        game.get_game().view.draw()
        game.get_game().renderer.render_play()


class BetweenRoundMode(object):
    
    def __init__(self, ttl = 4):
        self.ttl = ttl
    
    def enter(self):
        self.music = game.get_game().resource_manager.get('sound', 'Drums Intro.ogg')
        self.music.play(loops=-1)
        #game.get_game().background_view.draw()
        game.get_game().renderer.cleanup()
        
    def leave(self):
        self.music.stop()
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        player1 = game.get_game().entity_manager.get_by_name('player1')
        player2 = game.get_game().entity_manager.get_by_name('player2')
        
        if player1.score == 3 or player2.score == 3:
            player1.score = 0
            player2.score = 0
            player1.chasing = True
            player2.chasing = False
            
            game.get_game().change_mode(GameEndMode())
        
        self.ttl -= dt
        if self.ttl < 0:
            game.get_game().change_mode(PlayMode())
    
    def draw(self):
        if self.ttl > 2:
            player1 = game.get_game().entity_manager.get_by_name('player1')
            player2 = game.get_game().entity_manager.get_by_name('player2')
            if player1.chasing:
                ncolor = player1.color
            else:
                ncolor = player2.color
            if player1.winner:
                game.get_game().renderer.render_victor(0,player1.color,ncolor)
            else:
                game.get_game().renderer.render_victor(0,player2.color,ncolor)
        elif self.ttl > 1.3:
            game.get_game().renderer.render_victor(1)
        elif self.ttl > 0.7:
            game.get_game().renderer.render_victor(2)
        else:
            game.get_game().renderer.render_victor(3)
        

class GameEndMode(object):
    
    def __init__(self):
        self.ttl = 5
    
    def enter(self):
        pass
    
    def leave(self):
        pass
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        self.ttl -= dt
        if self.ttl < 0:
            game.get_game().change_mode(AttractMode())
    
    def draw(self):
        player1 = game.get_game().entity_manager.get_by_name('player1')
        player2 = game.get_game().entity_manager.get_by_name('player2')
        if player1.score > player2.score:
            game.get_game().renderer.render_game_end()
        else:
            game.get_game().renderer.render_game_end()  
