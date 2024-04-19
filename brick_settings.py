from resource_manager import ResourceManger

class BrickSettings():
    _brick_settings ={
        "1" : {
            "texture": 'block_solid',
            "color": (0.8, 0.8, 0.7),
            "is_solid": True
        },
        "2" : {
            "texture": 'block',
            "color": (0.2, 0.6, 1.0),
            "is_solid": False
        },
        "3" : {
            "texture": 'block',
            "color": (0.0, 0.7, 0.0),
            "is_solid": False
        }, 
        "4" : {
            "texture": 'block',
            "color": (0.8, 0.8, 0.4),
            "is_solid": False
        }, 
        "5" : {
            "texture": 'block',
            "color":  (1.0, 0.5, 0.0),
            "is_solid": False
        }, 
        "6" : {
            "texture": 'block',
            "color": (1.0, 0.3, 0.3),
            "powerup": "confuse",
            "is_solid": False
        },
        "7" : {
            "texture": 'block',
            "color": (0.9, 0.25, 0.25),
            "powerup": "chaos",
            "is_solid": False
        },
        "8" : {
            "texture": 'block',
            "color": (0.5, 0.5, 1.0),
            "powerup": "speed",
            "is_solid": False
        },
        "9" : {
            "texture": 'block',
            "color": (1.0, 0.6, 0.4),
            "powerup": "pad-resize",
            "is_solid": False
        }, 
        "10" : {
            "texture": 'block',
            "color": (0.5, 1.0, 0.5),
            "powerup": "pass-through",
            "is_solid": False
        }    
    }

    @classmethod
    def get_texture(cls, number):
        texture_name = cls._brick_settings[str(number)]["texture"]
        return ResourceManger.get_texture(texture_name)

    @classmethod
    def get_color(cls, number):
        return cls._brick_settings[str(number)]['color']
    
    @classmethod
    def get_powerup(cls, number):
        if "powerup" not in cls._brick_settings[str(number)]:
            return None
        return cls._brick_settings[str(number)]["powerup"]
    
    @classmethod
    def is_solid(cls, number):
        if "is_solid" not in cls._brick_settings[str(number)]:
            return False
        return cls._brick_settings[str(number)]["is_solid"]

        

    
