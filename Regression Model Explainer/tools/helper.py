class Helper(object):
    @staticmethod
    def is_number(s):
        try:
            float(s) # for int, long, float
        except ValueError:
            return False
        return True
    @staticmethod
    def is_integer(s):
        try:
            int(s) # for int
            if(int(s)<=0):# for positive
                return False
        except ValueError:
            return False
        return True
    @staticmethod
    def getInputFeatureList(inputfeaturelist,outputfeatur):
        templist=[]
        if(inputfeaturelist is None):
            return
        if(outputfeatur is None):
            return
        for i in range(inputfeaturelist.__len__()):
            if(inputfeaturelist[i] != outputfeatur):
                templist.append(inputfeaturelist[i])
        if(templist.__len__() == 0):
            return
        if(inputfeaturelist.__len__()-1 != templist.__len__()):
            return
        return templist
    @staticmethod
    def compareFeatureLists(list_model,list_testdata):
        if(list_model.__len__() != list_testdata.__len__()):
            return False
        for i in range(list_model.__len__()):
            if(list_model[i] != list_testdata[i]):
                return False
        return True  