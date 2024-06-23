import edempy.Deck as Deck 
from edempy import BoxBin, CylinderBin
import matplotlib.pyplot as plt

deck = Deck('Tutorial_Simulation.dem')

#on crée une boite pour représenter notre équipement  
boxbin = BoxBin([-0.4924039, 0.0, 0.08682409], [0.4924039, 0.0, -0.08682409], 0.3)

# initialiser la masse totale
total_mass =[0]

for i in range(1, deck.numTimesteps):
    # on récupère ID de chaque particule
    pIds = deck.timestep[i].particle[0].getIds()
    # vecteur positions
    pPos = deck.timestep[i].particle[0].getPositions()
    # assurer que y a présence 
    ids_inside = boxbin.getBinnedObjects(pIds, pPos)
    mass_inside = 0
    # parcourir les particules présentes
    for id_inside in ids_inside:
        # récupère et somme les masses
        mass_inside += deck.timestep[i].particle[0].getMass(id_inside)
    # ajoute la somme des masses à la notre liste     
    total_mass.append(mass_inside)
# récupère tous les pas du temps    
time_values = deck.timestepValues

# tracer la courbe de masse en fonction du temps
plt.figure(figsize=(7, 5), dpi=120)
plt.plot(time_values,total_mass, linewidth=2.5, color='cyan')
plt.xlabel('Temps (s)', fontsize = 13, fontname = 'Arial')
plt.ylabel('Masse dans le Mixeur (kg)', fontsize = 13, fontname = 'Arial')
plt.grid(True)
plt.show()