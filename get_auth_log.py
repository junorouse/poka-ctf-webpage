import pytz
import sys
from datetime import datetime

from db import db_session
from models import *


tz = pytz.timezone('Asia/Seoul')

def get(only_solved=False):
	if only_solved:
		auth_logs = AuthLog.query.filter(AuthLog.is_solve == True).order_by(AuthLog.submit_time.asc()).all()
	else:
		auth_logs = AuthLog.query.order_by(AuthLog.submit_time.asc()).all()

	for auth_log in auth_logs:
		st = auth_log.submit_time
		dt = datetime.fromtimestamp(int(st), tz)
		f = "({})[{}] - {} - {} - {}".format(auth_log.chall_id, auth_log.chall_title, auth_log.username, auth_log.submit_flag, dt)
		print(f.encode("utf-8"))


try:
	get(sys.argv[1])
except:
	get()

