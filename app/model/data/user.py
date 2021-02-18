from .. import db, flask_bcrypt
import datetime
from app.model.data.blacklisttoken import BlacklistToken
from ..config import key
import jwt


class User:

    _table_name_='user'
    _col_id_='id'
    _col_userid='userid'
    _col_username='username'
    _col_email_='email'
    _col_password_='password'
    _col_created_='created'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100))
    created = db.Column(db.DateTime, nullable=False)


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


    @property
    def password(self):
        raise AttributeError('password: write-only field')


    @password.setter
    def password(self, password):
        self._password_ = password flask_bcrypt.generate_password_hash(password).decode('utf-8')


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
