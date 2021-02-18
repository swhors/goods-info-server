from app.main import db
import datetime

"""
Token Model for storing JWT tokens
"""
class BlacklistToken(db.Model):

    _table_name_='blacklist'
    _col_id_='id'
    _col_userid='token'
    _col_created_='created'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, token):
        self._token_ = token
        self._created_ = datetime.datetime.now()


    def __repr__(self):
        return '<id: token: {}'.format(self._token_)


    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
