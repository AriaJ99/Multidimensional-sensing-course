import matplotlib.pyplot as plt
def read_data(fileName):
    #read data and store x y z in each index and convert them to float
    file=open(fileName,'r')
    data=[list(map(float,a.split(',')[1:])) for a in file.read().split('\n')]

    return data
def plot(x,y):
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')

    # giving a title to my graph
    plt.title('My first graph!')

    # function to show the plot
    plt.show()  
def staticThreasholdStepCounter(threshold,data):
    steps=0
    for i in data:
        if i>threshold:
            steps+=1
    return steps
data=read_data(r"MATLAB_DRIVE\MobileSensorData\fast_walk.csv")
data=data[:-1]
#print(data)
cnt=[i for i in range(len(data))]
x=[i[0] for i in data]
y=[i[1] for i in data]
z=[i[2] for i in data]


plot(cnt[50:400],x[50:400])