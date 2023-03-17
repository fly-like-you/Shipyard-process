import copy

class CustomDeepCopy:
    def __init__(self, data):
        self.data = data

    def custom_deep_copy(self, obj):
        if isinstance(obj, list):
            return [self.custom_deep_copy(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.custom_deep_copy(value) for key, value in obj.items()}
        elif isinstance(obj, tuple):
            return tuple(self.custom_deep_copy(item) for item in obj)
        elif hasattr(obj, '__dict__'):
            obj_copy = copy.copy(obj)
            for key, value in obj.__dict__.items():
                setattr(obj_copy, key, self.custom_deep_copy(value))
            return obj_copy
        else:
            return obj

    def get_deep_copy(self):
        return self.custom_deep_copy(self.data)


