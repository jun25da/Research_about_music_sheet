import os
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from pathlib import Path
from PyQt5.QtGui import QPixmap
import processing
import window


LOWER = False

#============================  class 설정 부분  ========================================
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('muti_window_test.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass( QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.setWindowTitle("music sheet")
        self.page=[]
        self.Label=[]
        self.fname =[]
        
        self.file_number = 1
        
        self.note_frequency = []
        self.note_length = []
        
        self.constract = False
#==========================  Signal & Setting 부분  =======================================

#--------------------  QStackedWidget객체 Setting 부분  -----------------------------------
    #StackedWidget 만들기
        self.setFixedSize(QSize(600, 916))
        # QStackedWidget 생성
        self.stack = QStackedWidget(self)                   # QStackedWidget 생성
        self.stack.setGeometry(0,0,600,850) # 위치 및 크기 지정
        self.stack.setFrameShape(QFrame.Box)                # 테두리 설정(보기 쉽게)

        # 입력할 page를 QWidget으로 생성
    
        self.page.append(QWidget(self))    # page_1 생성
        
    
        self.markLabel = QLabel(self.page[0])
        self.markLabel.setParent(self.page[0])
        self.markLabel.setGeometry(60, 100, 800, 600)
        self.markLabel.setText("악보 만드는 프로그램")
        self.markLabel.setFont(QtGui.QFont("궁서",30))
        self.markLabel.setStyleSheet("Color : green")


        self.markLabel.show()
        
        
        self.pic = QLabel(self.page[0])
        self.pic.setParent(self.page[0])
        self.pic.setGeometry(233, 180, 150, 150)
        self.pic.setPixmap(QPixmap("C:/python1/R&E/final/광.webp"))
        
        self.pic.show()
        
        self.statusBar()
        
        
        self.openFile = QPushButton('파일 선택', self.page[0])
        self.openFile.move(375, 570)
        self.openFile.clicked.connect(self.showDialog)
        
        self.textEdit = QTextEdit(self.page[0])
        self.textEdit.setGeometry(140,600,220,53)
        self.textEdit.setText("아직 파일이 추출되지 않았습니다.")
        

        self.btn = QPushButton('추출 시작', self.page[0])
        self.btn.move(375, 600)
        self.btn.clicked.connect(self.doAction)

        self.btn1 = QPushButton('악보 출력', self.page[0])
        self.btn1.move(375, 630)
        self.btn1.clicked.connect(self.fnc_btn_complete)

        self.btn2 = QPushButton("홈으로", self)
        self.btn2.move(0, 860)
        self.btn2.clicked.connect(self.fnc_btn_return)
        
        self.btn3 = QPushButton("저장", self)
        self.btn3.move(420, 860)
        self.btn3.clicked.connect(self.cap_btn_return)
        
        
        self.btn_forward = QPushButton("<-", self)
        self.btn_forward.move(100,860)
        self.btn_forward.clicked.connect(self.fnc_btn_forward)
        
        self.btn_backward = QPushButton("->", self)
        self.btn_backward.move(200,860)
        self.btn_backward.clicked.connect(self.fnc_btn_backward)
        
        
        
        
        self.n = 20
        
        self.stack.addWidget(self.page[0])
            
            
#--------------------------------------------------------------------------------------------------------------

        # setCurrentIndex / setCurrentWidget [페이지 전환]
        self.btn_forward.clicked.connect(self.fnc_btn_forward)          
        self.btn_backward.clicked.connect(self.fnc_btn_backward)
              
        
#===============================  Slot 부분   ==================================================================
    def fnc_btn_forward(self):
        if self.stack.currentIndex() == 1 or self.stack.currentIndex() == 0:
            pass
        else:
            self.stack.setCurrentWidget(self.page[self.stack.currentIndex()-1])                       

    def fnc_btn_backward(self):
        if self.stack.currentIndex() == 0:
            pass
        else:
            if not self.stack.currentIndex()==self.stack.count()-1:
                
                self.stack.setCurrentWidget(self.page[self.stack.currentIndex()+1])
                
    def fnc_btn_complete(self):
        if self.constract == True:
            
            self.stack.setCurrentWidget(self.page[self.stack.currentIndex()+1])
    
    def cap_btn_return(self):
        if self.stack.currentIndex() == 0:
            pass
            
        else:
            index = self.fname[0].rindex("/")
            file_name = self.fname[0][index+1:] + f"{self.file_number}"
            capture = window.WindowCapture("music sheet", file_name )
            frame = capture.screenshot()
            self.file_number += 1
            
            self.statusBar().showMessage(f"{file_name}이 저장되었습니다.")
           
            
            
        
        return
    
    def fnc_btn_return(self):
        if self.stack.currentIndex() == 0:
            pass
        else:
            for i in range(self.n+1):
                self.stack.removeWidget(self.page[i+1]) 
            self.fname =[]
            self.file_number = 0
            self.textEdit.setText("아직 파일이 추출되지 않았습니다.")
            self.btn.setText('추출 시작')
            self.statusBar().showMessage("")
            self.n=10
            self.stack.setCurrentWidget(self.page[self.stack.currentIndex()*0])
        
        
#===================================================================== 

    def doAction(self):

            if self.fname == []:
                self.textEdit.setText("아직 파일이 추출되지 않았습니다.")
                
            else:
                
                self.note_frequency , self.note_length =  processing.main(self.fname[0])
                
                LOWER = high_low(self.note_frequency)
                
                
                for i in range(self.n):
            
                    self.page.append(QWidget(self))
                    self.Label.append(QLabel(self.page[i+1]))
                    self.Label[i].setParent(self.page[i+1])
                    self.Label[i].setGeometry(0,0,600,850)
                    self.Label[i].setText(f'label_{i+1}')
                    if not LOWER: # 음자리표 결정
                        self.Label[i].setPixmap(QPixmap('C:/python1/R&E/final/sheeet/sheet_high.png'))
                    else:
                        self.Label[i].setPixmap(QPixmap('C:/python1/R&E/final/sheeet/sheet_low.png'))
            
                
                    
                
                if not LOWER:
                    pitch = return_pitch_high(self.note_frequency)
                elif LOWER:
                    pitch = return_pitch_low(self.note_frequency)
                    self
                
                self.n = len(self.note_length)//90
                self.note_frequency = list_chunk(self.note_frequency , 90)
                self.note_length = list_chunk(self.note_length , 90)
                pitch = list_chunk(pitch , 90)
                
            
                for i in range(self.n+1):
                    
                    self.draw_notes(self.note_frequency[self.n], pitch[self.n], self.note_length[self.n], label_index=self.n)
                    self.extra_lines(pitch[self.n], label_index=self.n)
                
                for i in range(self.n+1):
                    self.stack.addWidget(self.page[i+1])
                
                self.textEdit.setText(self.fname[0])
                self.btn.setText('추출 완료')
                self.constract = True
                
                return
                
    def showDialog(self):

        home_dir = str(Path.home())
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        self.textEdit.setText(self.fname[0])

#================================ 악보 출력 부분 ===============================================
    def draw_notes(self, notes_result, pitch_list, length_result, label_index): # 조표 추가까지
        notes = notes_result
        pitch = pitch_list
        length = length_result
        for N in range(len(notes)):
            if pitch[N] >= 8:
                self.note = QPixmap(f'C:/python1/R&E/final/sheeet/note_2_{int(length[N]*100)}.png')
                self.lab_note = QLabel(self.page[label_index+1])
                self.lab_note.setParent(self.page[label_index+1])
                self.lab_note.setGeometry(80 + (50 * N) - (500*(N//10)), (75 * (N//10)) + 127 -(pitch[N]), 22, 31) # 450
                self.lab_note.setPixmap(self.note)
                self.lab_note.show()
                
            else:
                self.note = QPixmap(f'C:/python1/R&E/final/sheeet/note_1_{int(length[N]*100)}.png')
                self.lab_note = QLabel(self.page[label_index+1])
                self.lab_note.setParent(self.page[label_index+1])
                self.lab_note.setGeometry(80 + (50 * N) - (500*(N//10)), (75 * (N//10)) +  107-(pitch[N]), 22, 31) # 450
                self.lab_note.setPixmap(self.note)
                self.lab_note.show()
            
            if len(notes[N]) == 3: # 조표(샵)
                self.note = QPixmap('C:/python1/R&E/final/sheeet/sharp.png')
                self.lab_note = QLabel(self.page[label_index+1])
                self.lab_note.setParent(self.page[label_index+1])
                self.lab_note.setGeometry(70 + (50 * N) - (500*(N//10)), (75 * (N//10)) +  118 -(pitch[N]), 11, 29) # 450
                self.lab_note.setPixmap(self.note)
                self.lab_note.show()
                
    
        

    def extra_lines(self, pitch_list, label_index): # 추가 선
        extra_file="C:/python1/R&E/final/sheeet/extra_1.png"
        pitch = pitch_list
        for N in range(len(pitch)):
            if pitch[N] >= 32:
                num = pitch[N]
                fix = 0
                if abs(num) % 8 == 0:
                    while num >= 32:
                        self.note = QPixmap(extra_file)
                        self.lab_note = QLabel(self.page[label_index+1])
                        self.lab_note.setParent(self.page[label_index+1])
                        self.lab_note.setGeometry(80 + (50 * N) - (500*(N//10)), (75 * (N//10)) + 107 -(pitch[N]) + fix, 22, 31) # 450
                        self.lab_note.setPixmap(self.note)
                        self.lab_note.show()
                       
                        num -= 4
                        fix += 8
                else:
                    while num >= 32:
                        self.note = QPixmap(extra_file)
                        self.lab_note = QLabel(self.page[label_index+1])
                        self.lab_note.setParent(self.page[label_index+1])
                        self.lab_note.setGeometry(80 + (50 * N) - (500*(N//10)), (75 * (N//10)) + 110 -(pitch[N]) - fix, 22, 31) # 450
                        self.lab_note.setPixmap(self.note)
                        self.lab_note.show()
                        
                        num -= 5
                        fix += 16
                        
            elif pitch[N] <= -16:
                num = pitch[N]
                fix = 0
                if abs(num) % 8 == 0:
                    while num <= -16:
                        self.note = QPixmap(extra_file)
                        self.lab_note = QLabel(self.page[label_index+1])
                        self.lab_note.setParent(self.page[label_index+1])
                        self.lab_note.setGeometry(80 + (50 * N) - (500*(N//10)), (75 * (N//10)) + 107 -(pitch[N]) + fix, 22, 31) # 450
                        self.lab_note.setPixmap(self.note)
                        self.lab_note.show()
                        num += 4
                        fix -= 8
                else:
                    while num <= -16:
                        self.note = QPixmap(extra_file)
                        self.lab_note = QLabel(self.page[label_index+1])
                        self.lab_note.setParent(self.page[label_index+1])
                        self.lab_note.setGeometry(80 + (50 * N) - (500*(N//10)), (75 * (N//10)) + 103 -(pitch[N]) + fix, 22, 31) # 450
                        self.lab_note.setPixmap(self.note)
                        self.lab_note.show()
                        num += 4
                        fix -= 8


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


def high_low(freguency):
    high = 0
    low = 0
    
    for i in freguency:
        if len(i)==2:
            number = int(i[1])
        else:
            number = int(i[2])
            
        if  number>=4:
            high+=1
        else:
            low += 1
    
        
    if high>=low:
        return False
    else:
        return True


def return_pitch_high(notes_result): # 음에 따라 줄 높이 보정값 반환 (높은음자리표)
        pitch_list = []
        notes = notes_result
        for note in notes:
            if note[-1] == '4':
                if note[0] == "c":
                    pitch_list.append(-16)
                elif note[0] == "d":
                    pitch_list.append(-12)
                elif note[0] == "e":
                     pitch_list.append(-8)
                elif note[0] == "f":
                     pitch_list.append(-4)
                elif note[0] == "g":
                     pitch_list.append(0)
                elif note[0] == "a":
                     pitch_list.append(4)
                elif note[0] == "b":
                     pitch_list.append(8)

            elif note[-1] == '3':
                if note[0] == "c":
                    pitch_list.append(-44)
                elif note[0] == "d":
                    pitch_list.append(-40)
                elif note[0] == "e":
                     pitch_list.append(-36)
                elif note[0] == "f":
                     pitch_list.append(-32)
                elif note[0] == "g":
                     pitch_list.append(-28)
                elif note[0] == "a":
                     pitch_list.append(-24)
                elif note[0] == "b":
                     pitch_list.append(-20)

            elif note[-1] == '5':
                if note[0] == "c":
                    pitch_list.append(12)
                elif note[0] == "d":
                    pitch_list.append(16)
                elif note[0] == "e":
                     pitch_list.append(20)
                elif note[0] == "f":
                     pitch_list.append(24)
                elif note[0] == "g":
                     pitch_list.append(28)
                elif note[0] == "a":
                     pitch_list.append(32)
                elif note[0] == "b":
                     pitch_list.append(36)

            elif int(note[-1]) >= 6:
                pitch_list.append(36)

            elif int(note[-1]) <= 2:
                pitch_list.append(-44)

        return pitch_list
    
def return_pitch_low(notes_result): # 음에 따라 줄 높이 보정값 반환 (낮은음자리표)
        pitch_list = []
        notes = notes_result
        for note in notes:
            if note[-1] == '3':
                if note[0] == "c":
                    pitch_list.append(-16)
                elif note[0] == "d":
                    pitch_list.append(-12)
                elif note[0] == "e":
                     pitch_list.append(-8)
                elif note[0] == "f":
                     pitch_list.append(-4)
                elif note[0] == "g":
                     pitch_list.append(0)
                elif note[0] == "a":
                     pitch_list.append(4)
                elif note[0] == "b":
                     pitch_list.append(8)

            elif note[-1] == '2':
                if note[0] == "c":
                    pitch_list.append(-44)
                elif note[0] == "d":
                    pitch_list.append(-40)
                elif note[0] == "e":
                     pitch_list.append(-36)
                elif note[0] == "f":
                     pitch_list.append(-32)
                elif note[0] == "g":
                     pitch_list.append(-28)
                elif note[0] == "a":
                     pitch_list.append(-24)
                elif note[0] == "b":
                     pitch_list.append(-20)

            elif note[-1] == '3':
                if note[0] == "c":
                    pitch_list.append(12)
                elif note[0] == "d":
                    pitch_list.append(16)
                elif note[0] == "e":
                     pitch_list.append(20)
                elif note[0] == "f":
                     pitch_list.append(24)
                elif note[0] == "g":
                     pitch_list.append(28)
                elif note[0] == "a":
                     pitch_list.append(32)
                elif note[0] == "b":
                     pitch_list.append(36)

            elif int(note[-1]) >= 4:
                pitch_list.append(36)

            elif int(note[-1]) <= 1:
                pitch_list.append(-44)

        return pitch_list






#==============================  app 실행 부분  =================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )