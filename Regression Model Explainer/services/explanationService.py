from explanation.failureTest import FailureTest
from explanation.overallExplanation import overallExplanation
from explanation.singleinstancelime import SingleInstanceLime
from explanation.featureExplanation import FeatureExplanation
class ExplanationService(object):
    ''' offers four static methods to run the explanation test
    should work as interface between the client(gui) and the backends
    '''
    @staticmethod
    def failureTest(file):
        ''' method for the failure test
        needs a filepath whos data fits to the trained model
        returns the data for this test
        '''
        ft=FailureTest(file)
        return ft.getTestData()
    @staticmethod
    def overallExplanation(file):
        ''' method for the overall explanation test
        needs a filepath whos data fits to the trained model
        returns the data for this test
        '''
        oe=overallExplanation(file)
        return oe.getTestData()
    @staticmethod
    def limeExplanation(inp):
        ''' method for the lime test for a single instance
        needs one input tuple of the data who fits to the model(one data tuple for prediction)
        returns a figure who shows the result of this test
        '''
        le=SingleInstanceLime(inp)
        return le.getFigure()
    @staticmethod
    def getInputTuples(file):
        le=SingleInstanceLime(None)
        return le.getInputTuples(file)
    @staticmethod
    def featureExplanation(file,feature,steps):
        ''' method for the feature explanation test
        needs a file path from test data who fits to the trained model
        needs a feature which gets test who fits to the trained model features
        and needs steps in which the tests get splitted
        return the data for this test
        '''
        fe=FeatureExplanation(file,feature,steps)
        return fe.getFeatureExplanationData()