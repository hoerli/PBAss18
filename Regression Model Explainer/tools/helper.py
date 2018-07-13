import numpy as np
class Helper(object):
    ''' this class has different helper methods for the application
    methods are all static methods (no object needed)
    '''
    @staticmethod
    def is_number(s):
        ''' returns true or false
        test if the s is a number
        '''
        try:
            float(s) # for int, long, float
        except ValueError:
            return False
        return True
    @staticmethod
    def is_integer(s):
        ''' returns true or false
        test if the s is positiv Integer number
        '''
        try:
            int(s) # for int
            if(int(s)<=0):# for positive
                return False
        except ValueError:
            return False
        return True
    @staticmethod
    def getInputFeatureList(inputfeaturelist,outputfeatur):
        ''' returns a list of features except the outputfeatur
        '''
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
        ''' returns true or false
        test if the model input features are the same (also same sequence) as the test data features
        '''
        if(list_model.__len__() != list_testdata.__len__()):
            return False
        for i in range(list_model.__len__()):
            if(list_model[i] != list_testdata[i]):
                return False
        return True
    @staticmethod
    def getDiffList(messuredlist,predictlist):
        ''' returns a list with differences between two list of data (numbers)
        first must be messured data second predict data
        '''
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
        ''' returns 2 dim array of prediction to 1 dim array (keras predictions always returns a two dimensional array)
        '''
        if(prediction is None):
            return
        predictionarr=[]
        for i in range(prediction.__len__()):
            predictionarr.append(str(prediction[i][0]))
        predictionarr=np.array(predictionarr)
        return predictionarr
    @staticmethod
    def getPositiveDifference(difflist):
        ''' returns array of all positive numbers of this list
        '''
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
        ''' returns array of all negative numbers of this list (change to positiv)
        '''
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
        ''' returns array of all numbers of this this list (change negativ numbers to positiv)
        '''
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
        ''' return the menas of 3 list of numbers
        '''
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
        ''' returns the index of a feature from a feature list
        '''
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
        ''' returns an array of of the data where the featureindex is is
        needs array of inputdata
        '''
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
        ''' returns result for feature explanation test
        needs array of features who gets explained
        needs the messured data (array)
        needs the predictdata (array)
        needs steps in wich the feature gets splited
        used by FeatureExplanation
        '''
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
        '''
        print(results)
        for i in range(finaldata.__len__()): #testing if correct
            for x in range(finaldata[i].__len__()):
                print(finaldata[i][x])
            print('_____________________________________________')
        '''    
        return results
    @staticmethod
    def getFeatureExplanationLabels(ran,numresult):
        label=[]
        for i in range(ran.__len__()):
            temp=ran[i].split('-')
            temp=np.array(temp).astype(float)
            temp[0]=temp[0].round(2)
            temp[1]=temp[1].round(2)
            l='Range: '+str(temp[0])+'-'+str(temp[1])+'\nTuples: '+str(numresult[i])
            label.append(l)
        return label
    @staticmethod
    def tranformDataForFeatureGraph(data):
        data=data
        ran=[]
        numresult=[]
        mesuredmins=[]
        mesuredmax=[]
        predictmin=[]
        predictmax=[]
        mesured=[]
        predict=[]
        
        for i in range(data.__len__()):
            ran.append(data[i][0])
            numresult.append(data[i][1])
            if(int(data[i][1])!=0):
                temp=[]
                temp=data[i][2].split('-')
                mesuredmins.append(temp[0])
                mesuredmax.append(temp[1])
                temp=data[i][3].split('-')
                predictmin.append(temp[0])
                predictmax.append(temp[1])
                mesured.append(data[i][4])
                predict.append(data[i][5])
            else:
                mesuredmins.append('0')
                mesuredmax.append('0')
                predictmin.append('0')
                predictmax.append('0')
                mesured.append('0')
                predict.append('0')
        mesuredmins=np.array(mesuredmins).astype(float)
        mesuredmax=np.array(mesuredmax).astype(float)
        predictmin=np.array(predictmin).astype(float)
        predictmax=np.array(predictmax).astype(float)
        mesured=np.array(mesured).astype(float)
        predict=np.array(predict).astype(float)
        result=[]
        result.append(ran)
        result.append(numresult)
        result.append(mesuredmins)
        result.append(mesuredmax)
        result.append(predictmin)
        result.append(predictmax)
        result.append(mesured)
        result.append(predict)
        return result
    @staticmethod
    def transformDataForLime(data):
        labels=[]
        values=[]
        result=[]
        for i in range(data.__len__()):
            labels.append(data[i][0])
            values.append(data[i][1])
        result.append(labels)
        result.append(values)
        return result
    @staticmethod
    def sortFeaturesForLime(features,inpu,expla):
        resultfeat=[]
        resultinpu=[]
        for i in range(expla.__len__()):
            for x in range(features.__len__()):
                if(expla[i].__contains__(features[x])):
                    resultfeat.append(features[x])
                    resultinpu.append(inpu[x])
        resultfeat=np.array(resultfeat)
        resultinpu=np.array(resultinpu)
        result=[]
        result.append(resultfeat)
        result.append(resultinpu)
        return result