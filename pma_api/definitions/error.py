class PmaApiError(Exception):
    """PmaApi base exception class."""

    def __init__(self, data=None, msg=None):
        name = 'PmaApiError'
        message = None
        if msg is None:
            message = '{}: An error occured.'.format(name)
        if data:
            message += '\n' if message else None
            message += 'Data: {}'.format(data)
        super(PmaApiError, self).__init__(message)
        self.data = data
