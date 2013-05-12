class LispError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return self.msg

class LispParseError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return self.msg

def lisp_assert(pred, msg=''):
    if not pred:
        raise LispError(msg)
