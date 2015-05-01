import spatialmap


GRID_SIZE = 32


class EntityManager(object):
    
    def __init__(self):
        self.entities = set()
        self._entities_by_name = {}
        self._entities_by_tag = {}
        self._spatial_maps = {}
        self.remove_list = []
        self.add_list = []
    
    def add_entity(self, entity):
        self.add_list.append(entity)
    
    def remove_entity(self, entity):     
        self.remove_list.append(entity)
    
    def commit_changes(self):
        for entity in self.remove_list:
            if hasattr(entity, 'tags'):
                for tag in entity.tags:
                    self._entities_by_tag[tag].remove(entity)
                    try:
                        self._spatial_maps[tag].remove(entity)
                    except KeyError:
                        pass
            
            if hasattr(entity, 'name'):
                del self._entities_by_name[entity.name]
            
            self.entities.remove(entity)
            
        for entity in self.add_list:
            self.entities.add(entity)
            
            if hasattr(entity, 'name'):
                self._entities_by_name[entity.name] = entity
            
            if hasattr(entity, 'tags'):
                for tag in entity.tags:
                    if tag in self._entities_by_tag:
                        self._entities_by_tag[tag].add(entity)
                    else:
                        self._entities_by_tag[tag] = {entity}
                    
                    if tag in self._spatial_maps:
                        self._spatial_maps[tag].add(entity)
                    else:
                        self._spatial_maps[tag] = spatialmap.SpatialMap(GRID_SIZE)
                        self._spatial_maps[tag].add(entity)
        
        self.add_list = []
        self.remove_list = []
    
    def update_position(self, entity):
        for tag in entity.tags:
            self._spatial_maps[tag].update(entity)
        
    def get_by_name(self, name):
        return self._entities_by_name[name]
        
    def get_by_tag(self, tag):
        try:
            return self._entities_by_tag[tag]
        except KeyError:
            return set()
    
    def get_in_area(self, tag, rect, precise=True):
        try:
            return self._spatial_maps[tag].get(rect, precise)
        except KeyError:
            return set()