from PyQt5 import QtCore, QtGui, QtWidgets

import ProteinExtract
import os
import cv2
import csv
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directory = os.path.join(BASE_DIR, 'EclampsiaDetection')
#directory = BASE_DIR

print(directory)
class Ui_MainWindow(object):
    
    
    def clearCheck(self):
        
        print('Clear')
        
        self.motherName.setText("")
        self.highPressure.setText("")
        self.lowPressure.setText("")
        self.pregnancy.setText("")
        self.output.setText("")
        sys.exit()
        os.system('python3 CameraCapture.py')
    
    def diagnoseCheck(self):
        print('Login Button Pressed')
        name = self.motherName.text()
        high_pressure = self.highPressure.text()
        low_pressure = self.lowPressure.text()
        pregnancy_age = self.pregnancy.text()
        
        protein_value = ProteinExtract.imageExtract(directory)
        
        print('Name: ', name)
        print('High Pressure: ', high_pressure)
        print('Low Pressure: ', low_pressure)
        print('Age: ', pregnancy_age)
        print('Protein Value: ', protein_value)
        
        highpressureflag = 0
        lowpressureflag = 0
        pregnancyflag = 0
        
        if(name == '' or high_pressure == '' or low_pressure == '' or pregnancy_age == ''):
            message = 'Fill in the missing values'
            
        else:
            
            prot_float = float(protein_value)
            
            try:
                hpress_float = float(high_pressure)
                
                if(hpress_float < 250 and hpress_float > 100):   
                    highpressureflag = 1
                else:
                    message = 'High Pressure value out of range'
                
                try:
                    lpress_float = float(low_pressure)
                    
                    if(lpress_float < 250 and lpress_float > 30):   
                        lowpressureflag = 1
                    else:
                        message = 'Low Pressure value out of range'
                    
                    try:
                        preg_float = float(pregnancy_age)
                        
                        if(preg_float < 40 and preg_float > 1):   
                            pregnancyflag = 1
                        else:
                            message = 'Prgnancy age value out of range'
                        
                    except ValueError:
                        self.pregnancy.setText("")
                        message = 'Input a number value for pregnancy'
                        
                        
                except ValueError:
                    self.lowPressure.setText("")
                    message = 'Input a number value for low blood pressure'
                

            except ValueError:
                self.highPressure.setText("")
                message = 'Input a number value for high blood pressure'
            
        
        
               
            if(highpressureflag == 1 and lowpressureflag == 1 and pregnancyflag == 1):
            
            
                ##CODE FOR DIAGNOSIS 
                
                message = ''
                if(preg_float < 20):      
                    if(hpress_float > 140):
                        if(prot_float > 0.3):    
                            message = 'No preclampsia, but possible hypertension and kidney disease, confirmatory tests recommended'
                        else:
                            message = 'No preclampsia, but possible hypertension'
                    else:
                        if(prot_float > 0.3):    
                            message = 'No preclampsia, but possible kidney disease, confirmatory tests recommended'
                        else:
                            message = 'No preclampsia, or hypertension detected'
                
                else:
                    if(hpress_float > 140 and hpress_float < 160):
                        if(prot_float > 0.3):    
                            message = 'Mild preclampsia detected, confirmatory tests recommended'
                        else:
                            message = 'No preclampsia, but possible hypertension'
                    elif(hpress_float > 160):
                        if(prot_float > 0.3):    
                            message = 'Severe preclampsia detected'
                        else:
                            message = 'Severe hypertension detected'
                
                stored_message = message
                      
                    
                param_list = [name, hpress_float, lpress_float, preg_float, prot_float, stored_message]
                title_list = ['Name','High Blood Pressure', 'Low Blood Pressure', 'Preg Age', 'Protein Value', 'Result']
                
                
                
                
                csvpath = os.path.join(directory,'Data.csv')
                
                print('CSVPATH: ', csvpath)
                
                
                exists = os.path.isfile(csvpath)
                if exists:
                    with open(csvpath,'a') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(param_list)
                else:
                    with open(csvpath,'a') as csvfile: 
                        writer = csv.writer(csvfile)
                        writer.writerow(title_list)
                        writer.writerow(param_list)
        
        
        
        msg_len = len(message)
        print(msg_len)
        
        if(msg_len > 40 and msg_len < 80):
            final_message = message[0:41] + '\n' + message[41:] 
        
        elif(msg_len > 80):
            final_message = message[0:41] + '\n' + message[41:81] + '\n' + message[81:] 
            
        else:
            final_message = message     
        self.output.setText(final_message)
    
    
    def imageCheck(self):
        #print('Image Button Pressed')
        imagepath = os.path.join(directory,'images', 'testimage.jpg')
        
        img = cv2.imread(imagepath) 
        window_height = self.imageView.height()
        #print('Window Height', window_height)
        
        img_height = img.shape[0] 
        #print('Image Height', img_height)
        
        
        resize_factor = window_height/img_height
        #print(resize_factor)
        
        img = cv2.resize(img,None,fx=resize_factor, fy=resize_factor, interpolation = cv2.INTER_LINEAR)
        resizedimagepath = os.path.join(directory,'images', 'resizedimage.jpg')
        cv2.imwrite(resizedimagepath, img)
        
        
        image = QtGui.QImage(QtGui.QImageReader(resizedimagepath).read())
        self.imageView.setPixmap(QtGui.QPixmap(image))
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(682, 463)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.motherName = QtWidgets.QLineEdit(self.centralwidget)
        self.motherName.setGeometry(QtCore.QRect(210, 70, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.motherName.setFont(font)
        self.motherName.setText("")
        self.motherName.setObjectName("motherName")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 70, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pregnancy = QtWidgets.QLineEdit(self.centralwidget)
        self.pregnancy.setGeometry(QtCore.QRect(270, 120, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pregnancy.setFont(font)
        self.pregnancy.setText("")
        self.pregnancy.setObjectName("pregnancy")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 120, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.highPressure = QtWidgets.QLineEdit(self.centralwidget)
        self.highPressure.setGeometry(QtCore.QRect(270, 170, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.highPressure.setFont(font)
        self.highPressure.setText("")
        self.highPressure.setObjectName("highPressure")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 170, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lowPressure = QtWidgets.QLineEdit(self.centralwidget)
        self.lowPressure.setGeometry(QtCore.QRect(270, 220, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lowPressure.setFont(font)
        self.lowPressure.setText("")
        self.lowPressure.setObjectName("lowPressure")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 220, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 20, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.diagnoseButton = QtWidgets.QPushButton(self.centralwidget)
        self.diagnoseButton.setGeometry(QtCore.QRect(50, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.diagnoseButton.setFont(font)
        self.diagnoseButton.setObjectName("diagnoseButton")
        
        ##function calling for diagnose button########
        self.diagnoseButton.clicked.connect(self.diagnoseCheck)
        ##function calling for diagnose button########
        
        self.imageButton = QtWidgets.QPushButton(self.centralwidget)
        self.imageButton.setGeometry(QtCore.QRect(220, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.imageButton.setFont(font)
        self.imageButton.setObjectName("imageButton")
        
        ##function calling for diagnose button########
        self.imageButton.clicked.connect(self.imageCheck)
        ##function calling for diagnose button########
        
        self.output = QtWidgets.QLabel(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(50, 350, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.output.setFont(font)
        self.output.setText("")
        self.output.setObjectName("output")
        self.imageView = QtWidgets.QLabel(self.centralwidget)
        self.imageView.setGeometry(QtCore.QRect(460, 70, 111, 351))
        self.imageView.setText("")
        self.imageView.setObjectName("imageView")
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearBtn.setGeometry(QtCore.QRect(130, 310, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.clearBtn.setFont(font)
        self.clearBtn.setObjectName("clearBtn")
        
        ##function calling for diagnose button########
        self.clearBtn.clicked.connect(self.clearCheck)
        ##function calling for diagnose button########
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 682, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Preeclampsia Detection"))
        self.label.setText(_translate("MainWindow", "Mother\'s Name"))
        self.label_2.setText(_translate("MainWindow", "Age of Pregnancy"))
        self.label_3.setText(_translate("MainWindow", "Higher Blood Pressure"))
        self.label_4.setText(_translate("MainWindow", "Lower Blood Pressure"))
        self.label_5.setText(_translate("MainWindow", "Preeclampsia Smart Diagnosis System"))
        self.diagnoseButton.setText(_translate("MainWindow", "Diagnose"))
        self.imageButton.setText(_translate("MainWindow", "Load Image"))
        self.clearBtn.setText(_translate("MainWindow", "New Diagnosis"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
