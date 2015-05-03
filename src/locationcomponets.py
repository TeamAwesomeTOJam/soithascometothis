from component import Component, verify_attrs
import game

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
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Rest', '%s is well rested and gained 10 energy.' % entity.humans[0].name)

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
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Work', 'Improved the shelter by 10, but %s lost 10 energy.' % entity.humans[0].name)


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

class InfirmaryComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].health += 10
            game.get_game().entity_manager.get_by_name('camp').medicine -= 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Infirmary', 'Used 10 medicine to heal %s lost 10 health.' % entity.humans[0].name)

class ExploreComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').medicine += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Explore', '%s found 10 medicine but lost 10 energy.' % entity.humans[0].name)

class HospitalComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').medicine += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Hospital', '%s found 10 medicine in the hospital but lost 10 energy' % entity.humans[0].name)

class RivalCampComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].health -= 10
            game.get_game().entity_manager.get_by_name('camp').food += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Rival Camp', '%s stole 10 food from the rivals but was wounded and lost 10 health' % entity.humans[0].name)

class WaterTowerComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').water += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Water Tower', '%s found 10 water but lost 10 energy' % entity.humans[0].name)

class ForestComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').food += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Forest', '%s went hunting and got 10 food but lost 10 energy' % entity.humans[0].name)

class ConstructionSiteComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').walls += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Construction Site', '%s found materials to improve the shelter by 10 but lost 10 energy' % entity.humans[0].name)

class DumpComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').food += 1
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Dump', '%s found 1 food and lost 10 energy' % entity.humans[0].name)
