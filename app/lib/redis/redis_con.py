import redis
import sys

from config import redis_conf as rcf

class redis_con:
    def __init__(self):
        if rcf.use_auth == 1:
            self.conn = redis.StrictRedis(host=rcf.host, port = rcf.port, db=0, password=rcf.password)
        else
            self.conn = redis.StrictRedis(host=rcf.host, port = rcf.port, db=0)

    def __del__(self):
        print('destroy redis_con')
        self.conn.close()

    def get_favorite(self):
        pass

    def set_category_count(self, catetory: str):
        self.conn.hincrby(0, category)

    get get_categories(self):


if __name__=="__main__":
    print(sys.path)
    print(rcf.host)
