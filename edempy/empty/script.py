# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 12:58:24 2024

@author: PC
"""

from edempy import Deck
import numpy as np

deck = Deck("empty.dem", mode='w')

# To create a bulk material, the last argument must be set to True
deck.createMaterial('BulkMaterial', 0.25, 10_000_000, 4100, 0, True) 

# Add a particle to the bulk material
deck.createMultisphereParticleType('BulkMaterial', particle_name = 'MyParticle')

# Set the position and radius of each sphere in MyParticle
deck.setMultisphereSpherePosition('MyParticle', 0, [0.0, 0.004, 0.0])
deck.setMultispherePhysicalRadius('MyParticle', 0, 0.005)
deck.setMultisphereSpherePosition('MyParticle', 1, [-0.00346, -0.002, 0.0])
deck.setMultispherePhysicalRadius('MyParticle', 1, 0.005)
deck.setMultisphereSpherePosition('MyParticle', 2, [0.00346, -0.002, 0.0])
deck.setMultispherePhysicalRadius('MyParticle', 2, 0.005)

# Enable auto-calculation of particle properties
deck.setAutoCalculateParticleProperties('MyParticle', True)

# To create the equipment material, the last argument must be set to False
deck.createMaterial('EquipMaterial', 0.30, 70_000_000_000, 7800, 0, False)


# Define particle-particle interactions
deck.createInteraction('BulkMaterial', 'BulkMaterial', 0.36, 0.64, 0.13)

# Define particle-geometry interactions
deck.createInteraction('BulkMaterial', 'EquipMaterial', 0.40, 0.45, 0.15)

# Define the 4 corners of the square
square_coords = np.array([[-0.5, -0.5, 0.5],[0.5, -0.5, 0.5],[0.5, 0.5, 0.5],[-0.5, 0.5, 0.5]])

# Define the 2 triangles that make up the square
square_triangles = np.array([[0,3,1], [1,3,2]])

# Define the 8 corners of the cube
cube_coords= np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]])
    
# Define the 12 triangles that make up the cube 
cube_triangles= np.array([[0,3,1],[1,3,2],[0,4,7],[0,7,3],[4,5,6],[4,6,7],[5,1,2],[5,2,6],[2,3,6],[3,7,6],[0,1,5],[0,5,4]])

# Create the square
deck.createGeometry('MySquare', 'EquipMaterial', square_coords, square_triangles, geometry_type='Virtual')

# Create the cube
deck.createGeometry('MyCube', 'EquipMaterial', cube_coords, cube_triangles, geometry_type='Physical')

# Set geometry motion - linear rotation
rotation_in_rpm = 10
rotation_in_rad_s = rotation_in_rpm * (2*np.pi/60)
deck.createKinematic('MyCube', kinematic_name= 'Cube_rotation', kinematic_type= 'Linear Rotation', start_time= 2.0, 
                     rotation_init_angular_velocity_value= rotation_in_rad_s, rotation_start_point= [0.0, 0.0, -1.0], 
                     rotation_end_point= [0.0, 0.0, 1.0])  

# Create particle factory
deck.createFactory('MySquare', 'BulkMaterial_Factory', 'BulkMaterial', velocity= 'fixed', fixed_velocity=[0.0, 0.0, -1.0], 
                   start_time= 0, is_mass_creation= False, total_to_create= 30_000, is_mass_generation= False,
                   creation_rate= 15_000)

# Define the particle size distribution
scales = np.array([1.0, 1.2, 1.5, 1.7])
mass_percentages = np.array([45, 30, 5, 20])
deck.setParticleUserDefinedSizeDistribution('MyParticle', scales, mass_percentages, is_scaled_by_radius= True)

# Delete the default Hertz-Mindling model
deck.deletePhysicsModelSurfSurf('Hertz-Mindlin (no slip)')

# Define the JKR surface energy
model_data=np.array([('BulkMaterial', 'BulkMaterial', 2)], dtype=([('name1', 'S256'), ('name2', 'S256'), ('value', '<f8')]))

# Add the particle-particle contact model
deck.createPhysicsModelSurfSurf('Hertz-Mindlin with JKR',{"data": model_data})

# Add the particle-geometry contact model
deck.createPhysicsModelSurfGeom('Relative Wear',{})

# Set the minimum values of the simulation domain
deck.setDomainMin([-1.01, -1.01, -1.01])

# Set the maximum values of the simulation domain
deck.setDomainMax([1.01, 1.01, 1.01])

# Save the simulation deck
deck.save()