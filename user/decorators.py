from django.http import Http404
from functools import wraps

def is_staff_or_in_group(user, *groups):
    return user.is_staff or user.groups.filter(name__in=groups).exists()


# def has_role(user, role_name):
#     if hasattr(user, 'staff_profile'):
#         return user.staff_profile.role == role_name
#     return False

def has_role(user, role_names):
    if hasattr(user, 'staff_profile'):
        return user.staff_profile.role in role_names 
    return False

def is_staff_or_has_role(user, *groups, roles=None):
    return is_staff_or_in_group(user, *groups) or (roles and has_role(user, roles))

