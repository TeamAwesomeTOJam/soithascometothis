import pygame
import game


class Render(object):
    pass


class View(object):
    
    def __init__(self, layers=None, entity_name=None):
        self.layers = layers if layers != None else []
        self.entity_name = entity_name
    
    @property
    def entity(self):
        if self.entity_name:
            return game.get_game().entity_manager.get_by_name(self.entity_name)
    
    def add_layer(self, layer):
        self.layers.append(layer)
        
    def draw(self):
#         self.surface.set_clip(self.area)
        
        for layer in self.layers:
            layer.draw(self)
            
#         self.surface.set_clip(None)


class StaticLayer(object):
    
    def __init__(self, size, tag):
        self.size = size
        self.tag = tag
        self.surface = pygame.Surface(self.size)
        self.surface.convert()
        
        transform = lambda x, y : (x, y)
        
        for entity in game.get_game().entity_manager.get_by_tag(tag):
            entity.handle('draw', self.surface, transform)
        
    def draw(self, view):
        area_to_blit = pygame.Rect(view.area)
        area_to_blit.center = (view.entity.x, view.entity.y)
        view.surface.blit(self.surface, view.area, area_to_blit)
    

class DepthSortedLayer(object):
    
    def __init__(self, tag):
        self.tag = tag
        
    def draw(self, view):
        area_to_blit = pygame.Rect(view.area)
        area_to_blit.center = (view.entity.x, view.entity.y)   

        entities_to_draw = sorted(game.get_game().entity_manager.get_in_area(self.tag, area_to_blit, precise=False), key=lambda entity: entity.y)

        transform = lambda x, y : (x - area_to_blit.x + view.area.x, y - area_to_blit.y + view.area.y)
        
        for entity in entities_to_draw:
            entity.handle('draw', view.surface, transform)


class BackgroundLayer(object):
    
    def draw(self, view):
        r = pygame.Rect(view.area)
        p = 1
        for x in xrange(0, view.area.width, 100):
            r.left = x
            pygame.draw.rect(view.surface, game.get_game().entity_manager.get_by_name('player' + str(1+p)).color, r)
            p = (p + 1) % 2
            

class SolidBackgroundLayer(object):
    
    def __init__(self, color):
        self.color = color
    
    def draw(self, view):
        r = pygame.Rect(view.area)
        pygame.draw.rect(view.surface, self.color, r)
            

class SimpleLayer(object):
    
    def __init__(self, tag):
        self.tag = tag
        
    def draw(self, view):        
        for entity in game.get_game().entity_manager.get_by_tag(self.tag):
            entity.handle('draw')
