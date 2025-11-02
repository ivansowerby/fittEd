from enum import Enum
from re import search as re_search

class BackendEnum(str, Enum):
    API_URL = 'http://127.0.0.1:8000'
    def endpoint(_a, b):
        a = _a.value
        return a+b if re_search(r'[/\\]$', a) else a+'/'+b
