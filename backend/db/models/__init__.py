from manage import init_django

init_django()

from .user import User, Employee, Admin
from .group import Group, Locations
