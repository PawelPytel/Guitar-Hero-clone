import time
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import RPi.GPIO as GPIO
import pygame
from timeit import default_timer as timer
import math
import sqlite3

# main vars
green = 26  # left
red = 19  # ok
yellow = 13
blue = 5  # right
orange = 16
songLines = []
timeStamp = 0


def playSound(self, songPath):
    pygame.mixer.init()
    pygame.mixer.music.load(songPath)
    sumOfNotes = sum([float(note[0]) for note in songLines])
    pygame.mixer.music.play()


class GuitarHero(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GuitarHero, self).__init__(*args, **kwargs)
        self.setUpButtons()

    def setUpButtons(self):
        # Configures pin numbering to Broadcom reference
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  # Disable Warnings
        GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(orange, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def buttonPressed(self, pin, color, double_buffer, i):
        if GPIO.input(pin) == 0:
            for col in range(3, 7):
                double_buffer.SetPixel(col, 4*i, color[0], color[1], color[2])
                double_buffer.SetPixel(
                    col, 4*i+3, color[0], color[1], color[2])
        return GPIO.input(pin) == 0

    def run(self):
        songList, textList, fileList, imageList, highScores, count, conn = dbConnection()
        fontPath = "../../../fonts/tom-thumb.bdf"
        textColor = graphics.Color(255, 255, 255)
        starColor = graphics.Color(255, 255, 0)
        while(True):

            #textPath = "sw/WIMM/WIMM.txt"
            #imagePath = "sw/WIMM/WIMM.png"
            #songPath = "sw/WIMM/song.ogg"
            songIndex = 0
            pos = 0
            star = ""
            starProgs = [0.1, 0.25, 0.49, 0.64,0.81]

            options = RGBMatrixOptions()
            double_buffer = self.matrix.CreateFrameCanvas()
            font = graphics.Font()
            font.LoadFont(fontPath)

            while(True):
                double_buffer.Clear()
                pos-=1
                if pos <= -4* len(songList[songIndex]):
                    pos = 31
                my_text = songList[songIndex]
                lenn = graphics.DrawText(
                double_buffer, font, pos, 10, textColor, my_text)
                double_buffer = self.matrix.SwapOnVSync(double_buffer)
                time.sleep(0.2)
                if GPIO.input(green) == 0:
                    songIndex -= 1
                    if songIndex <= -1:
                        songIndex = count-1
                if GPIO.input(blue) == 0:
                    songIndex += 1
                    if songIndex >= count:
                        songIndex = 0
                if GPIO.input(red) == 0:
                    break

                
                

            #double_buffer.Clear()

            for row in range(0, 16):
                for col in range(0, 32):
                    double_buffer.SetPixel(col, row, 0, 0, 0)
                
            for row in range(0, 16):
                double_buffer.SetPixel(7, row, 255, 255, 255)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            
          
            songLines=self.loadText(textList[songIndex])

            
            self.image = Image.open(imageList[songIndex]).convert('RGB')
            self.image.resize(
                (self.matrix.width, self.matrix.height), Image.ANTIALIAS)
            img_width, img_height = self.image.size
            timeStamp = (60/(float(songLines[0][-1])*16))
                             
            xpos = -10
            points = 0
            hit = 0
            combo = 0
            multiplier = 1
            start = 0
            cnt = 0
            cmb = 1
            maxPoints = 0
            maxHit = 0
            
            for line in songLines:
                if line[1] != 7:
                    maxHit += int(line[0]) * (len(line)-2)
                    maxPoints += int(line[0]) * (len(line)-2)*cmb
                    cnt += 1
                    if cnt >= 20 and cmb < 4:
                        cnt = 0
                        cmb += 1

            print(maxPoints)
            print(maxHit)
            playSound(self, fileList[songIndex])
            for line in songLines:
                for i in range(int(line[0])):
                    if i == 0:
                        start = timer()
                    xpos += 1
                    double_buffer.SetImage(self.image, -xpos)
                    double_buffer.SetImage(self.image, -xpos + img_width)

                    greenPressed = self.buttonPressed(pin=green, color=(
                        0, 255, 0), double_buffer=double_buffer, i=0)
                    redPressed = self.buttonPressed(pin=red, color=(
                        255, 0, 0), double_buffer=double_buffer, i=1)
                    yellowPressed = self.buttonPressed(pin=yellow, color=(
                        255, 255, 0), double_buffer=double_buffer, i=2)
                    bluePressed = self.buttonPressed(pin=blue, color=(
                        0, 0, 255), double_buffer=double_buffer, i=3)
                   # self.buttonPressed(pin = orange, color = (255,128,0), double_buffer = double_buffer,i=4, line[1:-1], )

                    for row in range(0, 16):
                        double_buffer.SetPixel(7, row, 255, 255, 255)

                    for row in range(0, 16):
                        double_buffer.SetPixel(28, row, 255, 255, 255)
                        for col in range(29, 32):
                            double_buffer.SetPixel(col, row, 0, 0, 0)
                    for note in line[1:-1]:
                        if note == "0":
                            if greenPressed == True:
                                hit += 1
                                points += multiplier
                                combo += 1
                            else:
                                combo = 0
                                multiplier = 1
                        if note == "1":
                            if redPressed == True:
                                hit += 1
                                points += multiplier
                                combo += 1
                            else:
                                combo = 0
                                multiplier = 1
                        if note == "2":
                            if yellowPressed == True:
                                hit += 1
                                points += multiplier
                                combo += 1
                            else:
                                combo = 0
                                multiplier = 1
                        if note == "3":
                            if bluePressed == True:
                                hit += 1
                                points += multiplier
                                combo += 1
                            else:
                                combo = 0
                                multiplier = 1

                    if points >= starProgs[len(star)] * maxPoints:
                        star += "*"

                    if combo >= 20 and multiplier<4:
                        multiplier += 1
                        combo = 0
                        
                    for m in range(0,multiplier):
                        for n in range(0,3):
                            double_buffer.SetPixel(31-n,15-m, 255, 255, 128- 128/(4-m))
                                                  
                    for m in range(0,len(star)):
                            double_buffer.SetPixel(30,2*m+1, 255, 255, 0)
                            
                            
                            
                    double_buffer = self.matrix.SwapOnVSync(double_buffer)
                    end = timer()
                    time.sleep(timeStamp-(end-start))
                    start = timer()

            pygame.mixer.music.stop()
            double_buffer.Clear()
            double_buffer = self.matrix.SwapOnVSync(double_buffer)

            percentage = int(float(hit)/float(maxHit)*100)
            pointsColor = textColor
            if highScores[songIndex] < points:
                pointsColor = starColor
                highScores[songIndex] = points               
                c = conn.cursor()
                c.execute( "Update songs set highScore=" + str(points)+ " where id = "+str(songIndex)+";")
                 
                conn.commit()
            else:
                pointsColor = textColor
            while True:
                if GPIO.input(blue) == 0:
                    break
                
                double_buffer.Clear()
                lenn = graphics.DrawText(
                double_buffer, font, 2*(8-len(str(points))), 6, pointsColor, str(points))
                if percentage < 100:
                    lenn = graphics.DrawText(
                        double_buffer, font, 11, 12, pointsColor, str(percentage)+"%")
                else:
                    lenn = graphics.DrawText(
                        double_buffer, font, 9, 12, pointsColor, str(percentage)+"%")

                lenn = graphics.DrawText(
                    double_buffer, font,  2*(8-len(str(star))), 18, starColor, star)
                double_buffer = self.matrix.SwapOnVSync(double_buffer)
                time.sleep(0.2)
            maxPoints = 0
            maxHit = 0
            songLines = []
    def loadText(self, path,):
        songLines=[]
        with open(path) as inp:
            for line in inp:
                songLines.append(line[:-1].split(" "))
        return songLines


def dbConnection():
    with open("sw/DB.db") as inp:
        conn = sqlite3.connect("sw/DB.db")

        if conn is not None:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS songs
            (
            id integer PRIMARY KEY,
            name text,
            textPath text,
            songPath text,
            imagePath text,
            highScore text
            );
            """)
            c = conn.cursor()
           # c.execute( """
           #  insert into songs(id,name,textPath,songPath,imagePath,highScore)
           #  Values (0, 'Where is my mind?', 'sw/WIMM/WIMM.txt','sw/WIMM/song.ogg','sw/WIMM/WIMM.png', 0);
           #  """);
            #c.execute("delete from songs where id=1;")
           # c.execute("""
           #  insert into songs(id,name,textPath,songPath,imagePath,highScore)
           # Values (1, 'Test', 'sw/test/test.txt','sw/test/song.ogg','sw/test/test.png', 0);
           #  """);
           # conn.commit()
            songList = c.execute("select * from songs;").fetchall()

            nameList = [str(x[1]) for x in songList]
            textList = [str(x[2]) for x in songList]
            fileList = [str(x[3]) for x in songList]
            imageList = [str(x[4]) for x in songList]
            highScores = [int(x[5]) for x in songList]
            return nameList, textList, fileList, imageList, highScores, len(nameList), conn


if __name__ == "__main__":
    pygame.init()
    game = GuitarHero()
    if (not game.process()):
        game.print_help()

