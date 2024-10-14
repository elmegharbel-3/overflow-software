from PyQt5.QtWidgets import *
import time
import serial.tools.list_ports
import pygame
app = QApplication([])
window = QWidget()
window.setWindowTitle("Final Project")
layout = QGridLayout()
# title
title = QLabel("Team Two")
layout.addWidget(title,0,1)
# Select the ports 
portList =[port.device for port in serial.tools.list_ports.comports()]
ports = QComboBox()
ports.addItems(portList)
layout.addWidget(ports,1,0)
# Select the serial
serialPort = QLineEdit()
layout.addWidget(serialPort,1,1)
# update arduino data button 
updatebtn = QPushButton("update")
layout.addWidget(updatebtn,1,2)
# Read the serial of arduino
def updateArduino():
    usbPort = ports.currentText()
    serialValue = serialPort.text()
    print(usbPort,serialValue)
    global serialCom
    serialCom = serial.Serial(usbPort,int(serialValue))
    pygame.init()
    screen = pygame.display.set_mode((300,400)) 
    i = 0
    while True:
        i+=1
        irValue.setText(str(i))
        events = pygame.event.get()
        """ irValue.setText(num) """
        """ num = serialCom.read() """
        # Pygame to close and control system
        for e in events:
            if e.type == pygame.KEYDOWN:
            # choose to control motots manually
                if chr(e.key) == "c":
                    if controlCb.isChecked() == False:
                        controlCb.setChecked(True)
                        print("You can control manually")
                    else:
                        controlCb.setChecked(False) 
                        print("You can't control manually")
                # change motor state
                elif chr(e.key) == "o" and controlCb.isChecked() == True:   
                    if changeMotor.isChecked() == False:
                        changeMotor.setChecked(True)
                        print("Motor is ON")
                    else:
                        changeMotor.setChecked(False)
                        print("Motor is OFF")
                # Close system with keyboard and exit btn and break loop
                elif  e.key == 27:
                    pygame.quit()
                    break
            elif e.type == pygame.QUIT:
                pygame.quit()
                break
updatebtn.clicked.connect(updateArduino)
# header for the ir
headState = QLabel("IR sensor reads:")
layout.addWidget(headState,2,0)
# the reading of IR
irValue = QLabel("High")
layout.addWidget(irValue,3,0)
# button to control motors manually
headControl = QLabel("Control motors manually:")
layout.addWidget(headControl,2,2)
controlCb = QCheckBox()
layout.addWidget(controlCb,3,2)
# Change motor state
headMotor = QLabel("Turn Motor on/off:")
layout.addWidget(headMotor,4,2)
headMotor.setHidden(True)
changeMotor = QCheckBox()
layout.addWidget(changeMotor,5,2)
changeMotor.setHidden(True)
motorState = QLabel("Motor is off")
layout.addWidget(motorState,6,2)
# function to control motors manually
def onOff():
    if changeMotor.isChecked()==True:
        motorState.setText("Motor is on")
        """ serialCom.write((bytearray('motor on','ascii'))) """
    else:
        motorState.setText("Motor is off")
        """ serialCom.write((bytearray('motor off','ascii'))) """
changeMotor.toggled.connect(onOff)
motorState.setHidden(True)
# show the controls of motor with checkboxe
def showMotor():
    if controlCb.isChecked() == True:
        headMotor.setHidden(False)
        changeMotor.setHidden(False)
        motorState.setHidden(False)
    else: 
        headMotor.setHidden(True)
        changeMotor.setChecked(False)
        changeMotor.setHidden(True)
        motorState.setHidden(True)
        """ serialCom.write((bytearray('control auto','ascii'))) """
controlCb.toggled.connect(showMotor)        
# set layout
window.setLayout(layout)
# window showing
window.show()
app.exec()
    