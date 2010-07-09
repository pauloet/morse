"""
This module implement a "semantic camera" sensor for the OpenRobots Simulator.

This special camera returns the list of objects as seen by the robot's cameras,
with unique id, possibly (if set in the objects' properties) the type of object
and the colour of the object.

Other such high-level information (the semantic description of the scene) can be
added.

Version: 1.0
Date: 16 Nov. 2009
Author: Severin Lemaignan <severin.lemaignan@laas.fr>

Copyright LAAS-CNRS 2009
"""

import GameLogic

import Blender
#import bpy.types
# Import the ontology server proxy
#import oro

import morse.helpers.sensor
import morse.helpers.colors

class MorseSemanticCameraClass(morse.helpers.sensor.MorseSensorClass):


	def __init__(self, obj, parent=None):
		""" Constructor method.

		Receives the reference to the Blender object.
		The second parameter should be the name of the object's parent.
		"""
		print ("######## SEMANTIC CAMERA '%s' INITIALIZING ########" % obj.name)
		# Call the constructor of the parent class
		super(self.__class__,self).__init__(obj, parent)

		# TrackedObject is a dictionary containing the list of tracked objects 
		# (->meshes with a class property set up) as keys
		#  and the bounding boxes of these objects as value.
		if not hasattr(GameLogic, 'trackedObjects'):
			print ('  ### Initialization of trackedObjects variable...')
			scene = GameLogic.getCurrentScene()
			GameLogic.trackedObjects = dict.fromkeys([ obj for obj in scene.objects if obj.getPropertyNames().count('objClass')!=0 ])
			
			# Store the bounding box of the marked objects
			################## WARNING ################## 
			# NOTE: This uses the Blender library, which has been removed
			#  in Blender 2.5. Thus this will likely break with the new version.
			for obj in GameLogic.trackedObjects.keys():
				# GetBoundBox(0) returns the bounding box in local space
				#  instead of world space.
				#GameLogic.trackedObjects[obj] = bpy.types.Object(obj).bound_box
				GameLogic.trackedObjects[obj] = Blender.Object.Get(obj.name[2:]).getBoundBox(0)
				print ('	- {0}'.format(obj.name))


		# Prepare the exportable data of this sensor
		# In this case, it is the list of currently visible objects by each independent robot.
		self.local_data['visible_objects'] = []
		self.data_keys = ['visible_objects']

		# Initialise the copy of the data
		for variable in self.data_keys:
			self.modified_data.append(self.local_data[variable])

		# Variable to indicate this is a camera
		self.semantic_tag = True

		print ('######## SEMANTIC CAMERA INITIALIZED ########')


    def default_action(self):
		""" Do the actual semantic 'grab'.

		Iterate over all the tracked objects, and check if they are visible for the robot.
		"""
		camera = self.blender_obj
		visibles = self.local_data['visible_objects']

		# Grab an image from the texture
        if self.blender_obj['capturing']:

			for obj in GameLogic.trackedObjects:
				visible = self._check_visible(obj, camera)

				# If the object is visible and not yet in the visible_objects list...
				if visible and visibles.count(obj) == 0:
					self.local_data['visible_objects'].append(obj)
					print ("Semantic: {0}, ({1}, {2}) just appeared".format(obj.name, obj['objClass'], morse.helpers.Colors.retrieveHue(obj)))

				# If the object is not visible and was in the visible_objects list...
				if not visible and visibles.count(obj) != 0:
					self.local_data['visible_objects'].remove(obj)
					print ("Semantic: {0}, ({1}) just disappeared".format(obj.name, obj['objClass']))
				

				
	def _check_visible(obj, camera):
		""" Check if an object lies inside of the camera frustrum. """
		# TrackedObjects was filled at initialization
		#  with the object's bounding boxes
		bb = GameLogic.trackedObjects[obj]
		pos = obj.position
		
		#print ("\n--- NEW TEST ---")
		#print ("OBJECT {0} AT {1}".format(obj, pos))
		#print ("BBOX: >{0}<".format([[bb_corner[i] + pos[i] for i in range(3)] for bb_corner in bb]))
		#print ("BBOX: {0}".format(bb))

		# Translate the bounding box to the current object position
		#  and check if it is in the frustrum
		if camera.boxInsideFrustum([[bb_corner[i] + pos[i] for i in range(3)] for bb_corner in bb]) != camera.OUTSIDE:
			# object is inside
			return True

		return False
