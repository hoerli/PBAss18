from explanation.failureTest import FailureTest
class ExplanationService(object):
    @staticmethod
    def failureTest(file):
        ft=FailureTest(file)
        return ft.getTestData()