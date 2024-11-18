import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.signal import butter,filtfilt,lfilter
def read_data(fileName):
    #read data and store x y z in each index and convert them to float
    file=open(fileName,'r')
    data=[list(map(float,a.split(',')[1:])) for a in file.read().split('\n')]

    return data
def plot(x,y,xName,yName,graphName):
    plt.plot(x, y)
    plt.xlabel(xName)
    plt.ylabel(yName)
    plt.title(graphName)
    plt.show()  
def staticThresholdStepCounter(threshold,data):
    #using the input threshold outputs the number of steps
    steps=0
    for i in data:
        if i>threshold:
            steps+=1
    return steps
def staticThresholdTester(start,end,step,data):
    #for the given range tests different thresholds
    steps=[]
    for i in range(start,end,step):
        steps.append(staticThresholdStepCounter(i,data))
    return steps
def dynamicThreshold(coeff,window,data):
    steps=0
    windowCounter=0
    mini,maxi=findMinMax(data[0:window])
    for i in range(len(data)):
        threshold=(mini+maxi)*coeff
        
        if data[i]>threshold:
            steps+=1

        windowCounter+=1
        if windowCounter==window:
            windowCounter=0
            mini,maxi=findMinMax(data[i:min(len(data),i+window)])
  
    return steps
def findMinMax(data):
    mini=100000
    maxi=-100000
    for i in data:
        mini=min(mini,i)
        maxi=max(maxi,i)
    return mini,maxi
def lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y+abs(min(y))
def butter_highpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='high', analog=False)

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y+abs(min(y))
data1=read_data(r"MATLAB_DRIVE\MobileSensorData\fast_walk_30.csv")
data2=read_data(r"MATLAB_DRIVE\MobileSensorData\normal_walk_30.csv")
data3=read_data(r"MATLAB_DRIVE\MobileSensorData\jump_10.csv")
data1,data2,data3=data1[:-1],data2[:-1],data3[:-1]

cnt1=[i for i in range(len(data1))]
cnt2=[i for i in range(len(data2))]
cnt3=[i for i in range(len(data3))]
#combining x y z with euclidean
comb1=[math.sqrt(i[0]**2+i[1]**2+i[2]**2) for i in data1]
comb2=[math.sqrt(i[0]**2+i[1]**2+i[2]**2) for i in data2]
comb3=[math.sqrt(i[0]**2+i[1]**2+i[2]**2) for i in data3]
#display unfiltered data
plot(cnt1,comb1,"time","acceleration","fast_walk_30(unfiltered)")
plot(cnt2,comb2,"time","acceleration","normal_walk_30(unfiltered)")
plot(cnt3,comb3,"time","acceleration","jump_10(unfiltered)")
#finding static threshold
plotCnt1=[i for i in range(10,20,1)]
plotCnt2=[i for i in range(10,20,1)]
plotCnt3=[i for i in range(20,40,1)]
steps1=staticThresholdTester(10,20,1,comb1)
steps2=staticThresholdTester(10,20,1,comb2)
steps3=staticThresholdTester(20,40,1,comb3)
plot(plotCnt1,steps1,"threshold","steps","fast_walk_30 steps for each threshold")
plot(plotCnt2,steps2,"threshold","steps","normal_walk_30 steps for each threshold")
plot(plotCnt3,steps3,"threshold","steps","jump_10 steps for each threshold")
#filtering the data
comb1=lowpass_filter(comb1,3,20)
comb2=lowpass_filter(comb2,3,20)
comb3=lowpass_filter(comb3,3,15)
plot(cnt1,comb1,"time","acceleration","fast_walk_30(smoothed)")
plot(cnt2,comb2,"time","acceleration","normal_walk_30(smoothed)")
plot(cnt3,comb3,"time","acceleration","jump_10(smoothed)")



#number of steps 
print(f"fast_walk dynamic threshold steps:{dynamicThreshold(0.55,10,comb1)}")
print(f"normal_walk dynamic threshold steps:{dynamicThreshold(0.55,10,comb2)}")
print(f"jump dynamic threshold steps:{dynamicThreshold(0.82,10,comb3)}")
