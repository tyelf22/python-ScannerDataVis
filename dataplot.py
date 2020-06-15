''' Tyson Elfors
6/13/20
CS-1410
Project 5 - Data Visualization
'''

"""I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitues cheating,
and that I will receive a zero on this project if I am found in violation of this policy."""

import numpy as np
import matplotlib.pyplot as plt
import glob

glob.glob("*.dat")

allRanges = []

def analyze(fname):
    raw = np.loadtxt(fname, dtype='i4') #load each file text

    first = raw[:3] #first three of raw for inserting
    second = raw[-3:] #last three of raw for appending

    '''Plotting'''
    # plt.plot(raw)
    # plt.ylabel('some nums')


    def smoothed(i):
        '''Algorithim for smoothing numbers'''
        smooth = (raw[i-3] + raw[i-2]*2 + raw[i-1]*3 + raw[i]*3 + raw[i+1]*3 + raw[i+2]*2 +raw[i+3]) // 15
        return smooth

    listToConvert = [] #initial list
    for i in range(3, len(raw) - 3):  #numbers to smooth disregarding first and last 3 nums 
        smoothNum = smoothed(i)
        listToConvert.append(smoothNum)

    listToConvert.extend(second) #add last elements back to array
    arrayToConvert = np.append(first, listToConvert) #add beginning elements back to array

    smoothedArr = np.array(arrayToConvert) #array of smoothed nums

    convertList = [] #initial list to convert to numpy array
    '''test pulse finder'''
    for i in range(-1, len(smoothedArr) - 3): #find the pulse given the expression
        if smoothedArr[i + 3] - smoothedArr[i] > 100:
            points = True
            convertList.append(points)
        else:
            points = False
            convertList.append(points)


    tfList = np.array(convertList)
    result = np.where(tfList) #pulse indexes where expression was true
    listResult = np.array(result) #convert to np array


    def groupSequence(lst): 
        '''group each of the lists sequentially'''
        res = [[lst[0]]] 
    
        for i in range(1, len(lst)): 
            if lst[i-1]+1 == lst[i]: 
                res[-1].append(lst[i]) 
    
            else: 
                res.append([lst[i]]) 
        return res 

    groupedArr = groupSequence(listResult[0]) #each pulse length


    def Extract(lst): 
        return [item[0] for item in lst] 

    firstEls = Extract(groupedArr) #first nums of each pulse

    for i in range(0, len(firstEls)):
        if i < len(firstEls) -1:
            myListRange = [*range(firstEls[i], firstEls[i + 1])] #the range of numbers for each pulse

            start = myListRange[0] #start of pulse
            end = myListRange[-1] + 1 #end of pulse plus one to include last one

            if len(myListRange) > 50: #if it is greater than fifty only include the first 50
                toSum = raw[start:end]
                aRange = np.sum(toSum)
                allRanges.append(aRange)
            else:
                toSum = raw[start:end] #give start and end nums for calcluating range
                aRange = np.sum(toSum)
                allRanges.append(aRange)

    lastEls = firstEls[-1] 

    allSum = raw[lastEls:lastEls + 50]

    fNameSplit = fname.split(".") #split file name
    fNameFirst = fNameSplit[0] #get the first index of file name

    anotherRange = np.sum(allSum)
    allRanges.append(anotherRange)


    fileI = 1
    elsI = 0
    with open(f"{fNameFirst}.out", 'a') as f: #open text file for appending
        print(f"{fname}:\n", file=f) #print to text file

    for r in allRanges:
        with open(f"{fNameFirst}.out", 'a') as f: #open text file for appending
            print(f"Pulse {fileI}: {firstEls[elsI] + 1} ({r}) \n", file=f) #print to text file
        fileI += 1 #iterator
        elsI += 1 #iterator


    '''Plotting'''
    _,axes = plt.subplots(nrows=2)
    axes[0].plot(raw)
    axes[0].set(title=fname,ylabel="raw",xticks=[])

    axes[1].plot(smoothedArr)
    axes[1].set_ylabel("smooth")

    plt.savefig(f"${fNameFirst}.pdf")# Save plot to a PDF file

    allRanges.clear() #clear the list of all ranges

    return f"{fname} successfully analyzed"

def main():
    '''Iterate over each file with .dat extension for data manipulation'''
    for fname in glob.glob('*.dat'):
        print(analyze(fname))

if __name__ == "__main__":
    main()
