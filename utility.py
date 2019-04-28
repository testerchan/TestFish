from datetime import datetime
import os

class utility():
    def get_current_time(self):
        return datetime.now().strftime('%Y%m%d_%H%M_%S')

    def get_last_ward_of_url(self, url):
        url = url.rstrip('/')
        words = url.split('/')
        return words[-1]

    def mkdir(self, path):
        os.mkdir(path)
        return path

