import base64

print("here i am")
DEBUG = True


def debug(log=True, dyna=False):
    def waa(dyna, log, fu, *args):
        if log:
            with open(
                f"logs{'_'+base64.b64encode(fu.__qualname__.encode()).decode() if dyna else ''}.txt",
                "a",
            ) as f:
                f.write(
                    " ".join(args).replace("\n", "\\n").replace("\t", "\\t") + "\n\n"
                )
        else:
            print(*args)

    class debug_s:
        last_out = None

        def __init__(self, func):
            print("here i will debug, thank you", func)
            self.base_func = func
            self.__qualname__ = func.__qualname__
            self.__name__ = func.__name__

        def __call__(self, *args, l=locals, **kwargs):
            print("here i am called by", self.base_func)
            if DEBUG:
                waa(
                    self.dyna,
                    self.log,
                    self.base_func,
                    "-->",
                    self.base_func.__qualname__,
                    ":",
                    repr(args),
                    repr(kwargs),
                )
            self.last_out = self.base_func(*args, **kwargs)
            if DEBUG:
                waa(
                    self.dyna,
                    self.log,
                    self.base_func,
                    "<--",
                    self.base_func.__qualname__,
                    ":",
                    repr(self.last_out),
                )
            return self.last_out

    debug_s.log, debug_s.dyna = log, dyna
    return debug_s
