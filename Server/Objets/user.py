class User:
    def __init__(self, user_name, client,board = None):
        self.user_name = user_name
        self.client = client
        self.board = board