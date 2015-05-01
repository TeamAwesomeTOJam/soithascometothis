import game
from component import verify_attrs, get_midpoint
import mode


class DrawScoreComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['target', 'x', 'y', 'direction', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
    
    def handle_draw(self, entity):
        player = game.get_game().entity_manager.get_by_name(entity.target)
        radius = entity.height/2
        
        if player.chasing:
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y, entity.width, entity.height)
        else:
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y, entity.width, entity.height)
        
        for i in range(player.score):
            if entity.direction == 1:
                start_x = entity.x + radius
            else:
                start_x = entity.x + entity.width - radius
            pos = (start_x + (i * radius * 2 * entity.direction), entity.y + radius)
            game.get_game().renderer.appendCircle(player.color, pos[0], pos[1], radius)


class DrawTimerComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['time_limit', ('time_remaining', entity.time_limit), 'x', 'y', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity):
        ratio = entity.time_remaining / entity.time_limit
        x, y = get_midpoint(entity)
        game.get_game().renderer.appendCircle((50,50,50), x, y, entity.width/2)
        game.get_game().renderer.appendFan((200,200,200), x, y, entity.width/2, ratio)
    

class UpdateTimerComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['time_limit', ('time_remaining', entity.time_limit), 'x', 'y', 'width', 'height'])
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        
    def handle_update(self, entity, dt):
        entity.time_remaining -= dt
        if entity.time_remaining < 0:
            game.get_game().change_mode(mode.BetweenRoundMode())
        

class DrawActionsComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['target', 'x', 'y', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity):
        player = game.get_game().entity_manager.get_by_name(entity.target)
        if player.chasing:
            top_bar_ratio = 1 - player.speed_boost_activation_cooldown / player.speed_boost_activation_cooldown_time
            bottom_bar_ratio = 1 - player.minefield_cooldown / player.minefield_cooldown_time
            bottom_bottom_bar_ratio = 1 - player.trap_cooldown / player.trap_cooldown_time
        else:
            top_bar_ratio = 1 - player.smoke_screen_cooldown / player.smoke_screen_cooldown_time
            bottom_bar_ratio = 1 - player.decoy_cooldown / player.decoy_cooldown_time
            bottom_bottom_bar_ratio = 1 - player.invisibility_cooldown / player.invisibility_cooldown_time
        
        if entity.direction == 1:
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y, entity.width, entity.height/3 - 2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y, entity.width * top_bar_ratio, entity.height/3 - 2)
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y + entity.height/3 + 2, entity.width, entity.height/3 - 2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y + entity.height/3 + 2, entity.width * bottom_bar_ratio, entity.height/3 - 2)
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y + 2*entity.height/3 + 2, entity.width, entity.height/3 - 2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y + 2*entity.height/3 + 2, entity.width * bottom_bottom_bar_ratio, entity.height/3 - 2)
        else:
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y, entity.width, entity.height/3 - 2)
            game.get_game().renderer.appendRect((200,200,200), entity.x + entity.width * (1 - top_bar_ratio), entity.y, entity.width * top_bar_ratio, entity.height/3 - 2)
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y + entity.height/3 + 2, entity.width, entity.height/3 - 2)
            game.get_game().renderer.appendRect((200,200,200), entity.x + entity.width * (1- bottom_bar_ratio), entity.y + entity.height/3 + 2, entity.width * bottom_bar_ratio, entity.height/3 - 2)
            game.get_game().renderer.appendRect((50,50,50), entity.x, entity.y + 2*entity.height/3 + 2, entity.width, entity.height/3 - 2)
            game.get_game().renderer.appendRect((200,200,200), entity.x + entity.width * (1- bottom_bottom_bar_ratio), entity.y + 2*entity.height/3 + 2, entity.width * bottom_bottom_bar_ratio, entity.height/3 - 2)
