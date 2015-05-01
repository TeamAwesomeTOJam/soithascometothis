import sys
import pygame
import componentmanager
from entitymanager import EntityManager
from resourcemanager import ResourceManager, LoadEntityData, LoadImage, LoadInputMapping, LoadSound
from component import (AnimationComponent,
                       MovementComponent,
                       ExampleComponent, 
                       InputMovementComponent, 
                       DrawComponent, 
                       DrawHitBoxComponent,
                       PlayerCollisionComponent)

from graphicscomponents import DrawCircleComponent

from aiplayercomponents import AIActionComponent, AIMovementComponent

from gamecomponents import (SmokeScreenComponent,
                            DecoyMovementComponent,
                            SelfDestructComponent,
                            SpawnDecoyComponent,
                            MinefieldComponent,
                            SpeedBoostComponent,
                            ButtonInterpreterComponent,
                            TrapComponent,
                            HideComponent)

from uicomponents import DrawScoreComponent, DrawTimerComponent, UpdateTimerComponent, DrawActionsComponent

from vortexcomponents import DrawVortextComponent, GrowVortextComponent, SpawnVortexComponent
from entity import Entity

from render import View, BackgroundLayer, SimpleLayer, SolidBackgroundLayer
from input import InputManager
from opengl import GLRenderer


_game = None


class Game(object):
    
    def __init__(self, screen_size, resource_path):
        global _game
        _game = self
        
        self.mode = None
        self.running = False
        self.screen_size = screen_size
        
        pygame.mixer.pre_init(frequency=44100)
        pygame.init()
        pygame.display.set_caption('After You!')
                                   
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size, pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
        
        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_component(MovementComponent())
        self.component_manager.register_component(ExampleComponent())
        self.component_manager.register_component(AnimationComponent())
        self.component_manager.register_component(DrawComponent())
        self.component_manager.register_component(InputMovementComponent())
        self.component_manager.register_component(DrawHitBoxComponent()) 
        self.component_manager.register_component(DrawCircleComponent())
        self.component_manager.register_component(SmokeScreenComponent())
        self.component_manager.register_component(PlayerCollisionComponent())
        self.component_manager.register_component(DecoyMovementComponent())
        self.component_manager.register_component(SelfDestructComponent())
        self.component_manager.register_component(SpawnDecoyComponent())
        self.component_manager.register_component(DrawScoreComponent())
        self.component_manager.register_component(MinefieldComponent())
        self.component_manager.register_component(DrawTimerComponent())
        self.component_manager.register_component(UpdateTimerComponent())
        self.component_manager.register_component(SpeedBoostComponent())
        self.component_manager.register_component(ButtonInterpreterComponent())
        self.component_manager.register_component(DrawActionsComponent())
        self.component_manager.register_component(SpawnVortexComponent())
        self.component_manager.register_component(DrawVortextComponent())
        self.component_manager.register_component(GrowVortextComponent())
        self.component_manager.register_component(TrapComponent())
        self.component_manager.register_component(HideComponent())
        self.component_manager.register_component(AIActionComponent())
        self.component_manager.register_component(AIMovementComponent())
        
        self.entity_manager = EntityManager()
            
        self.resource_manager = ResourceManager(resource_path)
        self.resource_manager.register_loader('data', LoadEntityData)
        self.resource_manager.register_loader('image', LoadImage)
        self.resource_manager.register_loader('inputmap', LoadInputMapping)
        self.resource_manager.register_loader('sound', LoadSound)

        self.input_manager = InputManager()
        
        self.renderer = GLRenderer()
        self.renderer.resize(self.screen_size)
       
        self.view = View([SimpleLayer('draw'), SimpleLayer('ui')])
        
    def run(self, mode):
        p1 = Entity("player1")
        p2 = Entity("player2")
        self.entity_manager.add_entity(p1)
        self.entity_manager.add_entity(p2)
        self.entity_manager.add_entity(Entity("scoreui-player1"))
        self.entity_manager.add_entity(Entity("scoreui-player2"))
        self.entity_manager.add_entity(Entity("actionui-player1"))
        self.entity_manager.add_entity(Entity("actionui-player2"))
        self.entity_manager.add_entity(Entity("timerui"))
        
        
        
        self.renderer.createBackground()

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
        if self.mode:
            self.mode.leave()
        self.mode = new_mode
        self.mode.enter()

def get_game():
    return _game
