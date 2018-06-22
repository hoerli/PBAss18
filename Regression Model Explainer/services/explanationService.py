from explanation.failureTest import FailureTest
from explanation.overallExplanation import overallExplanation
from explanation.singleinstancelime import SingleInstanceLime
from explanation.featureExplanation import FeatureExplanation
class ExplanationService(object):
    @staticmethod
    def failureTest(file):
        ft=FailureTest(file)
        return ft.getTestData()
    @staticmethod
    def overallExplanation(file):
        oe=overallExplanation(file)
        return oe.getTestData()
    @staticmethod
    def limeExplanation(inp):
        le=SingleInstanceLime(inp)
        return le.getFigure()
    @staticmethod
    def featureExplanation(file,feature,steps):
        fe=FeatureExplanation(file,feature,steps)
        return fe.getFeatureExplanationData()