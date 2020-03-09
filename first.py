import pybullet as pb
import cv2
import numpy as np
physicsClient = pb.connect(pb.GUI)
from PIL import Image
import pybullet_data
pb.setAdditionalSearchPath(pybullet_data.getDataPath())
import os, glob, random

planeId = pb.loadURDF("plane.urdf")

def pad(num):
    if(num < 10):
        return "00" + str(num)
    elif(num < 100):
        return "0" + str(num)
    else:
        return str(num)

num_objects = random.randint(2,5)
object_multi_ids = [None] * num_objects 
object_forces = [None] * num_objects
object_positions = [None] * num_objects

def check_object_positions(vect):
    for i in range(num_objects):
        if(np.array_equal(vect, object_positions[i])):
            check_object_positions([random.randint(0,2),random.randint(0,2),random.randint(0,2)])
    return vect

#generate random number of objects of any texture and shape
for i in range(num_objects):
    chosen_shape = pad(random.randint(0,999))

    visualShapeId = pb.createVisualShape(
        shapeType=pb.GEOM_MESH,
        fileName='random_urdfs/' + chosen_shape + '/' + chosen_shape + '.obj',
        rgbaColor=None,
        meshScale=[0.1, 0.1, 0.1])

    collisionShapeId = pb.createCollisionShape(
        shapeType=pb.GEOM_MESH,
        fileName='random_urdfs/' + chosen_shape + '/' + chosen_shape + '_coll.obj',
        meshScale=[0.1, 0.1, 0.1])

    object_multi_ids[i] = pb.createMultiBody(
        baseMass=1.0,
        baseCollisionShapeIndex=collisionShapeId, 
        baseVisualShapeIndex=visualShapeId,
        basePosition= check_object_positions([random.randint(0,3),random.randint(0,3),random.randint(0,3)]),
        baseOrientation=pb.getQuaternionFromEuler([0, 0, 0]))


    texture_paths = glob.glob(os.path.join('dtd', '**', '*.jpg'), recursive=True)
    random_texture_path = texture_paths[random.randint(0, len(texture_paths) - 1)]
    textureId = pb.loadTexture(random_texture_path)
    pb.changeVisualShape(object_multi_ids[i], -1, textureUniqueId=textureId)

# pb.setGravity(0, 0, -9.8)
pb.setGravity(0, 0, 0)

viewMatrix = pb.computeViewMatrix(
    cameraEyePosition=[0, 0, 3],
    cameraTargetPosition=[0, 0, 0],
    cameraUpVector=[0, 1, 0])

projectionMatrix = pb.computeProjectionMatrixFOV(
    fov=45.0,
    aspect=1.0,
    nearVal=0.1,
    farVal=3.1)

counter = 0
video = []
video_written = False
# out = cv2.VideoWriter('videos/first/first.avi', 0, 1, (224, 224))
out = cv2.VideoCapture(0)
while(True):
    pb.setRealTimeSimulation(1)
    objectPos, objectOrn = pb.getBasePositionAndOrientation(object_multi_ids[0])
    width, height, rgbImg, depthImg, segImg = pb.getCameraImage(
    width=224, 
    height=224,
    viewMatrix=viewMatrix,
    projectionMatrix=projectionMatrix)
    pb.applyExternalForce(object_multi_ids[0], -1, [0,50,0], [0,0,0], pb.WORLD_FRAME)
    # for i in range(num_objects):
    #     pb.applyExternalForce(object_multi_ids[i], -1, [0,50,0], [0,0,0], pb.WORLD_FRAME)
    
    # rgbImg = np.asarray(rgbImg)
    # rgbImg = Image.fromarray(rgbImg, 'RGBA')
    # video.append(rgbImg)
    # rgbImg = np.asarray(rgbImg)

    # out.write(rgbImg)
    # if(counter > 500 & ~video_written):
    #     out.release()
    #     video_written = True
    #     cv2.destroyAllWindows()
    # rgbImg.save("videos/first/first" + str(counter) + ".png", "PNG")
    
    counter += 1


# make sure to call step simulation