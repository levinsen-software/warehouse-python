import requests
import os
import shutil

class WHFile():
    def __init__(self, wh, id):
        self.wh = wh
        self.id = id
    
    def __str__(self):
        return 'WHFile(id=%s)' % self.id

    def getProperties(self):
        with requests.get('%s/files/%s' % (self.wh.url, self.id), auth=self.wh.auth) as r:
            return r.json()
    
    def download(self, path=None, createDirs=False):
        with requests.get('%s/files/%s/download' % (self.wh.url, self.id), auth=self.wh.auth, stream=True) as r:
            r.raise_for_status()
            filename = r.headers['x-content-filename']

            if path is not None:
                basename = os.path.basename(path)
                if not basename:
                    filename = os.path.join(os.path.dirname(path), filename)
                else:
                    filename = path
                
                if createDirs:
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

            print("Downloading file as %s" % filename)
            with open(filename + '.part', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            shutil.move(filename + '.part', filename)
            return filename