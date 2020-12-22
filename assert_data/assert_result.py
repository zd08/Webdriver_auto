from log.Log import info


class Assert:
    '''断言操作'''

    def __init__(self, move_data, result, assert_methodi):
        self.data = move_data
        self.result = result
        dic={'相等':self.assert_equation,
             '不相等':self.assert_not_equation,
             '大于':self.assert_greater,
             '小于':self.assert_less,
             'in':self.assert_in,
             'notin':self.assert_notin,
             }

        dic[assert_methodi]()

    def assert_equation(self):
        assert self.data == self.result

    def assert_greater(self):
        assert int(self.data) > int(self.result)

    def assert_less(self):
        assert int(self.data) < int(self.result)

    def assert_not_equation(self):
        assert self.data != self.result

    def assert_in(self):
        assert self.result in self.data

    def assert_notin(self):
        assert self.result not in self.data
