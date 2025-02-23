import json
import os


class Config:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        self.config_path = 'config.json'
        self.defaults = {
            'locale': 'en',
            'theme': 'system',
            'last_position': (None, None)
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.data = json.load(f)
            else:
                self.data = self.defaults.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.data = self.defaults.copy()

    def save(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def __getitem__(self, key):
        return self.data.get(key, self.defaults.get(key))

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()