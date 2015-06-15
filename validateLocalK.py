#encoding:utf-8
'''
列表排序
用字典会不会好一点？
二分类问题
训练数据大于100条（kmax=100）

'''

import math
from KnnSearch import KdTreeFindNearest
import genkdTree



class ValiLocalK:
    
    def __init__(self,testDataPath,trainDataPath,categorys):
        self.testDataPath=testDataPath
        self.trainDataPath=trainDataPath
        self.categorys=categorys
        
    def readTrainData(self):
        dataFile=open(self.trainDataPath)
        dataList=[]
        for line in dataFile.readlines():
            cellData=[]
            l=line.split(",")
            for i  in range(len(l)-1):
                cellData.append(float(l[i]))
            l[-1].replace('\r\n','')
            cellData.append(l[-1])
            
            dataList.append(cellData)
        return dataList[:-26]     
       
    def readTestData(self):
        dataFile=open(self.testDataPath)
        dataList=[]
        for line in dataFile.readlines():
            cellData=[]
            line.replace('\r\n','')
            l=line.split(",")
            for i  in range(len(l)-1):
                cellData.append(float(l[i]))
            cellData.append(l[-1])
            dataList.append(cellData)
        return dataList[-26:]
    
        
    def sortDistance(self,list,target):
        trainList=[]
        for node in list:  
            d=0    
            celdata=[]      
            for i in range(len(node)-1):#the last attribute is classify
                d+=(node[i]-target[i])**2
                
            celdata=node[:]
            celdata.append(math.sqrt(d))
            trainList.append(celdata)
            
        trainList=sorted(trainList, key=lambda node: node[-1])   
        return trainList

    def classifyInstance(self,sortedList,k,target):
        one=0
        two=0
        category=0
        for i in range(k):
            if sortedList[i][-2]==self.categorys[0]:
                one+=1
            else:
                two+=1  
                
        if one>two:
            category=self.categorys[0]
        else:
            category=self.categorys[1]
            
        if category==target[-1]:
            return 'Y'
        else:
            return 'N'
        
    def divData(self,data):
        #divide the data into 10 parts:10-fold cross validation
        dt_len=len(data)
        if dt_len==0 or dt_len<10:
            return []
        else :
            j=dt_len/10
            k=dt_len%10
            
            CellList=[]
            for i in xrange(0,9*j,j):
                CellList.append(data[i:i+j])
            CellList.append(data[9*j:])
            
        return CellList,j
        
    def GlobalAccTraining(self,k):
        data=self.readTrainData() 
        cellList,dt_len=self.divData(data)
        
        AccSum=0
        for i in range(10):
            testdata=cellList[i]
            traindata=[]
            for j in range(10):
                if j!=i:
                    traindata.extend(cellList[j])
             
            correct=0        
            for target in testdata:
                sortedList=self.sortDistance(traindata, target)
#                 print sortedList
                classify=self.classifyInstance(sortedList, k, target)
                if classify=='Y':
                    correct=correct+1
                    
            AccSum=AccSum+correct/float(dt_len)
            
        return AccSum/10.00000
                    
    def AccGlobalk(self):
        #comput the accuracy of global k
        AccGlobal=[]
        for k in range(1,101):
            globalk=self.GlobalAccTraining(k)
#             print globalk
            AccGlobal.append(globalk)
         
        AccGlobalK=open('AccGlobalK.txt','w')
        for line in AccGlobal:
            AccGlobalK.writelines(str(line)+'\n') 
        return AccGlobal 
 #---------------------------------------------------------------------
 
     
    def nearNerb(self,datalist):
        #find 3 nearest neighbors of each node   
        tempList=[]
        nearList=[]#((target,1nn,2nn,3nn);(target,1nn,2nn,3nn)...)
        for i in range(len(datalist)):
            tempList=datalist[:]
            del tempList[i]
            
            tempdata=[]#(target,1nn,2nn,3nn）
            sortedList=self.sortDistance(tempList, datalist[i])
            tempdata.append(datalist[i])
            for i in range(3):
                tempdata.append(sortedList[i][:-1])
            nearList.append(tempdata)    
        
#         print nearList
        return nearList   
      
    def nearNerbONe(self,x,datalist):
        nearList=self.nearNerb(datalist)
        #find 3 nodes whose nearest neighbor is x
        thrNearNeb=[]
        j=3
        while(len(thrNearNeb)<3 and j>0):
            for i in range(len(nearList)):
                if nearList[i][-j][:-1]==x[:-1]:
                    if len(thrNearNeb)<3:
                        thrNearNeb.append(nearList[i][0])
            j=j-1
            
#         print thrNearNeb
        if thrNearNeb is None:
            print "none of nearest neighbors"
        return thrNearNeb   
    
        
    def AccLocalk(self,thrNearNeb,dataList,k):
        #according the k neighbors to determine the classification of each ThrNearNeb
        tempList=[]
        correct=0
        for neighbor in thrNearNeb:
            tempList=dataList[:]
            tempList.remove(neighbor)
            sortedList=[]
            sortedList=self.sortDistance(tempList, neighbor)
#             print sortedList
            classify=self.classifyInstance(sortedList, k, neighbor)
            if classify=='Y':
                correct=correct+1
        if correct==0:
            return 0.0
        else:
            return correct/float(len(thrNearNeb))
            
            
    def evalk(self):
        data=self.readTrainData()
        thrNearNeb=[]
        targetK=[]
        trianedData=[]
        
        accglobalk=self.AccGlobalk()
        for target in data:
            thrNearNeb=self.nearNerbONe(target, data)
            AccK=[]
            for k in range(1,101):
                acclocalk=self.AccLocalk(thrNearNeb, data, k)
                evalk=acclocalk+accglobalk[k-1]
                AccK.append([k,evalk])
             
            RangeAcc=sorted(AccK, key=lambda node: node[-1]) 
            optimalK=RangeAcc[-1][0]#chose the max Eval
             
#             targetK.append([target,optimalK])
            target.append(optimalK)
            trianedData.append(target)
            
        trainR=open('trainRK.txt','w')
        for line2 in trianedData:
            trainR.write(str(line2)+'\n')
            
        return trianedData  

    def knn(self,dataList,target): 
        ##use the knn generate the search path 
        kdtree=genkdTree.kdtree(dataList, depth=0)
        findNearest=KdTreeFindNearest()
        nearList=findNearest.findNearest(kdtree,target)
#         print(nearList)  
        return nearList
    
    def SortedNodes(self,list,target):
        trainList=[]
        for node in list:  
            d=0    
            celdata=[]      
            for i in range(len(node)-2):#the last two attributes are classify and ki
                d+=(node[i]-target[i])**2
                
            celdata=node[:]
            celdata.append(math.sqrt(d))
            trainList.append(celdata)
            
        trainList=sorted(trainList, key=lambda node: node[-1])   
        return trainList
    
    def classifyTestData(self,nnNeighbor,target):
        #classify the test data
        one=0
        two=0
        category=0
        for neighbor in nnNeighbor:
            if neighbor[-1]==self.categorys[0]:
                one+=1
            else:
                two+=1  
                
        if one>two:
            category=self.categorys[0]
        else:
            category=self.categorys[1]
            
        if category==target[-1]:
            return 'Y'
        else:
            return 'N'
    
    def testData(self):       
        testData=self.readTestData()  
        trainedData=self.evalk() #[at1,at2,at3,class,ki]     
        accracy=0
        correct=0
        nnNeighbor=[]
        for target in testData:
            nearList=self.SortedNodes(trainedData, target)#[at1,at2,at3,class,ki,distance] 
            k=nearList[0][-2]#the k value of the nearest neighbor
            for i in range(k):
                nnNeighbor.append(nearList[i][:-2])#[at1,at2,at3,class]
            
            category=self.classifyTestData(nnNeighbor, target)   
            if category=='Y':
                correct=correct+1
                
        accracy=correct/(float(len(testData)))
        print 'the finally accracy is:'
        print accracy 
            
                
               
            
                  
            
            
        
    
def main():
    
    testDataPath="G:/UCI database/BreastCancer/breastCancer_test.data"
    trainDataPath="G:/UCI database/BreastCancer/breastCancer_train.data"
    categorys=['relapse','non-relapse']
    globalk=ValiLocalK(testDataPath,trainDataPath,categorys)
    globalk.testData()
#     data=globalk.testData()
#     print data


#     nearNerb=globalk.nearNerb(data)
#     x=[31, 65, 4]
#     globalk.nearNerbONe(x, nearNerb)
    
    
    
if(__name__ == "__main__"):
    main();    