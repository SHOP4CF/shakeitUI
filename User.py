
class LoggedInUser:

    def __init__(self):
        self.username = None
        self.role = None
        self.id = None
        self.accessToken = None
        self.refreshToken = None

    def updateInfo(self, username, role, ID):
        self.username = username
        self.role = role
        self.id = ID

    def updateAccess(self, newAccess, newRefresh):
        self.accessToken = newAccess
        self.refreshToken = newRefresh
