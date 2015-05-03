from component import Component, verify_attrs

class FarmComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').food += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Farm', 'A tough day on the farm. Gained 10 food, but %s lost 10 energy.' % entity.humans[0].name)

class WallsComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').defense += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Walls', 'Working on the walls. Defenses improved by 10, but %s lost 10 energy.' % entity.humans[0].name)

class RestComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Walls', '%s is well rested and gained 10 energy.' % entity.humans[0].name)

class WorkComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').shelter += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Walls', 'Improved the shelter by 10, but %s lost 10 energy.' % entity.humans[0].name)


class WellComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').water += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Well', 'Hauling water from the well. Got 10 water, but %s lost 10 energy.' % entity.humans[0].name)