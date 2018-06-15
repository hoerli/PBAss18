from nntests.topologyTest import TopologyTest
class NnTestService(object):
    @staticmethod
    def topologyTest():
        toptest=TopologyTest()
        return toptest.startTest()