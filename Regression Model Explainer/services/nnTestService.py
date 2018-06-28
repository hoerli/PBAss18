from nntests.topologyTest import TopologyTest
from nntests.performanceTest import PerformanceTest
class NnTestService(object):
    ''' offers two static methods to run the Neural Network test
    should work as interface between the client(gui) and the backends
    '''
    @staticmethod
    def topologyTest():
        ''' method to run MSE test
        train data must set in ModelData singleton
        returns the MSEs
        '''
        toptest=TopologyTest()
        return toptest.startTest()
    @staticmethod
    def performanceTest():
        ''' method to run Perfomance
        train data must set in ModelData singleton
        returns the history
        '''
        pertest=PerformanceTest()
        return pertest.startTest()