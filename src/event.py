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
        for node in entity.event.nodes:
            if node.id == node_id:
                entity.current_node = node
        
        if entity.current_node != None:
            # Apply effects
            if hasattr(entity.current_node, 'effects'):
                for target, delta in entity.current_node.effects._asdict().iteritems():
                    target_entity_ident, target_attr = target.split('_')
                    if target_entity_ident == 'human':
                        target_entities = {game.get_game().entity_manager.get_by_name(entity.event.location).humans[0]}
                    elif target_entity_ident == 'camp':
                        target_entities = {game.get_game().entity_manager.get_by_name('camp')}
                    elif target_entity_ident == 'all':
                        target_entities = game.get_game().entity_manager.get_by_tag('human')
                    
                    for target_entity in target_entities:
                        setattr(target_entity, target_attr, getattr(target_entity, target_attr) + delta)
            
            # Set text
            location = game.get_game().entity_manager.get_by_name(entity.event.location)
            if len(location.humans) > 0:
                human_name = location.humans[0].name
            else:
                human_name = ''
            entity.text = entity.current_node.text.format(human_name=human_name)
            
            # Clear old options and add new options
            for option_entity in entity.options:
                game.get_game().entity_manager.remove_entity(option_entity)
            
            entity.options = []
            
            for idx, option in enumerate(entity.current_node.options):
                option_entity = Entity('event-option', option=option, x=entity.x, y=entity.y+200+idx*100, event=entity)
                game.get_game().entity_manager.add_entity(option_entity)
                entity.options.append(option_entity)


class EventOptionComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['option', ('text', entity.option.text)])
        entity.register_handler('activate', self.handle_activate)
        
    def remove(self, entity):
        pass
    
    def handle_activate(self, entity):
        if not hasattr(entity.option, 'pass_'): # This is a terminal option
            for option_entity in entity.event.options:
                game.get_game().entity_manager.remove_entity(option_entity)
            game.get_game().entity_manager.remove_entity(entity.event)
            return
        
        
        entity.event.handle('change_node', entity.option.pass_)