import sys
import pygame
import random

import component
import componentmanager
from entitymanager import EntityManager
from resourcemanager import ResourceManager, LoadEntityData, LoadImage, LoadInputMapping, LoadSound, LoadText
from entity import Entity
from render import View, BackgroundLayer, SimpleLayer, SolidBackgroundLayer
from input import InputManager
from vec2d import Vec2d


_game = None


class Game(object):
    
    def __init__(self, screen_size, resource_path):
        global _game
        _game = self
        
        self.mode = None
        self.running = False
        self.screen_size = screen_size
        
        pygame.mixer.pre_init(frequency=48000)
        pygame.init()
        pygame.display.set_caption("It's All Come to This")
                                   
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
        
        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_module(component)
        
        self.entity_manager = EntityManager()
            
        self.resource_manager = ResourceManager(resource_path)
        self.resource_manager.register_loader('entity', LoadEntityData)
        self.resource_manager.register_loader('image', LoadImage)
        self.resource_manager.register_loader('inputmap', LoadInputMapping)
        self.resource_manager.register_loader('sound', LoadSound)
        self.resource_manager.register_loader('text', LoadText)

        self.input_manager = InputManager()
        self.view = View(pygame.display.get_surface(), [SolidBackgroundLayer((0,0,0,0)), 
                                                        SimpleLayer('draw'), 
                                                        SimpleLayer('draw-ui')])
        
    def run(self, mode):
        self.entity_manager.add_entity(Entity('camp'))
        self.entity_manager.add_entity(Entity('report'))
        
        origin = Vec2d(600, 200)
        num_humans = 6
        
        names = self.resource_manager.get('text','names.txt').split('\n')
        
        for i in range(num_humans):
            pos = Vec2d(100,0).rotated(360.0*i/(num_humans)) + origin
            self.entity_manager.add_entity(Entity('human', name=random.choice(names), home_x = pos.x, home_y = pos.y))
        
        self.entity_manager.add_entity(Entity('mouse'))
        
        self.entity_manager.add_entity(Entity('farm'))
        
        self.entity_manager.add_entity(Entity("camp"))
        
        self.entity_manager.add_entity(Entity('camp-food-meter-ui'))
        self.entity_manager.add_entity(Entity('camp-defense-meter-ui'))
        self.entity_manager.add_entity(Entity('camp-shelter-meter-ui'))
        self.entity_manager.add_entity(Entity('camp-water-meter-ui'))
        self.entity_manager.add_entity(Entity('camp-medicine-meter-ui'))
        self.entity_manager.add_entity(Entity('button'))

        self.entity_manager.commit_changes()

        self.change_mode(mode)
        self.running = True

        self.entity_manager.commit_changes()
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            events = self.input_manager.process_events()
            for event in events:
                if event.target == 'GAME':
                    if event.action == 'QUIT' and event.value > 0:
                        self.running = False
                    elif event.action == 'FULLSCREEN' and event.value > 0:
                        pygame.display.toggle_fullscreen()
                    elif event.action == 'RELOAD' and event.value > 0:
                        self.resource_manager.clear()
                else:
                    self.mode.handle_event(event)
            
            self.mode.update(dt)
            self.mode.draw()
            
            self.entity_manager.commit_changes()
            pygame.display.flip()
            
    def change_mode(self, new_mode):
        print self.mode, '->', new_mode
        if self.mode:
            self.mode.leave()
        self.mode = new_mode
        self.mode.enter()

def get_game():
    return _game
