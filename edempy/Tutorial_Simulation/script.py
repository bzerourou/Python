from edempy import Deck
import numpy as np

deck = Deck("Tutorial_Simulation.dem")


i = 50
nX = 1
nY = 1
nZ = 1

binnedAveVel, x, y, z = deck.timestep[i].particle[0].getBinnedProperty(nX, nY, nZ, 
option='velocity', average=True)
