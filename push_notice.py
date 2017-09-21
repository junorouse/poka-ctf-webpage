from db import *
from models import *

x = input()
n = Notice(x)
db_session.add(n)
db_session.commit()