import flask_bcrypt
import datetime
import jwt
from app.model.data.blacklisttoken import BlacklistToken
# from ..config import key


class User:

    _table_name_='user'

    _col_id_='id'
    _col_userid_='userid'
    _col_username_='username'
    _col_email_='email'
    _col_password_='password'
    _col_created_='created'


    @classmethod
    def create_table(cls) -> str:
        return f'create table if not exists {cls._table_name_} ( \n' +\
               f'    {cls._col_id_} integer primary key autoincrement, \n' +\
               f'    {cls._col_userid_} text,  \n' +\
               f'    {cls._col_username_} text,  \n' +\
               f'    {cls._col_email_} text,  \n' +\
               f'    {cls._col_password_} text,  \n' +\
               f'    {cls._col_created_} datetime default current_timestamp);'


    def __init__(self, userid, username=None,
                 email=None, password=None):
        self._userid_ = userid
        self._username_ = username
        self._email_ = email
        self._password_ = password
        self._created_ = datetime.datetime.now()


    @property
    def table_name(self):
        return self._table_name_


    @property
    def col_username(self):
        return self._col_username_


    @property
    def col_userid(self):
        return self._col_userid_


    @property
    def id(self):
        return self._id_


    @id.setter
    def id(self, _id):
        self._id_ = _id


    @property
    def created(self):
        return self._created_


    @created.setter
    def created(self, _created):
        self._created_ = _created


    @property
    def userid(self):
        return self._userid_


    @userid.setter
    def userid(self, userid):
        self._userid_ = userid


    @property
    def username(self):
        return self._username_


    @username.setter
    def username(self, username):
        self._username_ = username


    @property
    def email(self):
        return self._email_


    @email.setter
    def email(self, email):
        self._email_ = email


    @property
    def password(self):
        raise AttributeError('password: write-only field')


    @password.setter
    def password(self, password):
        self._password_ = password
        # flask_bcrypt.generate_password_hash(password).decode('utf-8')


    def __repr__(self):
        r = {
            'userid': self._userid_,
            'username': self._username_,
            'email': self._email_,
            'password': self._password_,
            'created': self._created_,
        }
        return str(r)


    def can_login(self, password):
        return self._password_ == password


    def is_active(self):
        return True


    def get_id(self):
        return self._userid_

    def is_authenticated(self):
        return True


    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self._password_, password)


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'



USERS = {
    "user01": User("user01", password='user_01'),
    "user02": User("user02", password='user_02'),
    "user03": User("user03", password='user_03'),
    "simpson": User("simpson", password='12345678'),
}
