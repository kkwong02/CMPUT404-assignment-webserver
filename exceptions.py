class NotFoundError(Exception):
    pass


class MovedPermanentlyError(Exception):
    def __init__(self, location, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.location = location
