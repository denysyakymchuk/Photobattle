import datetime
from datetime import datetime as dt

from models import User
from tools import check_time_login


class Session:
    def __init__(self, **cookies):
        self.my_time = str(datetime.datetime.now())[0:19]
        self.cookies = cookies

    def check_time_spam(self):
        if self.cookies["time"]:
            sec = dt.strptime(str(self.my_time), "%Y-%m-%d %H:%M:%S") - dt.strptime(str([self.cookies['time']]), "%Y-%m-%d %H:%M:%S")
            self.cookies['time'] = str(datetime.datetime.now())[0:19]
            if int(str(sec)[5:7]) <= 1000:
                if self.cookies['count'] >= 3:
                    return True
                else:
                    self.cookies['count'] += 1
                    return False
            else:
                return False

        else:
            self.cookies['time'] = str(self.my_time)
            self.cookies['count'] = 0

    def block_user(self):
        user = User.query.filter_by(id=self.cookies['_user_id']).first()
        user.block = 1

        self.cookies['block'] = 1
        self.cookies['time_start_block'] = str(datetime.datetime.now())[0:19]

        return {'message': 'your account was blocked'}

    def unblock_user(self, id):
        user = User.query.filter_by(id=id).first()
        user.block = 0

    def check_session(self, id):
        if 'block' in self.cookies:
            if self.cookies['block'] == 0:
                return False
            else:
                sec = dt.strptime(str(self.my_time), "%Y-%m-%d %H:%M:%S") - dt.strptime(str(self.cookies['time_start_block']), "%Y-%m-%d %H:%M:%S")
                if int(str(sec)[5:7]) >= 30:
                    self.unblock_user(id)
                    self.cookies['time'] = str(self.my_time)
                    self.cookies['count'] = 0
                    return False
                else:
                    return True

        else:
            self.cookies['block'] = 0
            self.cookies['time_start_block'] = 0
            return False

    def login_user(self, id):
        self.cookies['_user_id'] = id
        self.cookies['time_login'] = datetime.datetime.now()

        return True if check_time_login(self.cookies) is True else False

    def check_time_session(self):
        pass


