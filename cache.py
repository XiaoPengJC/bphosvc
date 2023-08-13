from errno import EEXIST
from os import makedirs, path, listdir

class Cache:
    def __init__(self) -> None:
        self.cache = {}
        self.make_cache_dir()

    def make_cache_dir(self):
        try:
            makedirs('cache')
        except OSError as exc:
            if exc.errno == EEXIST and path.isdir('cache'):
                pass
            else: raise

    # register all filenames in the cache folder
    def register_cache(self):
        for filename in listdir('cache'):
            self.cache[filename] = True
        print("Cache registered...")
        print(self.cache)
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value