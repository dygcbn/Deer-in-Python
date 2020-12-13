import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt,QTimer
import random,time
from pygame import mixer
from mutagen.mp3 import MP3
import style


musicList=[]
mixer.init()
muted=False
count=0
songLength=0
index=0




class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müzik Çalar")
        self.setGeometry(450,180,750,700)
        self.UI()
        self.show()

    def UI(self):
       self.widgets()
       self.layouts()

    def widgets(self):
        ########################progress bar#############
        self.progressBar=QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(style.progressBarStyle())
        ########################Labels###################
        self.songTimerLabel=QLabel("0:00")
        self.songLenthLabel=QLabel("/ 0:00")
        #######################Buttons###################
        self.ekle =QToolButton()
        self.ekle.setIcon(QIcon("icons/add.png"))
        self.ekle.setIconSize(QSize(48,48))
        self.ekle.setToolTip("Müzik Ekle")
        self.ekle.clicked.connect(self.addSound)

        self.shuffleButton=QToolButton()
        self.shuffleButton.setIcon(QIcon("icons/shuffle.png"))
        self.shuffleButton.setIconSize(QSize(48,48))
        self.shuffleButton.setToolTip("Listeyi Karıştır")
        self.shuffleButton.clicked.connect(self.shufflePlayList)

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon("icons/previous.png"))
        self.previousButton.setIconSize(QSize(48, 48))
        self.previousButton.setToolTip("Önceki Parça")
        self.previousButton.clicked.connect(self.playPrevious)


        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon("icons/play.png"))
        self.playButton.setIconSize(QSize(64, 64))
        self.playButton.setToolTip("Oynat")
        self.playButton.clicked.connect(self.playSounds)
        
        

        self.nextButton = QToolButton()
        self.nextButton.setIcon(QIcon("icons/next.png"))
        self.nextButton.setIconSize(QSize(48, 48))
        self.nextButton.setToolTip("Sonraki Parça")
        self.nextButton.clicked.connect(self.playNext)


        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon("icons/mute.png"))
        self.muteButton.setIconSize(QSize(24, 24))
        self.muteButton.setToolTip("Sessiz")
        self.muteButton.clicked.connect(self.muteSound)
        
        self.addButton =QToolButton()
        self.addButton.setIcon(QIcon("icons/add.png"))
        self.addButton.setIconSize(QSize(48,48))
        self.addButton.setToolTip("Müzik ekle")
        self.addButton.clicked.connect(self.addSound)

        #####################Volume Slider#################
        self.volumeSlider=QSlider(Qt.Horizontal)
        self.volumeSlider.setToolTip("Ses")
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        ###################Play List####################
        self.playList=QListWidget()
        self.playList.doubleClicked.connect(self.playSounds)
        self.playList.setStyleSheet(style.playListStyle())

        #####################Timer######################
        self.timer=QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgressBar)
        
#######################################################kljhkjhkhkjh




    def layouts(self):
        #########################Creating Layouts#################
        self.mainLayout=QVBoxLayout()
        self.topMainLayout=QVBoxLayout()
        self.topGroupBox=QGroupBox("Müzik Çalar")
        self.topGroupBox.setStyleSheet(style.groupboxStyle())
        self.topLayout=QHBoxLayout()
        self.middleLayout=QHBoxLayout()
        self.bottomLayout=QVBoxLayout()

        ###################Adding Widgets#########################
        ##################Top layout widgets######################
        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLenthLabel)

        ##################Middle layout Widget#################
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.nextButton)
        self.middleLayout.addWidget(self.volumeSlider)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addWidget(self.addButton)

        self.middleLayout.addStretch()

        ###################Bottom layout widget#############
        self.bottomLayout.addWidget(self.playList)

        self.topMainLayout.addLayout(self.topLayout)
        self.topMainLayout.addLayout(self.middleLayout)
        self.topGroupBox.setLayout(self.topMainLayout)
        self.mainLayout.addWidget(self.topGroupBox,25)
        self.mainLayout.addLayout(self.bottomLayout,75)
        self.setLayout(self.mainLayout)

    def addSound(self):
        directory=QFileDialog.getOpenFileName(self,"Müzik Ekle","","Ses Dosyaları (*.mp3 *.ogg *.wav)")
        # print(directory)
        filename=os.path.basename(directory[0])
        # print(filename)
        self.playList.addItem(filename)
        musicList.append(directory[0])

    def shufflePlayList(self):
        random.shuffle(musicList)
        print(musicList)
        self.playList.clear()
        for song in musicList:
            filename=os.path.basename(song)
            self.playList.addItem(filename)

    def pause(self):
        random.shuffle(musicList)
        print(musicList)
        self.playList.clear()
        for song in musicList:
            filename=os.path.basename(song)
            self.playList.addItem(filename)


    def playSounds(self):
        global songLength
        global count
        global index
        count=0
        index=self.playList.currentRow()

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound=MP3(str(musicList[index]))
            songLength=sound.info.length
            songLength=round(songLength)
            print(songLength)
            min,sec=divmod(songLength,60)

            self.songLenthLabel.setText("/ "+str(min)+":"+str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def playPrevious(self):
        global songLength
        global count
        global index
        count = 0
        items=self.playList.count()

        if index == 0:
             index = items
        index -=1

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            songLength = sound.info.length
            songLength = round(songLength)
            print(songLength)
            min, sec = divmod(songLength, 60)

            self.songLenthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def playNext(self):
        global songLength
        global count
        global index
        count = 0
        items = self.playList.count()
        index += 1

        if index == items:
            index = 0


        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            songLength = sound.info.length
            songLength = round(songLength)
            print(songLength)
            min, sec = divmod(songLength, 60)

            self.songLenthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def setVolume(self):
        self.volume=self.volumeSlider.value()
        # print(self.volume)
        mixer.music.set_volume(self.volume/100)

    def muteSound(self):
        global muted

        if muted == False:
            mixer.music.set_volume(0.0)
            muted = True
            self.muteButton.setIcon(QIcon("icons/unmuted.png"))
            self.muteButton.setToolTip("Ses aç")
            self.volumeSlider.setValue(0)

        else:
            mixer.music.set_volume(0.7)
            muted = False
            self.muteButton.setToolTip("Sessiz")
            self.muteButton.setIcon(QIcon("icons/mute.png"))
            self.volumeSlider.setValue(70)

    def updateProgressBar(self):
        global count
        global songLength
        count +=1
        self.progressBar.setValue(count)
        self.songTimerLabel.setText(time.strftime("%M:%S",time.gmtime(count)))
        if count == songLength:
            self.timer.stop()



def main():
    App=QApplication(sys.argv)
    window=Player()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()