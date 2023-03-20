
class LoggedInUser:

    def __init__(self, u, r, at, rt):
        self.username = u
        self.role = r
        self.accessToken = at
        self.refreshToken = rt

    def updateAccess(self, newAccess, newRefresh):
        self.accessToken = newAccess
        self.refreshToken = newRefresh
