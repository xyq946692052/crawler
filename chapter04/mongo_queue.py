from datetime import datetime,timedelta
from pymongo import MongoClient,errors

class MongoQueue:
    OUTSTANDING,PROCESSING,COMPLETE=range(3)
 
    def __init__(self,client=None,timeout=300):
        self.client=MongoClient() if client is None else client
        self.db=self.client.cache
        self.timeout=timeout

    def __nonzero__(self):
        record=self.db.crawl_queue.find_one(
            {'status':{'$ne':self.COMPLETE}}
        )
        return True if record else False

    def push(self,url):
        """Add new url to queue if does not exist"""
        try:
            self.db.crawl_queue.insert({'_id':url,'status':self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            pass

    def pop(self):
        """Get an outstanding URL from the queue and set its status to processing.if the queue is empty a KeyError exception is raise"""
        record=self.db.crawler_queue.find_and_modify(
            query={'status':self.OUTSTANDING},
            update={'$set':{'status':self.PROCESSING,'timestamp':datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError()

    def peek(self):
        record=self.db.crawl_queue.find_one({'status':self.OUTSTANDING})
        if record:
            return record['_id']
    
    def complete(self,url):
        self.db.crawl_queue.update({'_id':url},{'$set':{'status':self.COMPLETE}})

    def repair(self):
        """Release stalled jobs"""
        record=self.db.crawl_queue.find_and_modify(
            query={
                'timestamp':{'$lt':datetime.now()-timedelta(seconds=self.timeout)},
                'status':{'$ne':self.COMPLETE}
            },
            update={'$set':{'status':self.OUTSTANDING}}
        )
        if record:
            print 'Released',record['_id']

    def clear(self):
        self.db.crawl_queue.drop()
