import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class StorageService:
    @staticmethod
    def _get_path(filename):
        return os.path.join(DATA_DIR, filename)

    @classmethod
    def read(cls, filename):
        path = cls._get_path(filename)
        if not os.path.exists(path):
            return []
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @classmethod
    def write(cls, filename, data):
        path = cls._get_path(filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def find_user(cls, username):
        users = cls.read('users.json')
        for user in users:
            if user['username'] == username:
                return user
        return None

    @classmethod
    def save_user(cls, user_data):
        users = cls.read('users.json')
        users.append(user_data)
        cls.write('users.json', users)

    @classmethod
    def save_token(cls, token_data):
        tokens = cls.read('tokens.json')
        tokens.append(token_data)
        cls.write('tokens.json', tokens)

    @classmethod
    def validate_token(cls, token):
        tokens = cls.read('tokens.json')
        for t in tokens:
            if t['token'] == token:
                return t['username']
        return None

    @classmethod
    def save_widget(cls, widget_data):
        widgets = cls.read('widgets.json')
        widget_data['id'] = len(widgets) + 1
        widgets.append(widget_data)
        cls.write('widgets.json', widgets)
        return widget_data
