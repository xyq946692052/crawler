import os
import re
import urlparse
import shutil
import zlib
from datetime import datetime,timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle
from link_crawler import link_crawler

class DiskCache:
    def __init__(self,cache_dir='cache',expires=timedelta(days=30),compress=True):
        self.cache_dir=cache_dir
        self.expires=expires
        self.compress=compress

    def __getitem__(self,url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path,'rb') as fp:
                data = fp.read()
                if self.compress:
                    data=zlib.decompress(data)
                result,timestamp=pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url+' has expire')
                return result
        else:
            raise KeyError(url+' does not exist')

    
    def __setitem__(self,url,result):
        """save data to disk for this url"""
        path=self.url_to_path(url)
        folder=os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data=pickle.dumps((result,datetime.utcnow()))
        if self.compress:
            data=zlib.compress(data)
        with open(path,'wb') as fp:
            fp.write(data)

    
    def __delitem__(self,url):
        """ remove the value at this key and any empty parent sub-directories"""
        path=self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.diename(path))
        except OSError:
            pass


    def url_to_path(self,url):
        """create file system path for this URL"""
        components=urlparse.urlsplit(url)
        path=components.path
        if not path:
            path='/index.html'
        elif path.endswith('/'):
            path+='index.html'
        filename=components.netloc+path+components.query
        filename=re.sub('[^/0-9a-zA-Z\-.,;_]','_',filename)
        filename='/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir,filename)

 
    def has_expired(self,timestamp):
        """return whether this timestamp has expired"""
        return datetime.utcnow()>timestamp+self.expires

   
    def clear(self):
        """Remove all the cache values"""
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

if __name__=='__main__':
    link_crawler('http://example.webscraping.com/','/(index|view)',cache=DiskCache())   
    
        
