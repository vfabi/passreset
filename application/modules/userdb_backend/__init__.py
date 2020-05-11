#!/usr/bin/env python3


class BackendBase:

    def __init__(self, variables=None):
        #TODO: logging object
        #TODO: custom exception hadler inhereted to all backends
        pass

    def check_exists(self, email):
        raise Exception('NotImplementedException')

    def change_password(self, email, password):
        raise Exception('NotImplementedException')
