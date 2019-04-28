from datetime import datetime
import os

class utility():
    def get_current_time(self):
        return datetime.now().strftime('%Y%m%d_%H%M_%S')

    def get_last_ward_of_url(self, url):
        url = url.rstrip('/')
        words = url.split('/')
        word = words[-1]
        tmp  = word.split('?')
        return tmp[0]

    def mkdir(self, path):
        os.mkdir(path)
        return path

    def save_file(self, path, message):
        with open(path, mode='w') as f:
            f.write(message)


