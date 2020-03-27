import os.path
import numpy as np
from PIL import Image
import math
class Konwerter:
    def __init__(self):
        self.tempo=[]

        self.tempoMappingX={
            "W":128,
            "H":64,
            "Q":32,
            "E":16,
            "S":8,
            "T":4,
            "X":2
        }
        self.tempoMappingT = {
            "W": 64,
            "H": 32,
            "Q": 16,
            "E": 8,
            "S": 4,
            "T": 2,
        }
        self.tempoMappingMapping = {
            "X": self.tempoMappingX,
            "T": self.tempoMappingT
        }
        #itd..
        self.colorMappingDontSpeakMedium={
            (11,0,0,0,0,0):(3),
            (9, 0, 0, 0, 0, 0): (1),
            (10, 0, 0, 0, 0, 0): (2),
            (8, 0, 0, 0, 0, 0): (0),
            (0,15,18,0,0,0):(1,2),
            (0,16,0,0,0,0):(3),
            (0,15, 0, 0, 0, 0): (2),
            (0,0,18,  0, 0, 0): (1),
            (19, 0, 0, 0, 0, 0): (0),
            (0,14,17,0,0,0):(0,1),
            (0,16,19,0,0,0):(2,3),
            (0,14,0,0,0,0):(1),
            (0,13,0,0,0,0):(2),
            (0,0,17,0,0,0):(1),
            (0,0,19,0,0,0):(0),
            (0, 0, 0, 0, 0, 0):-1
        }
        self.colorMappingDuHastMedium={
            (10,0,0,0,0,0):(2),
            (9,15,0,0,0,0):(1,2),
            (13,13,18,0,0,0):(0,1),
            (8,0,0,0,0,0):(0),
            (8,14,0,0,0,0):(0,1),
            (13,14,19,0,0,0):(1,2),
            (9,0,0,0,0,0):(1),
            (10,16,0,0,0,0):(2,3),
            (13,15,20,0,0,0):(2,3),
            (11,0,0,0,0,0):(3),
            (0,0,0,0,0,0):-1
        }
        self.RGBMapping={
            0:(0,255,0),
            1:(255,0,0),
            2:(255,255,0),
            3:(0,0,255),
            4:(255,165,0)
        }
    def allInList(self,x,num):
        for i in x:
            if i!=num:
                return False
        return True

    def find(self,s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]
    def setTempoMapping(self,val):
        self.tempoMapping=self.tempoMappingMapping[val]
    def loadText(self,path,):

        with open(path) as inp:
            j=0
            triolaCounter=0

            triola=[]
            self.matrix=[]
            for line in inp:
                self.matrix.append([])
                if line=='Duration Legend\n':
                    break
                if line[0]==' ':
                    for i in line:
                        if i==' ':
                            self.matrix[j].append(-1)
                        elif i=='3':
                            triola=self.find(line,'3')
                            triola=list(set(triola))
                            self.matrix[j].append(-1)
                        elif i!='\n':
                            if i=='.':
                                self.matrix[j][-1]+=1/2*self.matrix[j][-1]
                                self.matrix[j].append(-1)
                            elif i in self.tempoMappingX:
                                self.matrix[j].append(self.tempoMapping[i])
                            else:
                                self.matrix[j].append(-1)
                    for index in triola:
                        if self.matrix[j][index] > 0:
                            self.matrix[j][index]=self.matrix[j][index]*2/3
                            triolaCounter+=self.matrix[j][index]%1
                           
                           # if triolaCounter%1<0.0003 or triolaCounter%1>0.9997:
                            #    self.matrix[j][index]+=round(triolaCounter)
                             #   triolaCounter=0
                            if triolaCounter>1:
                                triolaCounter-=1
                                self.matrix[j][index]+=1
                            self.matrix[j][index]=int(self.matrix[j][index])

                elif line[0]=='\n':
                    triola=[]
                    continue

                else:
                    for i in line:
                        if i.isdigit():
                            if self.matrix[j][-1]!=-1:
                                tmp=self.matrix[j][-1]
                                self.matrix[j].append(int(i)+tmp*10)
                                self.matrix[j][-2]=0
                            else:
                                self.matrix[j].append(int(i))
                        elif i=='L':
                            self.matrix[j].append(-2)

                        else:
                            self.matrix[j].append(0)

                j += 1
    def transpose(self):
        self.transposedMatrix=[]
        for i in self.matrix:
            while len(i)<len(max(self.matrix,key=len)):
                if len(i)>0:
                    if i[-1]==0:
                        i.append(0)
                    elif i[-1]==-1:
                        i.append(-1)
                else:
                    i.append(-1)

        self.matrix=[i for i in self.matrix if not self.allInList(i,-1)]

        for i in range(0,len(self.matrix),7):
            tmp=np.array(self.matrix[i:i+7])
            tmp=np.transpose(tmp)
            tmp=tmp.tolist()
            for j in tmp:
                self.transposedMatrix.append(j)

        self.transposedMatrix=[i for i in self.transposedMatrix if not i[0]==-1]
        for i in range(len(self.transposedMatrix)):
            for j in range(len(self.transposedMatrix[i])):
                if self.transposedMatrix[i][j]==-2:
                    self.transposedMatrix[i][j]=self.transposedMatrix[i-1][j]
        for i in self.transposedMatrix:
            print(i)

    def draw(self,title,song):
        width=0
        for i in self.transposedMatrix:
            width+=i[0]
        image=Image.new('RGB',(int(width),16),color='black')
        img=image.load()
        current=0
        for i in self.transposedMatrix:
            length=int(i[0])
            color=song[tuple(i[1:])]
            if color!=-1:
                if type(color)==tuple:
                    for j in range(length):
                        for k in color:
                            img[j+current,1+k*4]=self.RGBMapping[k]
                            img[j + current,2 + k*4] = self.RGBMapping[k]
                else:
                    for j in range(length):
                        img[j+current,1+color*4]=self.RGBMapping[color]
                        img[j + current,2 + color*4] = self.RGBMapping[color]
            current+=length


        image.save(title)

    def generateTextFile(self,song,path):
        sum=0
        tempoIterator=0
        currentTempo=self.tempo[tempoIterator]
        file=open(path,"w")
        for i in self.transposedMatrix:
            file.write(str(int(i[0])))
            file.write(" ")
            accord=song[tuple(i[1:])]
            if type(accord)==tuple:
                for j in accord:

                    file.write(str(j))
                    file.write(" ")
            else:
                if (accord == -1):
                    file.write("7 ")
                else:
                    file.write(str(accord))
                    file.write(" ")
            # file.write(str(currentTempo))
            file.write(str(self.tempo[tempoIterator]))
            tempoIterator+=1
            # sum+=int(i[0])
            # if tempoIterator==0:
            #     if sum==64:
            #         if (tempoIterator < len(self.tempo) - 1):
            #             tempoIterator += 1
            #             currentTempo = self.tempo[tempoIterator]
            #             sum = 0
            # else:
            #     if sum==128:
            #         if(tempoIterator<len(self.tempo)-1):
            #             tempoIterator+=1
            #             currentTempo=self.tempo[tempoIterator]
            #             sum=0
            file.write("\n")
            
    def generateTempo(self,path):
        self.tempo=[]
        tempo=0
        tempoString=""
        newTact=False
        with open(path) as inp:
            for line in inp:

                x=line.find("measure")
                if x>=0:

                    if line[x-1]=='<':
                        if newTact:
                            self.tempo.append(tempo)
                        else:
                            newTact=True
                        continue
                if not newTact:
                    continue
                x=line.find("tempo")
                if x>=0:
                    for i in line[x+7:]:
                        if i.isdigit():
                            tempoString+=i
                        else:
                            tempo=int(tempoString)
                            newTact=False
                            self.tempo.append(tempo)
                            tempoString=""
                            break

    def generateTempo2(self, path):
        self.tempo = []
        tempo = 0
        tempoString = ""
        with open(path) as inp:
            for line in inp:
                x = line.find("tempo")
                if x >= 0:
                    for i in line[x + 7:]:
                        if i.isdigit():
                            tempoString += i
                        else:
                            tempo = int(tempoString)
                            tempoString = ""
                            break
                x=line.find("<note><pitch>")
                if x>=0:
                    self.tempo.append(tempo)
                x = line.find("<note><rest>")
                if x >= 0:
                    self.tempo.append(tempo)



konwerter=Konwerter();
konwerter.setTempoMapping('X')
konwerter.loadText("sw/DS/DS.tab")
konwerter.transpose()
konwerter.generateTempo2('sw/DS/notesP.xml')
print(konwerter.tempo)
konwerter.generateTextFile(konwerter.colorMappingDontSpeakMedium,'sw/DS/DS.txt')
konwerter.draw('sw/DS/DS.png',konwerter.colorMappingDontSpeakMedium)