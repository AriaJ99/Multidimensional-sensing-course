
import sys          # System manipulation
import time         # Used to pause execution in threads as needed
import keyboard     # Register keyboard events (keypresses)
import threading    # Threads for parallel execution
import pyaudio      # Audio streams
import numpy as np  # Matrix/list manipulation
import audioop      # Getting volume from sound data
import math
# import struct       # Used for converting sound data to integer lists
# For recording the sound into playable .wav files
# from scipy.fftpack import fft 
# import wave

# GUI dependencies
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import * 

# Constants for streams, modify with care!
CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
buffer_width = 100
overallVar=0


print("Available audio devices:")
# Check the input devices
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
p.terminate()


# Modified from:
# https://people.csail.mit.edu/hubert/pyaudio/

# This is the method running on a thread, one initialized for each audio device
def log_sound(index, label,calLabel):
    
    # This global buffer consists of several lists, this stream has a list available at the provided index
    # Store the volume data at: buffer[index]
    global buffer       
    global mean
    global variance
    global buffer_width
    # wave_buffer = []      # Store audiosignal here
    
    # Open stream
    stream = p.open(
        format = FORMAT,           # Format of stream data
        channels = CHANNELS,       # Number of input channels
        rate = RATE,               # Frequency of audio
        input = True,              # Stream reads data
        frames_per_buffer = CHUNK, # Number of inout frames for each buffer
        input_device_index = index # Input device
    )

    while True:
            
        # Read a chunk of data from the stream
        data = stream.read(CHUNK)
        
        # Store the data in buffer for .wav file convertion
        # wave_buffer.append(data)
        
        # Calculate the volume from the "chunk" of data
        volume = audioop.rms(data, 2)
        
        # Append the necessary data to the buffer

        #volume=(volume-m)/math.sqrt(myVarianceV2(buffer[index],m))
        buffer[index].append(volume)
        m=myMeanV2(buffer[index])
        v=myVarianceV2(buffer[index],m)
        if len(buffer[index])>buffer_width:
            buffer[index]=buffer[index][-buffer_width:]
        if fault_check(v,200):
            #check if device is faulty
            label.setText(str(index)+ f" Faulty device" )
            calLabel.setText(f"{index} -> mean : {m} , var : {v}" )
        else:
            label.setText(str(index)+ f" : {volume} " )
            calLabel.setText(f"{index} -> mean : {m} , var : {v}" )

        
        # Check for quit command
        if keyboard.is_pressed('q') or quit_flag:
            
            print("Closing stream", index)
            stream.stop_stream()
            stream.close()
            
            # Save the buffer as a .wav file, for testing purposes only
            #print("Storing f"+str(index)+".wav")
            #wf = wave.open("f"+str(index)+".wav", 'wb')
            #wf.setnchannels(CHANNELS)
            #wf.setsampwidth(p.get_sample_size(FORMAT))
            #wf.setframerate(RATE)
            #wf.writeframes(b''.join(wave_buffer))
            #wf.close()
            break

            
# Close threads when window is closed
def exitMethod():
    global quit_flag
    quit_flag = True
    
# This is the main thread, the code should be implemented here
def mainThread(mean_label, var_label):
    
    # This is the buffer which includes data from all audio sources
    global buffer
    global overallVar
    # the buffers sould only include the latest entries, this is the length of them
    # try finding a suitable value for it
    
    
    while True:
        
        # Check the exit condition and join the threads if it is met
        if keyboard.is_pressed('q') or quit_flag:
            for x in threads:
                x.join()
            p.terminate()
            break
            
        #time.sleep(0.01) # Pause the updates
        
        # Limit buffers to the buffer_width
        #for i in range(len(buffer)):
        #    buffer[i] = buffer[i][-buffer_width:]  
        m=myMeanV1(buffer)
        overallVar=myVarianceV1(buffer,m)
        mean.setText(f"Mean: {m}")
        variance.setText(f"Variance: {overallVar}")
        # Here we check the variance of each device and if it's too high we conclude that it has a problem
        #for i in buffer:
            #var=myVarianceV2(buffer[i])
            
        # The method has been given a set of labels where you may put the desired text
        # Use 'label.setText(string)' to display text

            

    print("Execution finished")
def myMeanV1(data):
    #mean of a 2d list
    sum=0
    cnt=0
    
    for i in data:
        for j in i:
            sum+=j
            cnt+=1
    if cnt==0:
        return 1
    return sum/cnt
def myVarianceV1(data,mean):
    #variance of 2d list
    cnt=0
    sum=0
    for i in data:
        for j in i:
            cnt+=1
            sum+=(j-mean)**2
    if cnt==0:
        return 1
    return sum/cnt
def myMeanV2(data):
    #mean of 1d list
    sum=0
    cnt=0
    for i in data:
        sum+=i
        cnt+=1
    if cnt==0 or sum==0:
        return 1
    return sum/cnt
def myVarianceV2(data,mean):
    #variance of a 1d list
    cnt=0
    sum=0
    for i in data:
        cnt+=1
        sum+=(i-mean)**2
    if cnt==0 or sum==0:
        return 1
    return sum/cnt
def fault_check(variance,threshold):
    global overallVar
    #check if input var is smaller than overall variance divided by threshold
    if variance<overallVar/threshold:
        return True
    return False
# Store threads and labels
threads = []
labels = []
calLabels=[]
buffer = []
quit_flag = False

# GUI
app = QApplication(sys.argv)
app.aboutToQuit.connect(exitMethod)

# Initializing window
window = QWidget()
window.setWindowTitle('Soundwave log')
window.setGeometry(100, 100, 1000, 500)
window.move(500, 500)

# Initialize pyaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

# Run the threads
for i in range(0, numdevices):
    
        # Check if the device takes input
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            
            # Initialize labels
        labels.append(QLabel("____________", parent = window))
        labels[-1].move(60, (15 * (i+1)) + (10*i))
        labels[-1].setFont(QFont('Arial', 10))
        labels[-1].setFixedWidth(1000)
        calLabels.append(QLabel("____________", parent = window))
        calLabels[-1].move(60, (15 * (numdevices+1))+(15 * (i+1)) + (10*i))
        calLabels[-1].setFont(QFont('Arial', 10))
        calLabels[-1].setFixedWidth(1000)
            # Append a new buffer to the global list
        buffer.append([])
        
            # Start threads
        threads.append(threading.Thread(target=log_sound, args=(i, labels[i],calLabels[i])))
        threads[i].start()

# Init. labels for combined data     
   
mean = QLabel(f"Mean: {myMeanV1(buffer)}", parent = window)
mean.move(60, (15 * 2*numdevices + (10 * 2*numdevices)))
mean.setFont(QFont('Arial', 12))
mean.setFixedWidth(1000)

variance = QLabel(f"Variance: {myVarianceV1(buffer,myMeanV1(buffer))}", parent = window)
variance.move(60, (15 * 2*numdevices + (13 * (2*numdevices + 2))))
variance.setFont(QFont('Arial', 12))
variance.setFixedWidth(1000)


# Start the main thread
main_thread = threading.Thread(target = mainThread, args=[mean, variance])
main_thread.start()

# Show window
window.show()
# Run GUI-application loop
app.exec_()



# Implementation without threads
