
class Node:
    def __init__(self, **kwarg):
        self.kind = 'Node'
        self.edges = []
        self.nodeid = 0
        self._distance = 0
        for key, value in kwarg.items():
            setattr(self, key, value)
    @classmethod
    def make_one(cls, df):
        lst = df.to_dict('records')
        return cls(**lst[0])
    @classmethod
    def make_list(cls, df):
        lst = df.to_dict('records')
        return [cls(**dct) for dct in lst]
    def __str__(self):
        return f"Node {self.nodeid}"

class Vraag(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'Vraag'
    def __str__(self):
        return f"{self.STELLING} ({self.VRAAGID}) vervallen={self.VERVALLEN}"

class Lijst(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'Lijst'
        self.children = []
    def __str__(self):
        return f"{self.LIJSTNAAM} ({self.LIJSTID}) vervallen={self.VERVALLEN}"
