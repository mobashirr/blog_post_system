
'''
redis client class
'''

import redis


class Redis_client():
    
    def __init__(self):
        try:
            self.__redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
            print('connected to redis.');
        except redis.ConnectionError:
            print('redis connection went wrong.');
    
    def isAlive(self):
        connection_state = False;
        try:
            # Test connection using ping
            if self.__redis_client.ping():
                connection_state=  True;
        except redis.ConnectionError:
            pass
        return connection_state;

    def set_key_val(self, key, val, duration=7200):
        '''
        set token for given amout of time
        ex is in seconds (means it will expire aftet 2h (7200s))
        '''
        return self.__redis_client.set(key,val, ex=duration);

    def get_value(self,key):
        return self.__redis_client.get(key);