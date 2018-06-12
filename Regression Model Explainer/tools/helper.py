import numpy as np
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
    @staticmethod
    def getDiffList(messuredlist,predictlist):
        if(messuredlist.__len__() != predictlist.__len__()):
            return
        resultlist=[]
        for i in range(messuredlist.__len__()):
            try:
                r=float(predictlist[i])-float(messuredlist[i])
                resultlist.append(str(r))
            except:
                return
        resultlist=np.array(resultlist)
        return resultlist
    @staticmethod
    def transformPredictiontoArray(prediction):
        if(prediction is None):
            return
        predictionarr=[]
        for i in range(prediction.__len__()):
            predictionarr.append(str(prediction[i][0]))
        predictionarr=np.array(predictionarr)
        return predictionarr
    @staticmethod
    def getPositiveDifference(difflist):
        if(difflist is None):
            return
        try:
            temp=np.array(difflist)
            temp=temp.astype(float)
        except:
            return
        posdifflist=[]
        for i in range(temp.__len__()):
            if(temp[i]>=0):
                posdifflist.append(temp[i])
        posdifflist=np.array(posdifflist)
        return posdifflist
    @staticmethod
    def getNegativeDifference(difflist):
        if(difflist is None):
            return
        try:
            temp=np.array(difflist)
            temp=temp.astype(float)
        except:
            return
        negdifflist=[]
        for i in range(temp.__len__()):
            if(temp[i]<0):
                negdifflist.append(abs(temp[i]))
        negdifflist=np.array(negdifflist)        
        return negdifflist
    @staticmethod
    def getPosAndNegDiffList(difflist):
        if(difflist is None):
            return
        try:
            resultlist=np.array(difflist)
            resultlist=resultlist.astype(float)
            resultlist=abs(resultlist)
        except:
            return
        return resultlist
    @staticmethod
    def getMeans(positiv,negativ,full):
        if(positiv is None):
            return
        if(negativ is None):
            return
        if(full is None):
            return
        means=[]
        if(positiv.__len__()==0):
            means.append(0)
        else:
            means.append(positiv.mean())
        if(negativ.__len__()==0):
            means.append(0)
        else:
            means.append(negativ.mean())
        if(full.__len__()==0):
            means.append(0)
        else:
            means.append(full.mean())
        means=np.array(means)
        return means