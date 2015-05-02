from component import Component


class ComponentManager(object):

    def __init__(self):
        self.components = {}
        
    def register_component(self, component):
        print component.__class__.__name__
        self.components[component.__class__.__name__] = component
        
    def register_module(self, module):
        for name, value in module.__dict__.iteritems():
            try:
                if issubclass(value, Component):
                    self.components[name] = value()
            except Exception , e:
                print e
        
    def add(self, name, entity):
        self.components[name].add(entity)
        
    def remove(self, name, entity):
        self.components[name].remove(entity)
        