from tools.failureTest import FailureTest
class FailureTestService():
    def __init__(self):
        self.ft=FailureTest()
    def getTestData(self,file):
        return self.ft.getTestData(file)