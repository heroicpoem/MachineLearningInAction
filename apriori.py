# -*- coding: gb2312 -*-
from numpy import *

#构造数据
def loadDat():
    # dat=list([[1,2,3,4,5],[1,2,3],[1,2,3],[1,2,3],[2,3],[1,3,4,5],[3,4,5],[3,4,5],[3,4,5],[3,4,5]])
    dat=list([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]])
    # print(dat)
    return dat

def createC1(dataset):
    #创建1级候选项集
    c1=[];ck=[]
    for tid in dataset:
        for item in tid:
            c1=list([item])
            if not c1 in ck:ck.append(c1)
    ck.sort()
    # ck.append(c1)
    # return frozenset(map(frozenset,c1))
    # return frozenset(list(map(frozenset,c1)))
    return ck
    # return list(map(frozenset,c1))
def scanDat(dat,Ck,minSupport):
    #从候选项计算频繁项集
    allSupport={};freL=[];freSupport={}
    ckCnt=len(Ck)
    for tid in dat:
        # print('tid:',tid)
        # for item in Ck:
        for i in range(ckCnt):
            # print('item:',item)
            # print('Ck[i]',Ck[i])
            fsetCk=frozenset(Ck[i])
            if fsetCk.issubset(tid):
                # if not allSupport.has_key(Ck[i]):allSupport[Ck[i]]=1
                if not fsetCk in allSupport:allSupport[fsetCk]=1
                else:allSupport[fsetCk]+=1
        # print('allSupport:',allSupport)
    tidCnt=len(dat)
    for item in allSupport:
        support=allSupport[item]/tidCnt
        if support>=minSupport:
            freL.append(item)
            freSupport[item]=support
    return freL,freSupport

def aprioriGen(Lk,k2):
    retList=[]
    itemCnt=len(Lk)
    if k2==2:
        for i in range(itemCnt):
            for j in range (i+1,itemCnt):
                l1=list(Lk[i]);l2=list(Lk[j])
                retList.append(set(l1)|set(l2))
        return retList

    for i in range(itemCnt):
        for j in range (i+1,itemCnt):
            # print('Lk[i]:',Lk[i],'Lk[j]:',Lk[j])
            # print('list(Lk[i])[:k2-2]:',list(Lk[i])[:k2-2],'list(Lk[j])[:k2-2]:',list(Lk[j])[:k2-2])
            l1=list(Lk[i])[:k2-2];l2=list(Lk[j])[:k2-2]
            l1.sort();l2.sort()
            # print('l1==l2:',l1==l2)
            if l1==l2:
                retList.append(set(Lk[i])|set(Lk[j]))
    return retList

def apriori(dataset,minsupport=0.5):
    C1=createC1(dataset)
    frqL1,supportData=scanDat(dataset,C1,minsupport)
    frqL=[frqL1]
    k=2
    while (len(frqL[k-2])>0):
        Ck=aprioriGen(frqL[k-2],k)
        # print('Ck:',Ck)
        frqLk,supportk=scanDat(dataset,Ck,minsupport)
        supportData.update(supportk)
        frqL.append(frqLk)
        k+=1
    return frqL,supportData

def calcConf(freqSet,H,supportData,brl,minConf=0.7):
    #freqSet 频繁项集  H 频繁项集子集list，从1项开始，直到频繁项集-1子集。eg：freqSet[1,2,3,4] 子集包括长度为1,2,3的。
    #supportData[频繁项集]的支持度 是置信度的分母；freqSet-H[i] 是前置，置信度的分子
    #函数作用：1）计算置信度，构造规则brl； 2）返回满足置信度的后置列表（后置滚动增加，置信度分母增大，只有满足置信度的才能进入下次的滚动）
    #附录1：支持度代表出现的次数
    prunedH=[]
    for conseq in H:
        print('freqSet:',freqSet)
        print('freqSet-conseq:',freqSet-conseq)
        #规则置信度，sup[freqSet]/sup[freqSet-H]分子相同，分母不同
        #eg:[4,5] 4->5与5->4规则置信度不同，分子都是[4,5]的支持度;分母分别是[4],[5]的支持度
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    print('Func calcConf ret:',prunedH)
    return prunedH

def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7 ):
    #入参：freqSet  频繁项集; H 频繁项集子集的list，作为规则后置；
    #说明：1）用H组合k+1后置，计算置信度；2）递归，
    # 调用aprioriGen,用H各元素构造k+1候选项Hmp1
    # 调用calcConf，计算Hmp1的置信度；Hmp1只保留满足置信度的元素
    # 如果满足置信度的元素数>1(2个及以上)，递归，计算k+1+1规则置信度，直到后置列表<=1或H元素是freqSet-1子集（-1子集构造后置，就得到freqSet）
    # print('*****'*len(freqSet),freqSet,H,supportData,brl)
    m=len(H[0])
    if(len(freqSet)>(m+1)):
        #构造频繁项集候选集
        Hmp1=aprioriGen(H,m+1)
        print('Hmp1:1',Hmp1)
        #Hmp1变成 规则前置
        #calcConf()计算频繁项集->Hmp1子集的置信度，返回支持的子集？
        Hmp1=calcConf(freqSet,Hmp1,supportData,brl,minConf)
        print('Hmp1:1',Hmp1)
        if(len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)

def generateRules(L,supportData,minConf=0.7):
    #参数：L 频繁项集list汇总,L[i]是频繁(i-1)项集列表；
    # 说明：1）对频繁2项集，直接生成规则1->1，并计算置信度
    #       2）对3及以上的频繁项集，递归覆盖k-n>n(n=2,3,k-1)规则，并计算置信度
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet ]
            if(i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList


if __name__=='__main__':
    print('this is main interface!')

    dat=loadDat()
    # c1=createC1(dat)
    # print('c1:',c1)
    # f1,f1support=scanDat(dat,c1,0.5)
    # print('f1:',f1)
    # print('f1support:',f1support)
    frqL,supportdata=apriori(dat)
    print('frqL:',frqL)
    print('supportdata:',supportdata)
    rules=generateRules(frqL,supportdata,minConf=0.7)
    print('rules:',rules)

    # brl=[]
    # for freqSet in frqL[1]:
    #     print(freqSet)
    #     h1=[frozenset([item]) for item in freqSet]
    #     # print('h1:',h1)
    #     calcConf(freqSet,h1,supportdata,brl,0.7)
    # h1=[frozenset([item]) for item in frqL[1]]
    # print('h1:',h1)

    #测试验证
    # set1=list([1,2,3,4])
    # set2=list([4])
    # print(set2.issubset(set1))
    # list1=list()
    # print((list1))
    # print(set(str(1)))
    #数字转list c1转list二位数组
    # i=1
    # l1=list([i])
    # j='i'
    # l1=list('1')
    # l13=list(j)
    # print(l1)
    # print('l13:',l13)
    # l2=[]
    # l2.append(l1)
    # print(l2)

    #list in函数
    # listP=[[1,2,3],[2,3,4],[1,2]]
    # list1=[1,2,3]
    # print(not list1 in listP)

    #dic的key可否是list
    # dic1={}; l1=[1,2]
    # dic1[l1]='x'
    # print(dic1)
    # list1=[1,2,3]
    # fset=frozenset(list1)
    # print(fset)

    #for循环
    # h1=[frozenset([item]) for item in frqL[1]]
    # print('frqL[1]:',frqL[1])
    # print('h1:',h1)
