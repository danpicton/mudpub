class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Args(Borg):
    def __init__(self, parsed_args=None):
        super(Args, self).__init__()
        if parsed_args is not None:
            self.args = parsed_args
