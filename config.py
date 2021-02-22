class RedisConf:
    host="192.168.4.200"
    port=6379
    use_auth=1
    password='danal1004!'


class Config:
    jwt_key='dkakehzl'


class DBConfig:
    db_name='goods.db'


if __name__=="__main__":
    print("conf", redis_conf)
