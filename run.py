#! /bin/env python2

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'src'))
import game
import mode


g = game.Game((1280, 720), os.path.join(sys.path[0], 'res'))
g.run(mode.AttractMode())
