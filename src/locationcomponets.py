from component import Component
import game
from util import *
import random

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
                amount_repaired = min(mid(), 100 - camp().defense)
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
                amount_repaired = min(mid(), 100 - camp().shelter)
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
            h = entity.humans[0]
            energy_needed = small()
            if h.energy >= energy_needed:
                h.energy -= energy_needed
                h.strength = clamp(h.strength + small())
                amount_collected = min(mid(), 100 - camp().water)
                camp().water += amount_collected
                report('Work', '%s collected %s water.' % (h.name, amount_collected))
            else:
                report('Work', '%s was to tired to haul water.' % h.name)

class InfirmaryComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            medicine_needed = mid()
            if camp().medicine >= medicine_needed:
                amount_rested = min(small(), 100 - h.energy)
                h.energy += amount_rested
                amount_healed = min(mid(), 100 - h.health)
                h.health += amount_healed
                report('Infirmary', '%s healed %s health and gained %s energy.' % (h.name, amount_healed, amount_rested))
            else:
                report('Infirmary', 'There was not enough medicine to heal %s.' % h.name)

class ExploreComponent(Component):
    
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
                num = random.randrange(0, 100)
                if num < 15:
                    food_found = min(big(),100 - camp().food)
                    camp().food += food_found
                    report('Explore','%s found %s food.' % (h.name, food_found))
                elif num < 30:
                    water_found = min(big(),100 - camp().water)
                    camp().water += water_found
                    report('Explore','%s found %s water.' % (h.name, water_found))
                elif num < 45:
                    medicine_found = min(big(),100 - camp().medicine)
                    camp().medicine += medicine_found
                    report('Explore','%s found %s medicine.' % (h.name, medicine_found))
                else:
                    report('Explore',"%s couldn't find anything." % h.name)
            else:
                report('Explore',"%s did not have the energy to go exploring." % h.name)
        
        
        if entity.humans:
            entity.humans[0].energy -= 10
            game.get_game().entity_manager.get_by_name('camp').medicine += 10
            game.get_game().entity_manager.get_by_name('report').handle('record_update', 'Explore', '%s found 10 medicine but lost 10 energy.' % entity.humans[0].name)

class HospitalComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', []), 'medicine'])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            if entity.medicine <= 0:
                report('Hospital','There is nothing left to find at the hospital')
                return
            amount = None
            msg = ''
            num = random.randrange(0,100)
            if num < 25:
                amount = small
                msg = '%s only found %s medicine at the hospital'
            elif num < 75:
                amount = mid
                msg = '%s found %s medicine at the hospital'
            elif num < 85:
                amount = big
                msg = '%s hit the jackpot and found %s medicine at the hospital'
            else:
                wounds = min(h.health, mid())
                h.health -= wounds
                report('Hospital','%s got sick at the hospital and lost %s health' % (h.name, wounds))
                return
            medicine_found = min(min(amount(),entity.medicine), 100 - camp().medicine)
            camp().medicine += medicine_found
            report('Hospital', msg % (h.name, medicine_found))

class RivalCampComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            enemy_strength = random.randrange(15, 75)
            if h.strength <= enemy_strength:
                wounds = min(h.health, big())
                h.health -= wounds
                report('Rival Camp','%s was not strong enough to fight and lost %s health' % (h.name, wounds))
                return
            num = random.randrange(0,100)
            if num < 33:
                food_found = min(big(), 100 - camp().food)
                camp().food += food_found
                wounds = min(h.health, mid())
                h.health -= wounds
                report('Rival Camp', '%s managed to steal %s food but got into a fight and lost %s health' %(h.name, food_found, wounds))
            elif num < 66:
                water_found = min(big(), 100 - camp().water)
                camp().water += water_found
                wounds = min(h.health, mid())
                h.health -= wounds
                report('Rival Camp', '%s managed to steal %s water but got into a fight and lost %s health' %(h.name, water_found, wounds))
            else:
                medicine_found = min(big(), 100 - camp().medicine)
                camp().medicine += medicine_found
                wounds = min(h.health, mid())
                h.health -= wounds
                report('Rival Camp', '%s managed to steal %s medicine but got into a fight and lost %s health' %(h.name, medicine_found, wounds))

class WaterTowerComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', []), 'water'])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            if entity.water <= 0:
                report('Water Tower','There is nothing left to find at the water tower.')
                return
            amount = None
            msg = ''
            num = random.randrange(0,100)
            if num < 15:
                amount = small
                msg = '%s only collected %s water at the water tower.'
            elif num < 75:
                amount = mid
                msg = '%s collected %s water at the water tower.'
            elif num < 90:
                amount = big
                msg = '%s hit the jackpot and collected %s water at the water tower.'
            else:
                wounds = min(h.health, mid())
                h.health -= wounds
                report('Water Tower','%s fell off the water tower and lost %s health' % (h.name, wounds))
                return
            water_found = min(min(amount(),entity.water), 100 - camp().water)
            camp().water += water_found
            report('Water Tower', msg % (h.name, water_found))

class ForestComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            enemy_strength = random.randrange(15, 50)
            if h.strength <= enemy_strength:
                wounds = min(h.health, big())
                h.health -= wounds
                report('Forest','%s was attacked by wild animals and lost %s health' % (h.name, wounds))
                return
            amount = None
            msg = ''
            num = random.randrange(0,100)
            if num < 15:
                amount = small
                msg = '%s only collected %s food in the forest.'
            elif num < 75:
                amount = mid
                msg = '%s collected %s food in the forest.'
            elif num < 90:
                amount = big
                msg = '%s hit the jackpot and collected %s food in the forest.'
            else:
                report('Forest','%s couldn\'t find any food in the forest' % h.name)
                return
            food_found = min(amount(), 100 - camp().food)
            camp().food += food_found
            report('Forest', msg % (h.name, food_found))

class ConstructionSiteComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            enemy_strength = random.randrange(15, 75)
            num = random.randrange(0,100)
            if num < 33:
                shelter_found = min(big(), 100 - camp().shelter)
                camp().shelter += shelter_found
                report('Construction Site', '%s found materials to improve the shelter by %s.' %(h.name, shelter_found))
            elif num < 66:
                defense_found = min(big(), 100 - camp().defense)
                camp().defense += defense_found
                report('Construction Site', '%s found materials to improve the walls by %s' %(h.name, defense_found))
            else:
                wounds = min(h.health, mid())
                h.health -= wounds
                report('Rival Camp', '%s was injured while exploring the construction site and lost %s health' %(h.name, wounds))

class DumpComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, [('humans', [])])
        entity.register_handler('day', self.handle_day)
        
    def remove(self, entity):
        entity.unregister_handler('day', self.handle_day)
        
    def handle_day(self, entity):
        if entity.humans:
            h = entity.humans[0]
            num = random.randrange(0,100)
            if num < 33:
                shelter_found = min(mid(), 100 - camp().shelter)
                camp().shelter += shelter_found
                report('Dump', '%s found materials to improve the shelter by %s.' %(h.name, shelter_found))
            elif num < 66:
                defense_found = min(mid(), 100 - camp().defense)
                camp().defense += defense_found
                report('Dump', '%s found materials to improve the walls by %s' %(h.name, defense_found))
            else:
                report('Dump', '%s found nothing of value at the dump' %h.name)