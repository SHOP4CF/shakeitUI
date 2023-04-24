
class LoggedInUser:

    def __init__(self):
        self.username = None
        self.role = None
        self.id = None
        self.accessToken = None
        self.refresh_token = None

    def update_info(self, username, role, ID):
        self.username = username
        self.role = role
        self.id = ID

    def update_access(self, new_access, new_refresh):
        self.accessToken = new_access
        self.refresh_token = new_refresh
