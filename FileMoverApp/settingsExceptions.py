class SettingsException(Exception):
    def __init__(self, *args):
        if len(args) == 1:
            self.message = args[0]
        elif len(args) == 2:
            self.message = "{0} at line {1}".format(args[0], args[1])
        else:
            self.message = none

    def __str__(self):
        if self.message:
            return 'Problem in settings file: {0}'.format(self.message)
        else:
            return 'Unknown problem in settings file'
