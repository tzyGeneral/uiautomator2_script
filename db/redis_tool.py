import redis
from config import Config


pool = redis.ConnectionPool(host=Config.REDIS["host"], port=Config.REDIS["port"], db=Config.REDIS["db"],
                            password=Config.REDIS["passwd"])


class RedisQueue:
    """将redis作为存储队列使用"""

    def __init__(self, name):
        self.__db = redis.Redis(connection_pool=pool)
        self.key = '%s' % (name,)

    def getKeys(self):
        """
        获取所有的key
        :return:
        """
        return self.__db.keys(pattern='result_*')

    def qsize(self):
        return self.__db.llen(self.key)

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get_wait(self, timeout=30):
        item = self.__db.blpop(self.key, timeout=timeout)
        return item

    def get_nowait(self):
        item = self.__db.lpop(self.key)
        return item

    def putList(self, l):
        for item in l:
            self.__db.rpush(self.key, item)

    def getQueueList(self):
        return self.__db.lrange(self.key, 0, -1)


if __name__ == '__main__':
    import json

    RedisQueue(name="user_passwd").put(json.dumps({"phone": "", "passwd": ""}))