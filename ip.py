import cv2
import spacy
import os
import re
import random
from images import render_order
from images import object_data

nlp = spacy.load("en_core_web_sm")

background_image = cv2.imread("images/jungle.png")

def imgResize(obj, object_images):
    data = object_data[obj]
    image_path = "images/"+data["image_path"]
    
    if os.path.exists(image_path):
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is not None:
            image = cv2.resize(image, data["size"], interpolation=cv2.INTER_AREA)
            object_images[obj] = image
        else:
            print(f"Failed to load image for {obj} from path: {image_path}")
    else:
        print(f"Image not found for {obj} at path: {image_path}")

def place_image(base_image, overlay_image, x, y):
    overlay_height, overlay_width, _ = overlay_image.shape
    roi = base_image[y:y + overlay_height, x:x + overlay_width]

    overlay_image = cv2.resize(overlay_image, (roi.shape[1], roi.shape[0]), interpolation=cv2.INTER_AREA)

    overlay_mask = overlay_image[:, :, 3]
    background_mask = 255 - overlay_mask

    for c in range(0, 3):
        base_image[y:y + overlay_height, x:x + overlay_width, c] = (
            (overlay_mask / 255.0) * overlay_image[:, :, c] +
            (background_mask / 255.0) * roi[:, :, c]
        )

    return base_image

def get_relative_positions(preposition, object1, object2):

    if object2 =="invisible.png" and object1 == "rat.png":
        return  (random.randint(150,200), 350),(190, 400)
    
    if preposition == "above":
        return (0, 0), (0, 200)
    elif preposition == "below":
        return (0, 200), (0, 0)
    elif (preposition == "on") and object1 == "net.png":
        return (150, 320), (190, 360)
    elif (preposition == "in") and object2 == "net.png":
        return (190, 360), (150, 320)
    elif preposition == "on" and object1 == "bird.png"  and object2 == "tree.png":
        return (220, 230), (100, 160)
    elif preposition == "on" or preposition=='in':
        return (200, 350), (190, 360)
    elif preposition == "under":
        return (110, 350), (0, 0)
    else:
        return (110, 350), (0, 0)

def update_scene_from_images(obj1, preposition, obj2, scene, object_images):
    if obj1 not in object_images:
        imgResize(obj1, object_images)
    if obj2 not in object_images:
        imgResize(obj2, object_images)

    position1, position2 = get_relative_positions(preposition, obj1, obj2)
    scene[obj1] = position1
    scene[obj2] = position2

    return scene, object_images

def run(data):
    scene = {}
    object_images = {}

    for item in data:
        obj1, preposition, obj2 = item
        scene, object_images = update_scene_from_images(obj1, preposition, obj2, scene, object_images)

    canvas = cv2.resize(background_image, (500, 500), interpolation=cv2.INTER_AREA)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2BGRA)

    placed_base_characters = {}

    for obj in render_order:
        base_name = obj.split('_')[0]

        if base_name not in placed_base_characters:
            if obj in scene:
                x, y = scene[obj]
                canvas = place_image(canvas, object_images[obj], x, y)
                placed_base_characters[base_name] = obj

    output_image_path = 'server/static/images/composed_image.png'
    cv2.imwrite(output_image_path, canvas)

    print(scene)

# # Example sentences
# data = [#('rat.png', 'on', 'invisible.png'), ('net.png', 'on', 'invisible.png'), ('lion.png', 'on', 'invisible.png')
#         # ('lion2.png', 'in', 'jungle.png'), ('lion2.png', 'under', 'tree.png')
#     ('rat2.png', 'on', 'invisible.png'), ('rat2.png', 'on', 'lion2.png')
#     # ('rat.png', 'on', 'invisible.png'), ('rat.png', 'on', 'lion.png')
#     # ('lion1.png', 'on', 'invisible.png'), ('lion1.png', 'on', 'invisible.png'), ('rat1.png', 'on', 'invisible.png')
#     # ('lion1.png', 'on', 'invisible.png'), ('rat.png', 'on', 'invisible.png')
# # ('lion.png', 'on', 'invisible.png'), ('rat.png', 'on', 'invisible.png')
# # ('rat.png', 'on', 'invisible.png')
#     # ('hunter.png', 'on', 'invisible.png'), ('net.png', 'on', 'lion1.png'), ('lion1.png', 'on', 'invisible.png')
#     # ('rat.png', 'on', 'invisible.png'), ('net.png', 'on', 'invisible.png'), ('lion.png', 'on', 'invisible.png')
#     # ('rat.png', 'on', 'invisible.png'), ('lion.png', 'on', 'invisible.png')
#     # ('rat.png', 'on', 'invisible.png'), ('lion.png', 'on', 'invisible.png'), ('rat.png', 'on', 'invisible.png')
#         ]
# run(data)