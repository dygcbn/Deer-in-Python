import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt,QTimer
import random,time
from pygame import mixer
from mutagen.mp3 import MP3



muzikList=[]
mixer.init()
muted=False
sayac=0
parcauzunluk=0
index=0




class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müzik Çalar")
        self.setGeometry(450,180,750,700)
        self.show()
        self.widgets()
        self.layouts()

    

    def widgets(self):
        ########################progress bar#############
        self.progressBar=QProgressBar()
        self.progressBar.setStyleSheet("""
        QProgressBar {
        border: 1px solid #bbb;
        background: white;
        height: 10px;
        border-radius: 6px;     
        }
    """)

        self.parcauzunluk=QLabel("0:00")
        self.parcalabel=QLabel("/ 0:00")
        #######################Butonlar###################
        self.ekle =QToolButton()
        self.ekle.setIcon(QIcon("butonlar/ekle.png"))
        self.ekle.setIconSize(QSize(48,48))
        self.ekle.setToolTip("Müzik Ekle")
        self.ekle.clicked.connect(self.sesekle)

        self.butonkaristir=QToolButton()
        self.butonkaristir.setIcon(QIcon("butonlar/karistir.png"))
        self.butonkaristir.setIconSize(QSize(48,48))
        self.butonkaristir.setToolTip("Listeyi Karıştır")
        self.butonkaristir.clicked.connect(self.listekaristir)

        self.oncekiparca = QToolButton()
        self.oncekiparca.setIcon(QIcon("butonlar/onceki.png"))
        self.oncekiparca.setIconSize(QSize(48, 48))
        self.oncekiparca.setToolTip("Önceki Parça")
        self.oncekiparca.clicked.connect(self.oncekinical)


        self.oynat = QToolButton()
        self.oynat.setIcon(QIcon("butonlar/play.png"))
        self.oynat.setIconSize(QSize(64, 64))
        self.oynat.setToolTip("Oynat")
        self.oynat.clicked.connect(self.seslerical)
        

        self.sonrakiparca = QToolButton()
        self.sonrakiparca.setIcon(QIcon("butonlar/sonraki.png"))
        self.sonrakiparca.setIconSize(QSize(48, 48))
        self.sonrakiparca.setToolTip("Sonraki Parça")
        self.sonrakiparca.clicked.connect(self.sonrakinical)


        self.sessiz = QToolButton()
        self.sessiz.setIcon(QIcon("butonlar/mute.png"))
        self.sessiz.setIconSize(QSize(24, 24))
        self.sessiz.setToolTip("Sessiz")
        self.sessiz.clicked.connect(self.sesikapat)
        
        self.muzikekle =QToolButton()
        self.muzikekle.setIcon(QIcon("butonlar/ekle.png"))
        self.muzikekle.setIconSize(QSize(48,48))
        self.muzikekle.setToolTip("Müzik ekle")
        self.muzikekle.clicked.connect(self.sesekle)

        #####################ses Slider#################
        self.sesslider=QSlider(Qt.Horizontal)
        self.sesslider.setToolTip("Ses")
        self.sesslider.setValue(70)
        self.sesslider.setMinimum(0)
        self.sesslider.setMaximum(100)

        self.sesslider.valueChanged.connect(self.sesayarla)

        ###################oynatma Listesi####################
        self.oynatmalistesi=QListWidget()
        self.oynatmalistesi.doubleClicked.connect(self.seslerical)
        self.oynatmalistesi.setStyleSheet("""
        QListWidget{
        background-color:#fff;
        border-radius: 10px;
        border:3px solid blue;     
        }
    """)

        #####################zamanlayıcı######################
        self.timer=QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.progressbarguncelle)
        




    def layouts(self):
        #########################başlık#################
        self.anapencere=QVBoxLayout()
        self.anapencere2=QVBoxLayout()
        
        self.penceregrup=QGroupBox("Müzik Çalar")
        self.penceregrup.setStyleSheet("""
        QGroupBox {
        background-color:#acc324;
        font:15pt Times Bold;
        color:white;
        border:2px solid gray;
        border-radius:15px;
        }
    """)
        self.ustkutu=QHBoxLayout()
        self.ortakutu=QHBoxLayout()
        self.altkutu=QVBoxLayout()

        ###################Widget ekle#########################
        ##################tepe######################
        self.ustkutu.addWidget(self.progressBar)
        self.ustkutu.addWidget(self.parcauzunluk)
        self.ustkutu.addWidget(self.parcalabel)

        ##################orta#################
        self.ortakutu.addStretch()
        self.ortakutu.addWidget(self.muzikekle)
        self.ortakutu.addWidget(self.butonkaristir)
        self.ortakutu.addWidget(self.oynat)
        self.ortakutu.addWidget(self.oncekiparca)
        self.ortakutu.addWidget(self.sonrakiparca)
        self.ortakutu.addWidget(self.sesslider)
        self.ortakutu.addWidget(self.sessiz)


        self.ortakutu.addStretch()

        ###################alt#############
        self.altkutu.addWidget(self.oynatmalistesi)

        self.anapencere.addLayout(self.ustkutu)
        self.anapencere.addLayout(self.ortakutu)
        self.penceregrup.setLayout(self.anapencere)
        self.anapencere2.addWidget(self.penceregrup,25)
        self.anapencere2.addLayout(self.altkutu,75)
        self.setLayout(self.anapencere2)

    def sesekle(self):
        klasor=QFileDialog.getOpenFileName(self,"Müzik Ekle","","Ses Dosyaları (*.mp3 *.ogg *.wav)")
        dosya=os.path.basename(klasor[0])
        self.oynatmalistesi.addItem(dosya)
        muzikList.append(klasor[0])

    def listekaristir(self):
        random.shuffle(muzikList)
        print(muzikList)
        self.oynatmalistesi.clear()
        for parca in muzikList:
            dosya=os.path.basename(parca)
            self.oynatmalistesi.addItem(dosya)



    def seslerical(self):
        global parcauzunluk
        global sayac
        global index
        sayac=0
        index=self.oynatmalistesi.currentRow()

        try:
            mixer.music.load(str(muzikList[index]))
            mixer.music.play()
            self.timer.start()
            sound=MP3(str(muzikList[index]))
            parcauzunluk=sound.info.length
            parcauzunluk=round(parcauzunluk)
            print(parcauzunluk)
            min,sec=divmod(parcauzunluk,60)

            self.parcalabel.setText("/ "+str(min)+":"+str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(parcauzunluk)

        except:
            pass

    def oncekinical(self):
        global parcauzunluk
        global sayac
        global index
        sayac = 0
        ogeler=self.oynatmalistesi.count()

        if index == 0:
             index = ogeler
        index -=1

        try:
            mixer.music.load(str(muzikList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(muzikList[index]))
            parcauzunluk = sound.info.length
            parcauzunluk = round(parcauzunluk)
            print(parcauzunluk)
            min, sec = divmod(parcauzunluk, 60)

            self.parcalabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(parcauzunluk)
        except:
            pass

    def sonrakinical(self):
        global parcauzunluk
        global sayac
        global index
        sayac = 0
        ogeler = self.oynatmalistesi.count()
        index += 1

        if index == ogeler:
            index = 0


        try:
            mixer.music.load(str(muzikList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(muzikList[index]))
            parcauzunluk = sound.info.length
            parcauzunluk = round(parcauzunluk)
            print(parcauzunluk)
            min, sec = divmod(parcauzunluk, 60)

            self.parcalabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(parcauzunluk)
        except:
            pass

    def sesayarla(self):
        self.sesayari=self.sesslider.value()
        mixer.music.set_volume(self.sesayari/100)

    def sesikapat(self):
        global muted

        if muted == False:
            mixer.music.set_volume(0.0)
            muted = True
            self.sessiz.setIcon(QIcon("butonlar/unmuted.png"))
            self.sessiz.setToolTip("Ses aç")
            self.sesslider.setValue(0)

        else:
            mixer.music.set_volume(0.7)
            muted = False
            self.sessiz.setToolTip("Sessiz")
            self.sessiz.setIcon(QIcon("butonlar/mute.png"))
            self.sesslider.setValue(70)

    def progressbarguncelle(self):
        global sayac
        global parcauzunluk
        sayac +=1
        self.progressBar.setValue(sayac)
        self.parcauzunluk.setText(time.strftime("%M:%S",time.gmtime(sayac)))

        if sayac == parcauzunluk:
            self.timer.stop()




App=QApplication(sys.argv)
pencere=Player()
sys.exit(App.exec_())
