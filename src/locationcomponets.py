from component import Component
import game
from util import *

class FarmComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            energy_needed = mid()
            if h.energy >= energy_needed:
                h.energy -= energy_needed
                food_farmed = min(mid(),100 - camp().food)
                camp().food += food_farmed
                h.strength = clamp(h.strength + small())
                report('Farm', '%s collected %s food.' %(h.name, str(food_farmed)))
            else:
                report('Farm',"%s was to tired to work on the farm." % h.name)

class WallsComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            energy_needed = mid()
            if h.energy >= energy_needed:
                h.energy -= energy_needed
                h.strength = clamp(h.strength + small())
                amount_repaired = min(mid(), camp().defense)
                camp().defense += amount_repaired
                report('Walls', '%s improved the walls by %s.' % (h.name, amount_repaired))
            else:
                report('Walls', '%s was to tired to repair the walls.' % h.name)

class RestComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            if camp().shelter < 20:
                amount_rested = min(small(), 100 - h.energy)
                h.energy += amount_rested
                report('Rest', '%s got a bit of rest in the poor shelter and gained %s energy.' % (h.name, amount_rested))
            elif camp().shelter < 70:
                amount_rested = min(mid(), 100 - h.energy)
                h.energy += amount_rested
                report('Rest', '%s got a good of rest in the mediocre shelter and gained %s energy.' % (h.name, amount_rested))
            else:
                amount_rested = min(big(), 100 - h.energy)
                h.energy += amount_rested
                report('Rest', '%s got a great of rest in the shelter and gained %s energy.' % (h.name, amount_rested))

class WorkComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            energy_needed = mid()
            if h.energy >= energy_needed:
                h.energy -= energy_needed
                h.strength = clamp(h.strength + small())
                amount_repaired = min(mid(), camp().shelter)
                camp().defense += amount_repaired
                report('Work', '%s improved the shelter by %s.' % (h.name, amount_repaired))
            else:
                report('Work', '%s was to tired to work on the shelter.' % h.name)


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
            game.get_game().entity_manager.get_by_name('camp').defense += 10
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
