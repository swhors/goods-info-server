# from app.main import db
import datetime
import json

"""
Token Model for storing JWT tokens
"""
class BlacklistTokenResponse:

    len: int
    blacklists: []

    def __init__(self, len: int, blacklists: []):
        self.len = len
        self.blacklists = blacklists


    def __del__(self):
        pass


    def __str__(self):
        return f'len={self.len},' + \
               f'blacklists={self.blacklists}'


    def toJson(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)
