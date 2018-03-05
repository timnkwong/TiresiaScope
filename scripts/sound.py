"""Play a fixed frequency sound."""
from __future__ import division
import math
import Queue
import threading
import time

#sensor queues
q1 = Queue.Queue()
q2 = Queue.Queue()
q3 = Queue.Queue()
q4 = Queue.Queue()
q5 = Queue.Queue()
q6 = Queue.Queue()
q7 = Queue.Queue()
q8 = Queue.Queue()

wRange = 200
aRange = 100
sRange = 0
dRange = 50
qRange = 200
eRange = 100
zRange = 0
cRange = 50


from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

#simulate sensor value reading

##Functionality:
##    Input some string with characters W, w, A, a, S, s, D, d
##    and the simulator will parse through and increment/decrement specified directions
##    based on the dedicated characters read (i.e. W/w represents range of front sensor
##                                            and will increase/decrease readings on that
##                                            direction)

##  The intent of this code when implemented with hardware is to read values of ASCII and translate
##  them to audio values
def simulate():
   while True:
        #print("WASDQEZC corresponds to each direction. Enter WASDQEZC to increase distance. Enter wasdqezc to decrease. \n")
        command = raw_input('In\n')
        if(len(command) == 0):
            continue
        if(command == "endd"):
            break
        deltaW = command.count('W') - command.count('w')
        deltaA = command.count('A') - command.count('a')
        deltaS = command.count('S') - command.count('s')
        deltaD = command.count('D') - command.count('d')
        deltaQ = command.count('Q') - command.count('q')
        deltaE = command.count('E') - command.count('e')
        deltaZ = command.count('Z') - command.count('z')
        deltaC = command.count('C') - command.count('c')
        if(deltaW != 0):
            print('Placing ' + str(deltaW) + ' into queue')
            q1.put(str(deltaW))
        if(deltaA != 0):
            print('Placing ' + str(deltaA) + ' into queue')
            q2.put(str(deltaA))
        if(deltaS != 0):
            print('Placing ' + str(deltaS) + ' into queue')
            q3.put(str(deltaS))
        if(deltaD != 0):
            print('Placing ' + str(deltaD) + ' into queue')        
            q4.put(str(deltaD))
        if(deltaQ != 0):
            print('Placing ' + str(deltaQ) + ' into queue')
            q5.put(str(deltaW))
        if(deltaE != 0):
            print('Placing ' + str(deltaE) + ' into queue')
            q6.put(str(deltaA))
        if(deltaZ != 0):
            print('Placing ' + str(deltaZ) + ' into queue')
            q7.put(str(deltaS))
        if(deltaC != 0):
            print('Placing ' + str(deltaC) + ' into queue')        
            q8.put(str(deltaD))
        time.sleep(2)

#sensor setup#
def sensor1():
    while True:
        data = q1.get()
        dist = int(data)
        range_to_sound(dist, 1)

def sensor2():
    while True:
        data = q2.get()
        dist = int(data)
        range_to_sound(dist, 2)
        
def sensor3():
    while True:
        data = q3.get()
        dist = int(data)
        range_to_sound(dist, 3)

def sensor4():
    while True:
        data = q4.get()
        dist = int(data)
        range_to_sound(dist, 4)
        
def sensor5():
    while True:
        data = q1.get()
        dist = int(data)
        range_to_sound(dist, 5)

def sensor6():
    while True:
        data = q2.get()
        dist = int(data)
        range_to_sound(dist, 6)
        
def sensor7():
    while True:
        data = q3.get()
        dist = int(data)
        range_to_sound(dist, 7)

def sensor8():
    while True:
        data = q4.get()
        dist = int(data)
        range_to_sound(dist, 8)

#end sensor setup#
        
##def pos_to_freq(pos):
##    #for simplicity sake of testing, freq will just be pos*100, can edit to be more dynamic
##    return pos*100

#VALUES ARE NOT NORMALIZED YET

def range_to_sound(dist, pos):
    #dist will represent the RS-232 value of the sensor output, range 0-255
    #dist will represent volume of the tone
    #pos will be dependent on which sensor is outputting
    global wRange
    global aRange
    global sRange
    global dRange
    global qRange
    global eRange
    global zRange
    global cRange
    if(pos == 1):
        if(wRange + dist > 255):
            wRange = 255
        elif(wRange + dist < 0):
            wRange = 0
        else:
            wRange = wRange + dist
        print('New range: '+str(wRange))
        rsVal = intToAscii(wRange)
    elif(pos == 2):
        if(aRange + dist > 255):
            aRange = 255
        elif(wRange + dist < 0):
            aRange = 0
        else:
            aRange = aRange + dist
        rsVal = intToAscii(aRange)
    elif(pos == 3):
        if(sRange + dist > 255):
            sRange = 255
        elif(sRange + dist < 0):
            sRange = 0
        else:
            sRange = sRange + dist
        rsVal = intToAscii(sRange)
    elif(pos == 4):
        if(dRange + dist > 255):
            dRange = 255
        elif(dRange + dist < 0):
            dRange = 0
        else:
            dRange = dRange + dist
        rsVal = intToAscii(dRange)
    elif(pos == 5):
        if(qRange + dist > 255):
            qRange = 255
        elif(qRange + dist < 0):
            qRange = 0
        else:
            qRange = qRange + dist
        print('New range: '+str(qRange))
        rsVal = intToAscii(qRange)
    elif(pos == 6):
        if(eRange + dist > 255):
            eRange = 255
        elif(eRange + dist < 0):
            eRange = 0
        else:
            eRange = eRange + dist
        rsVal = intToAscii(eRange)
    elif(pos == 7):
        if(zRange + dist > 255):
            zRange = 255
        elif(zRange + dist < 0):
            zRange = 0
        else:
            zRange = zRange + dist
        rsVal = intToAscii(zRange)
    elif(pos == 8):
        if(cRange + dist > 255):
            cRange = 255
        elif(cRange + dist < 0):
            cRange = 0
        else:
            cRange = cRange + dist
        rsVal = intToAscii(cRange)
    parseDist = rs232parse(rsVal)
    if(parseDist != -1):
        freq = translate(parseDist, 0, 255, 0, 2200)
        print("Freq: "+ str(freq))
        #freq = pos_to_freq(pos)
        sine_tone(freq, 5, 0.5, 22050)
    

def intToAscii(val):
    intStr = str(val)
    asciiStr = "82 " #82 = R
    for i in range(0, len(intStr)):
        asciiStr = asciiStr + str(ord(intStr[i])) + ' '
    asciiStr.rstrip()
    print(asciiStr)
    return(asciiStr)

#parse in rs232 inputs
def rs232parse(rsIn):
    #assuming rsIn = "82 X X X" in strings split by chars"
    asciiSplit = rsIn.split()
    asciiStr = ""
    for c in asciiSplit:
        asciiStr = asciiStr + chr(int(c))
    if(asciiStr[0] != 'R'):
        return -1
    try:
        dist = int(asciiStr[1:])
        if(dist > 255 or dist < 0):
            return -1
        print('RS232 parse: '+str(dist))
        return dist
    except Exception:
        return -1

#rs232 key simulation
    
      
#https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

#https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound
def sine_tone(frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), # 8bit
                    channels=1, # stereo
                    rate=sample_rate,
                    output=True)
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
    for buf in izip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

    stream.stop_stream()
    stream.close()
    p.terminate()
    
        
#multithread in order to have sensors work in parallel
s1 = threading.Thread(target = sensor1)
s2 = threading.Thread(target = sensor2)
s3 = threading.Thread(target = sensor3)
s4 = threading.Thread(target = sensor4)
s5 = threading.Thread(target = sensor5)
s6 = threading.Thread(target = sensor6)
s7 = threading.Thread(target = sensor7)
s8 = threading.Thread(target = sensor8)


s1.daemon = True
s2.daemon = True
s3.daemon = True
s4.daemon = True
s5.daemon = True
s6.daemon = True
s7.daemon = True
s8.daemon = True


s1.start()
s2.start()
s3.start()
s4.start()
s5.start()
s6.start()
s7.start()
s8.start()

simulate()
#simulate()
