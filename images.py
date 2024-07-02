image_data = [
    {"character": "lion", "tags": [], "image_path": "lion.png"},
    {"character": "lion", "tags": ["sleeping", "resting", "dozing", "nap", "napping"], "image_path": "lion2.png"},
    {"character": "lion", "tags": ["angry", "upset", "furious","roaring"], "image_path": "lion1.png"},
    {"character": "rat", "tags": ["jumping", "hopping", "leaping","playing"], "image_path": "rat2.png"},
    {"character": "rat", "tags": ["Scared","Afraid","Terrified","Petrified","Frightened","Panicked","Anxious","Nervous","Worried","Apprehensive","Alarmed"], "image_path": "rat1.png"},
    {"character": "rat", "tags": [], "image_path": "rat.png"},
    {"character": "net", "tags": [], "image_path": "net.png"},
    {"character": "tree", "tags": [], "image_path": "tree.png"},
    {"character": "bird", "tags": [], "image_path": "bird.png"},
    {"character": "invisible", "tags": [], "image_path": "invisible.png"},
    {"character": "hunter", "tags": [], "image_path": "hunter.png"},
    {"character": "jungle", "tags": [], "image_path": "jungle.png"},
    {"character": "lion","tags":["happily","joyfully","friends"],"image_path":"lion3.png"}
]

object_data = {
    "lion2.png": {"image_path": "lion2.png", "size": (140, 140)},
    "lion3.png":{"image_path":"lion3.png","size":(140,140)},
    "lion.png": {"image_path": "lion.png", "size": (140, 140)},
    "lion1.png": {"image_path": "lion1.png", "size": (140, 140)},
    "net.png": {"image_path": "net.png", "size": (180, 180)},
    "stone.png": {"image_path": "stone.png", "size": (140, 140)},
    "rat2.png": {"image_path": "rat2.png", "size": (50, 50)},
    "rat1.png": {"image_path": "rat1.png", "size": (50, 50)},
    "tree.png": {"image_path": "tree.png", "size": (300, 800)},
    "rat.png": {"image_path": "rat.png", "size": (50, 50)},
    "bird.png": {"image_path": "bird.png", "size": (40, 40)},
    "hunter.png": {"image_path": "hunter.png", "size": (200, 400)},
    "invisible.png": {"image_path": "invisible.png", "size": (1, 1)},
    "jungle.png":{"image_path": "jungle.png", "size": (1, 1)}
    # Add more objects and sizes as needed
}

render_order = ["invisible.png","tree.png","stone.png","lion3.png","lion.png","lion2.png","lion1.png","net.png","rat1.png","rat2.png","rat.png","bird.png","hunter.png",]