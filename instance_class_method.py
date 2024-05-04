'''Defines a decorator class for a method that uses both the class and instance as variables'''

import functools

class InstanceClassMethod:
    '''Decorator class for a method
    To use the instance and class as the first and second argument in its signature'''

    def __init__(self, func):
        '''Initializer, func is the function to be wrapped'''
        self.func = func

    def __get__(self, obj, obj_type=None):
        '''obj is the instance and obj_type is the class'''

        if obj_type is None:
            obj_type = type(obj)

        @functools.wraps(self.func)
        def new_func(*args, **kwargs):
            '''Replacement function'''
            return self.func(obj, obj_type, *args, **kwargs)

        return new_func
