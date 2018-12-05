class User:
    # user class
    def __init__(self, id, firstname, lastname, othernames, email,
                 phoneNumber, username, registered, isAdmin, password, password_confirm):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.registered = registered
        self.isAdmin = isAdmin
        self.password = password
        self.password_confirm = password_confirm

    def get_user_details(self):
        # getting one user
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "othernames": self.othernames,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "username": self.username,
            "registered": self.registered,
            "isAdmin": self.isAdmin
        }