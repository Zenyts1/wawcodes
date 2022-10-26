import threading


class Events:
    def __init__(self, *args):
        self.funcs = {x: [] for x in args}

    def __call__(self, name):
        def sec(func):
            self.funcs[name].append(func)
            return func

        return sec

    def trigger(self, names, *args, **kwargs):
        if type(names) == str:
            names = [names]
        for name in names:
            for func in self.funcs[name]:
                threading.Thread(target=func, args=args, kwargs=kwargs).start()
