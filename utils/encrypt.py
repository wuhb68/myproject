import hashlib
from myproject import settings


def md5(data):
    salt = settings.SECRET_KEY
    return hashlib.md5(salt.encode('utf-8') + data.encode('utf-8')).hexdigest()