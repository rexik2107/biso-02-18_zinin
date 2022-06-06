command_list = []


class Command:
    def __init__(self):
        self.__keys = []
        self.topics_blocks = []
        self.topics_resolution = []
        self.description = ''
        self.condition = True
        command_list.append(self)
        self.definitions = {}

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def __call__(self, for_definition, methods=None):
        if methods is None:
            methods = ["POST", "GET"]

        def decorator(func):
            self.definitions[(for_definition, func)] = [func, methods]
            print("DECORATOR", self.definitions)
            return func

        return decorator


