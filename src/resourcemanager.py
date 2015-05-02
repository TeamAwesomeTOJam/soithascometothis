import json
import os

import pygame

import freezejson
import game


class ResourceManager(object):
    
    def __init__(self, prefix):
        self.prefix = prefix
        self.loaders = {}
        self.cache = {}
    
    def register_loader(self, res_type, loader):
        self.loaders[res_type] = loader
    
    def get(self, res_type, key):
        try:
            return self.cache[(res_type, key)]
        except KeyError:
            value = self.loaders[res_type](self.prefix, key)
            self.cache[(res_type, key)] = value
            return value
    
    def clear(self):
        self.cache = {}
        
    
def LoadEntityData(prefix, key):
    with open(os.path.join(prefix, 'entities', key + '.json')) as in_file:
        definition = json.load(in_file)
    
    if 'animations' in definition:
        for animation in definition['animations'].values():
            if 'frame_dir' in animation:
                frame_dir = os.path.join(prefix, 'images', animation['frame_dir'])
                frames = sorted(os.listdir(frame_dir))
                animation['frames'] = []
                for frame in frames:
                    animation['frames'].append(os.path.join(frame_dir, frame))
    
    if 'includes' in definition:
        flattened = {}
        for include_name in definition['includes']:
            include = game.get_game().resource_manager.get('entity', include_name)
            for field in include._fields:
                flattened[field] = getattr(include, field)
        for key, value in definition.iteritems():
            if key.endswith('+'):
                base_key = key[:-1]
                flattened[base_key] = flattened.get(base_key, tuple()) + tuple(value)
            else:
                flattened[key] = value
        definition = flattened
    
    return freezejson.freeze_value(definition)
    
def LoadImage(prefix, key):
    image_surface = pygame.image.load(os.path.join(prefix, 'images', key))
    image_surface.set_alpha(None)
    image_surface.convert()
    if 'Doda' in key:
        image_surface.set_colorkey((255, 125, 255))
    elif not 'passable' in key:
        image_surface.set_colorkey((255, 0, 255))
    return image_surface

def LoadInputMapping(prefix, key):
    with open(os.path.join(prefix, 'inputmaps', key + '.json')) as in_file:
        mapping = json.load(in_file)
        
    return mapping

def LoadAnimation(prefix, key):
    with open(os.path.join(prefix, 'animations', key + '.json')) as in_file:
        animation = json.load(in_file)

    if 'frame_dir' in animation:
        frame_dir = os.path.join(prefix, 'images', animation['frame_dir'])
        frames = sorted(os.listdir(frame_dir))
        animation['frames'] = []
        for frame in frames:
            animation['frames'].append(os.path.join(frame_dir, frame))
                
    return freezejson.freeze_value(animation)
                    
def LoadSound(prefix, key):
    return pygame.mixer.Sound(os.path.join(prefix, 'sounds', key))

<<<<<<< Upstream, based on origin/master
def LoadText(prefix, key):
    f = open(os.path.join(prefix, 'text', key),'r')
    return f.read()
=======
def LoadEvent(prefix, key):
    with open(os.path.join(prefix, 'events', key + '.json')) as in_file:
        event = json.load(in_file)
    
    # ???
    
    return freezejson.freeze_value(event)
>>>>>>> b4f332f More work towards event stuff.
