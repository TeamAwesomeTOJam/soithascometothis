class ComponentManager(object):

    def __init__(self):
        self.components = {}
        
    def register_component(self, component):
        self.components[component.__class__.__name__] = component
        
    def add(self, name, entity):
        self.components[name].add(entity)
        
    def remove(self, name, entity):
        self.components[name].remove(entity)
        