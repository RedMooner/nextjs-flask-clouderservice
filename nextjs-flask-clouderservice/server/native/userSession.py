import crypt


def authenticate(cls, email, password):
    user = cls.query.filter(cls.email == email).one()
    if not crypt.verify(password, user.password):
        raise Exception("No user with this password")
    return user
