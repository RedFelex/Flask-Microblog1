from app import new_app, db
from app.models import User, Post


@new_app.shell_context_processor
def make_shell_context():
    return  {'db':db, 'User' : User, 'Post':Post}
