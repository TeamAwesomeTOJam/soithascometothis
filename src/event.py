import game
from component import Component, verify_attrs
from entity import Entity


class EventComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['event', ('text', ''), 'x', 'y'])
        entity.register_handler('change_node', self.handle_change_node)
        
        entity.event = game.get_game().resource_manager.get('event', entity.event)
        entity.current_node = None
        entity.options = []
        self.handle_change_node(entity, 1)
    
    def remove(self, entity):
        for option_entity in entity.options:
            game.get_game().entity_manager.remove_entity(option_entity)
            
    def handle_change_node(self, entity, node_id):
        for node in entity.event:
            if node.id == node_id:
                entity.current_node = node
        
        if entity.current_node != None:
            entity.text = entity.current_node.text
            
            for option_entity in entity.options:
                game.get_game().entity_manager.remove_entity(option_entity)
            
            entity.options = []
            
            for idx, option in enumerate(entity.current_node.options):
                option_entity = Entity('event-option', option=option, x=entity.x, y=entity.y+200+idx*100, event=entity)
                game.get_game().entity_manager.add_entity(option_entity)
                entity.options.append(option_entity)

    def handle_draw(self, entity, surface):
        pass

class EventOptionComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['option', ('text', entity.option.text)])
        entity.register_handler('activate', self.handle_activate)
        
    def remove(self, entity):
        pass
    
    def handle_activate(self, entity):
        entity.event.handle('change_node', entity.option.pass_)