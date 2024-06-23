

import edempy.Deck as Deck 

deck = Deck('Cohesion_and_Conveyor.dem')



import matplotlib.pyplot as plt
from   mpl_toolkits.mplot3d import Axes3D


# nompbre de géométries
nGeoms = deck.numGeoms

fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
# parcourir toutes les géométries 
for i in range(0,nGeoms):
    x = deck.creatorData.geometry[i].getXCoords()
    y = deck.creatorData.geometry[i].getYCoords()
    z = deck.creatorData.geometry[i].getZCoords()
    tri = deck.creatorData.geometry[i].getTriangleNodes()
    ax.plot_trisurf(x, y, z, triangles=tri, alpha=0.2, color='lightgrey')
plt.show()