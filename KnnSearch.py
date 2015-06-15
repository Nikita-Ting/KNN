#encoding:utf-8

''' created on 2014-8-26
算法：k-d树最邻近查找  
输入：Kd，    //k-d tree类型  
     target  //查询数据点  
输出：nearest， //最邻近数据点  
     distance      //最邻近数据点和查询点间的距离 
     
   search_path：搜索路径集  
     1. 如果Kd是空的，则设dist为无穷大返回   
    2. 向下搜索直到叶子结点   
   
'''

import math


class KdTreeFindNearest():
     
    def GetDistance(self,nearest,target):
        d=0
        for i in range(len(nearest)-2):#the last two attribute are classfication and ki
            d+=(nearest[i]-target[i])**2
        return math.sqrt(d)
   
   
    def findNearest(self,tree,target):
        search_path=[]   #搜索路径 
        depth=0         #二叉树深度
        minxDistance=0      #最近邻点与目标点距离
        nearList=[]  #搜索路径上的点以及与目标点的距离
        nearest=None
        if tree is None:
            minxDistance=float("inf")
            nearest=None
            return nearList
        
        kd_root=tree
#         k = len(kd_root.location) # assumes all points have the same dimension
        nearest=tree.location  #init nearest point
        while(kd_root):
            search_path.append(kd_root)
#             axis = depth % k
            if target[kd_root.split] <= kd_root.location[kd_root.split]:
                kd_root=kd_root.left_child
            else:
                kd_root=kd_root.right_child
#             depth+=1
        
        
        nearest = search_path.pop()   #移除一个元素并返回该元素值  
        minxDistance=self.GetDistance(nearest.location,target) #回溯初始最近邻
     #--生成搜索路径--
        nearList.append([nearest.location,minxDistance])
        pathNode=[]
        while(search_path):
            pBack=search_path.pop()
#             depth=depth-1
#             axis=axis = depth % k
            axis=pBack.split
            if(abs(pBack.location[axis]-target[axis])<minxDistance):
                if  self.GetDistance(pBack.location,target) < self.GetDistance(nearest.location,target):
                    nearest=pBack
                    minxDistance=self.GetDistance(pBack.location,target)
                    nearList.append([nearest.location,minxDistance])
                    
                if target[axis] <= pBack.location[axis]:
                    kd_root=pBack.right_child   #如果target位于左子空间，就应进入右子空间
                else:
                    kd_root=pBack.left_child
                if kd_root:
                    search_path.append(kd_root)
                    if self.GetDistance(kd_root.location,target) < self.GetDistance(nearest.location,target):
#                         depth+=1
                        nearest=kd_root
                        minxDistance=self.GetDistance(kd_root.location,target)
                        nearList.append([nearest.location,minxDistance])
                        
        nearList=sorted(nearList, key=lambda node: node[-1])        
        return nearList
                
        
def main():
    getdistance=KdTreeFindNearest()
    distance=getdistance.GetDistance((4,2,8), (2,6,1))
    print (distance)
        
if(__name__ == "__main__"):
    main();

