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
    @staticmethod
    def getFeaturIndex(featurlist,feature):
        if(featurlist is None):
            return
        if(feature == ''):
            return
        for i in range(featurlist.__len__()):
            if(featurlist[i]==feature):
                return i
        return
    @staticmethod
    def getFeatureArray(inputdata,featureindex):
        if(inputdata is None):
            return
        if(featureindex is None):
            return
        featurearray=[]
        for i in range(inputdata.__len__()):
            featurearray.append(inputdata[i][featureindex])
        featurearray=np.array(featurearray)
        featurearray=featurearray.astype(float)
        return featurearray
    @staticmethod
    def getFeatureExplanationData(featurearray,messureddata,predictdata,steps):
        if(featurearray.__len__()!=messureddata.__len__()!=predictdata.__len__()):
            return
        
        fmin=featurearray.min()
        fmax=featurearray.max()
        step=(fmax-fmin)/int(steps)
        steparray=[]
        temp=fmin
        for i in range(int(steps)):
            temp=temp+step
            steparray.append(temp)
        steparray[steparray.__len__()-1]=fmax
        finaldata=[]
        for i in range(steparray.__len__()):
            tempor=[]
            if(i==0):
                for x in range(featurearray.__len__()):
                    if(featurearray[x]<=steparray[i]):
                        temp=[]
                        temp.append(featurearray[x])
                        temp.append(messureddata[x])
                        temp.append(predictdata[x])
                        tempor.append(temp)
            else:
                for x in range(featurearray.__len__()):
                    if(featurearray[x]>steparray[i-1] and featurearray[x]<=steparray[i]):
                        temp=[]
                        temp.append(featurearray[x])
                        temp.append(messureddata[x])
                        temp.append(predictdata[x])
                        tempor.append(temp)
            finaldata.append(tempor)
        results=[]
        for i in range(steparray.__len__()):
            temp=[]
            if(i==0):
                temp.append(str(fmin)+'-'+str(steparray[i]))
            else:
                temp.append(str(steparray[i-1])+'-'+str(steparray[i]))
            temp.append(str(finaldata[i].__len__()))
            if(finaldata[i].__len__()==0):
                temp.append('NA')
                temp.append('NA')
                temp.append('NA')
                temp.append('NA')
            else:
                tm=[]
                tp=[]
                for x in range(finaldata[i].__len__()):
                    t=finaldata[i][x]
                    tm.append(t[1])
                    tp.append(t[2])
                tm=np.array(tm)
                tp=np.array(tp)
                temp.append(str(tm.min())+'-'+str(tm.max()))
                temp.append(str(tp.min())+'-'+str(tp.max()))
                temp.append(str(tm.mean()))
                temp.append(str(tp.mean()))
            results.append(temp)
        print(results)
        for i in range(finaldata.__len__()): #testing if correct
            for x in range(finaldata[i].__len__()):
                print(finaldata[i][x])
            print('_____________________________________________')       
        return results