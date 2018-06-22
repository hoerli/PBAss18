from nntests.topologyTest import TopologyTest
from nntests.performanceTest import PerformanceTest
class NnTestService(object):
    @staticmethod
    def topologyTest():
        toptest=TopologyTest()
        return toptest.startTest()
    @staticmethod
    def performanceTest():
        pertest=PerformanceTest()
        return pertest.startTest()