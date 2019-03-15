# Import PySide classes
import sys
from Morphing import *
from PySide.QtCore import *
from PySide.QtGui import *
import numpy as np
from PIL import Image
from PIL import ImageDraw
from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline
from scipy.ndimage.interpolation import map_coordinates
import matplotlib.pyplot as plt
from matplotlib.cm import gray as bw
from MorphingGUI import *
from os import path



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.horizontalSlider.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.Triangle1 = []
        self.Triangle2 = []
        self.startLabel = QtGui.QLabel()
        self.endLabel = QtGui.QLabel()
        self.myFunc()
        self.horizontalSlider.valueChanged.connect(self.Change)
        self.pushButton_3.clicked.connect(self.Blend)
        self.click1F = 0
        self.click2F = 0
        self.savePoint = 0
        self.firstP = 0
        self.OutPress = 0
        self.LastPoint = 0
        self.BackF1 = 0
        self.BackF2 = 0
        self.Green = 0
        self.Blue1 = 0
        self.Blue2 = 0
        self.Exist1 = 0
        self.Exist2 = 0
        self.Triangle1Orig = [[]]
        self.Triangle2Orig = [[]]
        with open("temp1.txt", "w") as temp1:
            self.Tpoint1 = "temp1.txt"
            temp1.close()
        with open("temp2.txt", "w") as temp2:
            self.Tpoint2 = "temp2.txt"
            temp2.close()
        self.centralWidget = QtGui.QMainWindow
        self.keyPressEvent = self.BackSpace

    def BackSpace(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            if self.LastPoint == 1:
                self.Green = 0
                self.BackF1 = 1
                with open(self.Tpoint1, "w") as TFile:
                    TFile.write("")
                TFile.close()
                a = plt.figure(frameon=False)
                a.add_axes([0,0,1,1])
                plt.axis("off")
                if len(self.Image1.shape) == 2:
                    plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0], cmap=bw)
                else:
                    plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0])
                if self.Exist1 == 1:
                    plt.plot(self.Triangle1Orig[0], self.Triangle1Orig[1],"o", color="red", linewidth=4, markeredgecolor='red')
                    plt.savefig("New2.png")
                    plt.close()
                    self.Scene = QtGui.QPixmap("New2.png")
                    self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    label = QtGui.QLabel(self.graphicsView)
                    label.setPixmap(self.Scene)
                    label.show()
                    self.click2F = 0
                    self.click1F = 1
                    self.LastPoint = 2
                    self.ShowTri()



                if os.stat(self.IM1Name).st_size != 0:
                    line = np.loadtxt(self.IM1Name)
                    self.Triangle1 = line
                    if self.firstP == 1:
                        if len(self.Triangle1) > 2:
                            plt.plot(self.Triangle1[:,0], self.Triangle1[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                        elif isinstance(self.Triangle1[0], np.ndarray):
                            plt.plot(self.Triangle1[0][0], self.Triangle1[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                            plt.plot(self.Triangle1[1][0], self.Triangle1[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                        else:
                            plt.plot(self.Triangle1[0], self.Triangle1[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                    plt.savefig("New1.png")
                    plt.close()
                    self.Scene = QtGui.QPixmap("New1.png")
                    self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    label = QtGui.QLabel(self.graphicsView)
                    label.setPixmap(self.Scene)
                    label.show()
                    self.click2F = 0
                    self.click1F = 1
                    self.LastPoint = 2
                    self.ShowTri()

                    self.click1F = 1
                    label.mousePressEvent = self.mouseClick1
                elif self.Exist1 == 1:
                    plt.plot(self.Triangle1Orig[0], self.Triangle1Orig[1],"o", color="red", linewidth=4, markeredgecolor='red')
                    plt.savefig("New1.png")
                    plt.close()
                    self.Scene = QtGui.QPixmap("New1.png")
                    self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    label = QtGui.QLabel(self.graphicsView)
                    label.setPixmap(self.Scene)
                    label.show()
                    self.ShowTri()
                    self.click1F = 1
                    label.mousePressEvent = self.mouseClick1

                else:
                    self.firstP = 0
                    self.loadDataFromFile1(str(self.IM1Name).replace(".txt", ""))

            elif self.LastPoint == 2:
                self.Green = 1
                self.BackF2 = 1
                with open(self.Tpoint2, "w") as TFile:
                    TFile.write("")
                TFile.close()
                a = plt.figure(frameon=False)
                a.add_axes([0,0,1,1])
                plt.axis("off")
                if len(self.Image2.shape) == 2:
                    plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0], cmap=bw)
                else:
                    plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0])
                if self.Exist2 == 1:
                    print("HERE")
                    plt.plot(self.Triangle2Orig[0], self.Triangle2Orig[1],"o", color="red", linewidth=4, markeredgecolor='red')
                    plt.savefig("New2.png")
                    plt.close()
                    self.Scene2 = QtGui.QPixmap("New2.png")
                    self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    label = QtGui.QLabel(self.graphicsView_2)
                    label.setPixmap(self.Scene2)
                    label.show()
                    self.click2F = 1
                    self.click1F = 0
                    self.LastPoint = 1
                    self.ShowTri()

                elif os.stat(self.IM2Name).st_size != 0:
                    line = np.loadtxt(self.IM2Name)
                    self.Triangle2 = line
                    if self.firstP == 1:
                        if len(self.Triangle2) > 2:
                            plt.plot(self.Triangle2[:,0], self.Triangle2[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                        elif isinstance(self.Triangle2[0], np.ndarray):
                            plt.plot(self.Triangle2[0][0], self.Triangle2[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                            plt.plot(self.Triangle2[1][0], self.Triangle2[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                        else:
                            plt.plot(self.Triangle2[0], self.Triangle2[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                    plt.savefig("New2.png")
                    plt.close()
                    self.Scene2 = QtGui.QPixmap("New2.png")
                    self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    label = QtGui.QLabel(self.graphicsView_2)
                    label.setPixmap(self.Scene2)
                    label.show()
                    self.click2F = 1
                    self.click1F = 0
                    self.LastPoint = 1
                    self.ShowTri()
                    self.click2F = 1
                    label.mousePressEvent = self.mouseClick2

                else:
                    self.firstP = 0
                    self.loadDataFromFile2(str(self.IM2Name).replace(".txt", ""))


    def Central(self, event):
        if self.savePoint == 1 and self.BackF1 == 0 and self.BackF2 == 0 and self.Green == 2:
            self.Green = 0
            self.OutPress = 1
            self.ShowBlue1()
            self.ShowBlue2()
            self.firstP = 1
            label = QtGui.QLabel(self.graphicsView)
            label.setPixmap(self.Scene)
            label.show()
            self.ShowTri()
            label.mousePressEvent = self.mouseClick1

    def ShowBlue1(self):
        print("Blue")
        Line = np.loadtxt(self.Tpoint1)
        with open(self.IM1Name, "a") as Tile2:
            Tile2.write("\n" + str(Line[0]) + "   " + str(Line[1]))
            Tile2.close()
        if self.Exist1 == 1:
            with open("tempBlue.txt", "a") as File1:
                File1.write("\n" + str(Line[0]) + "    " + str(Line[1]))
                File1.close()
        if self.Exist1 == 1:
            self.Triangle1 = np.loadtxt("tempBlue.txt")
        else:
            self.Triangle1 = np.loadtxt(self.IM1Name)
        self.Check()
        a = plt.figure(frameon=False)
        a.add_axes([0, 0, 1, 1])
        plt.axis("off")
        if len(self.Image1.shape) == 2:
            plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0], cmap=bw)
        else:
            plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0])
        if isinstance(self.Triangle1[0], np.ndarray):
            plt.plot(self.Triangle1[:, 0], self.Triangle1[:, 1], "o", color="blue", linewidth=4, markeredgecolor='blue')
        else:
            plt.plot(self.Triangle1[0], self.Triangle1[1], "o", color="blue", linewidth=4, markeredgecolor='blue')
        plt.savefig("New1.png")
        plt.close()
        self.Scene = QtGui.QPixmap("New1.png")
        self.Scene = self.Scene.scaled(291,211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        label = QtGui.QLabel(self.graphicsView)
        label.setPixmap(self.Scene)
        label.show()
        self.startLabel = label

    def ShowBlue2(self):
        print("BLUE2")
        Line = np.loadtxt(self.Tpoint2)
        with open(self.IM2Name, "a") as Tile2:
            Tile2.write("\n" + str(Line[0]) + "   " + str(Line[1]))
            Tile2.close()
        if self.Exist2 == 1:
            with open("tempBlue2.txt", "a") as File1:
                File1.write("\n" + str(Line[0]) + "    " + str(Line[1]))
                File1.close()
        if self.Exist2 == 1:
            self.Triangle2 = np.loadtxt("tempBlue2.txt")
        else:
            self.Triangle2 = np.loadtxt(self.IM2Name)
        self.Check()
        a = plt.figure(frameon=False)
        a.add_axes([0, 0, 1, 1])
        plt.axis("off")
        if len(self.Image2.shape) == 2:
            plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0], cmap=bw)
        else:
            plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0])
        if isinstance(self.Triangle2[0], np.ndarray):
            plt.plot(self.Triangle2[:, 0], self.Triangle2[:, 1], "o", color="blue", linewidth=4, markeredgecolor='blue')
        else:
            plt.plot(self.Triangle2[0], self.Triangle2[1], "o", color="blue", linewidth=4, markeredgecolor='blue')
        plt.savefig("New2.png")
        plt.close()
        self.Scene2 = QtGui.QPixmap("New2.png")
        self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        label = QtGui.QLabel(self.graphicsView_2)
        label.setPixmap(self.Scene2)
        label.show()
        self.ShowTri()
        self.endLabel = label


    def mouseClick1(self, event):
        print("MouseClick")
        if self.savePoint == 1 and self.OutPress == 0 and self.BackF1 == 0 and self.BackF2 == 0:
            self.ShowBlue1()
            self.ShowBlue2()
            self.firstP = 1

        if self.click1F == 1:
            self.OutPress = 0
            self.Image1X = np.round(event.x() * self.Image1.shape[1]/291)
            self.Image1Y = np.round(event.y() * self.Image1.shape[0]/211)
            with open(self.Tpoint1, "w") as TFile:
                TFile.write(str(self.Image1X) + "   " + str(self.Image1Y) + "\n")
            TFile.close()
            line = np.loadtxt(self.Tpoint1)
            Triangle1 = line
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image1.shape) == 2:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0])
            plt.plot(Triangle1[0], Triangle1[1],"o", color = "green", markeredgecolor='green')
            self.Green = 1
            if self.firstP == 1:
                if len(self.Triangle1) > 2:
                    plt.plot(self.Triangle1[:,0], self.Triangle1[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                elif isinstance(self.Triangle1[0], np.ndarray):
                    plt.plot(self.Triangle1[0][0], self.Triangle1[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                    plt.plot(self.Triangle1[1][0], self.Triangle1[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                else:
                    plt.plot(self.Triangle1[0], self.Triangle1[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
            plt.savefig("New1.png")
            plt.close()
            self.Scene = QtGui.QPixmap("New1.png")
            self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView)
            label.setPixmap(self.Scene)
            label.show()
            self.LastPoint = 1

            self.click2F = 1
            label2 = QtGui.QLabel(self.graphicsView_2)
            label2.setPixmap(self.Scene2)
            label2.show()
            self.click1F = 0
            self.ShowTri()
            label2.mousePressEvent = self.mouseClick2
            self.savePoint = 0

    def mouseClick2(self, event):
        print("MouseClick2")
        if self.click2F == 1:
            self.Image2X = np.round(event.x() * self.Image2.shape[1]/291)
            self.Image2Y = np.round(event.y() * self.Image2.shape[0]/211)
            with open(self.Tpoint2, "w") as TFile:
                TFile.write(str(self.Image2X) + "   " + str(self.Image2Y) + "\n")
            TFile.close()
            line = np.loadtxt(self.Tpoint2)
            Triangle2 = line
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image2.shape) == 2:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0])
            plt.plot(Triangle2[0], Triangle2[1],"o", color = "green", markeredgecolor='green')
            self.Green = 2
            if self.firstP == 1:
                if len(self.Triangle2) > 2:
                    plt.plot(self.Triangle2[:,0], self.Triangle2[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                elif isinstance(self.Triangle2[0], np.ndarray):
                    plt.plot(self.Triangle2[0][0], self.Triangle2[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                    plt.plot(self.Triangle2[1][0], self.Triangle2[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                else:
                    plt.plot(self.Triangle2[0], self.Triangle2[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
            plt.savefig("New2.png")
            plt.close()
            self.Scene2 = QtGui.QPixmap("New2.png")
            self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView_2)
            label.setPixmap(self.Scene2)
            label.show()
            self.LastPoint = 2

            self.click1F = 1
            label2 = QtGui.QLabel(self.graphicsView)
            label2.setPixmap(self.Scene)
            label2.show()
            self.ShowTri()
            self.click2F = 0
            self.savePoint = 1
            self.centralWidget.mousePressEvent = self.Central
            if self.BackF1 == 1:
                self.BackF1 = 0
            if self.BackF2 == 0:
                label2.mousePressEvent = self.mouseClick1
            else:
                self.BackF2 = 0;

    def Blend(self):
        if self.Blue1 == 1:
            startPoint = self.Triangle1
        elif self.Exist1 == 1:
            if np.any(self.Triangle1):
                if isinstance(self.Triangle2[0], np.ndarray):
                    startPoint = np.append(self.Triangle2Orig, self.Triangle2, axis = 0)
                else:
                    startPoint = np.append(self.Triangle1Orig, [self.Triangle1], axis = 0)
            else:
                startPoint = self.Triangle1Orig

        if self.Blue2 == 1:
            endPoint = self.Triangle2
        elif self.Exist1 == 1:
            if np.any(self.Triangle2):
                if isinstance(self.Triangle2[0], np.ndarray):
                    endPoint = np.append(self.Triangle2Orig, self.Triangle2, axis = 0)
                else:
                    endPoint = np.append(self.Triangle2Orig, [self.Triangle2], axis = 0)
            else:
                endPoint = self.Triangle2Orig
        startImage = self.Image1
        endImage = self.Image2

        if len(self.Image1.shape) == 2:
            blend = Blender(startImage, startPoint, endImage, endPoint)
            A = blend.getBlendedImage(self.horizontalSlider.value()/20)
        else:
            blend = ColorBlender(startImage, startPoint, endImage, endPoint)
            A = blend.getBlendedImage(self.horizontalSlider.value()/20)

        Image.fromarray(A).save("New1.png")
        self.Scene = QtGui.QPixmap("New1.png")
        self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        label = QtGui.QLabel(self.graphicsView_3)
        label.setPixmap(self.Scene)
        label.show()

    def Change(self):
        self.lineEdit.setText(str(self.horizontalSlider.value()/20))

    def Check(self):
        if np.any(self.Triangle1) and np.any(self.Triangle2) or (np.any(self.Triangle1Orig) and np.any(self.Triangle2Orig)):
            self.horizontalSlider.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.checkBox.setEnabled(True)

    def myFunc(self):
        self.pushButton.clicked.connect(self.loadData1)
        self.pushButton_2.clicked.connect(self.loadData2)
        self.checkBox.stateChanged.connect(self.ShowTri)

    def ShowTri(self):
        if self.checkBox.isChecked() and ((len(self.Triangle1) > 2 and len(self.Triangle2) > 2)or (len(self.Triangle1Orig) > 2 and len(self.Triangle2Orig) > 2)):
            if np.any(self.Triangle1Orig) and np.any(self.Triangle1):
                if isinstance(self.Triangle1[0], np.ndarray):
                    Super = np.append(self.Triangle1Orig, self.Triangle1, axis = 0)
                else:
                    Super = np.append(self.Triangle1Orig, [self.Triangle1], axis = 0)
                self.tri1 = Delaunay(Super)
            elif np.any(self.Triangle1):
                self.tri1 = Delaunay(self.Triangle1)
                Super = self.Triangle1
            else:
                self.tri1 = Delaunay(self.Triangle1Orig)
                Super = self.Triangle1Orig
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image1.shape) == 2:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0])
            if self.Blue1 == 1:
                plt.triplot(self.Triangle1[:, 0], self.Triangle1[:, 1], self.tri1.simplices.copy(), color = "blue", linewidth=2)
                plt.plot(self.Triangle1[:,0], self.Triangle1[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')



            elif self.Exist1 == 1:
                with np.errstate(invalid="ignore"):
                    plt.triplot(Super[:,0], Super[:,1], self.tri1.simplices.copy(), color="cyan", linewidth=2)
                if self.firstP == 1:
                    if len(self.Triangle1) > 2:
                        plt.plot(self.Triangle1[:,0], self.Triangle1[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                    elif isinstance(self.Triangle1[0], np.ndarray):
                        plt.plot(self.Triangle1[0][0], self.Triangle1[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                        plt.plot(self.Triangle1[1][0], self.Triangle1[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                    else:
                        plt.plot(self.Triangle1[0], self.Triangle1[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                plt.plot(self.Triangle1Orig[:,0], self.Triangle1Orig[:,1],"o", color="red", linewidth=4, markeredgecolor='red')



            else:
                with np.errstate(invalid="ignore"):
                    plt.triplot(self.Triangle1Orig[:, 0], self.Triangle1Orig[:, 1], self.tri1.simplices.copy(), color = "red", linewidth=2)
                plt.plot(self.Triangle1Orig[:,0], self.Triangle1Orig[:,1],"o", color="red", linewidth=4, markeredgecolor='red')
            if self.Green == 1 or self.Green == 2:
                line = np.loadtxt(self.Tpoint1)
                plt.plot(line[0], line[1],"o", color="green", linewidth=4, markeredgecolor='green')
            plt.savefig("New1.png")
            plt.close()
            self.Scene = QtGui.QPixmap("New1.png")
            self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView)
            label.setPixmap(self.Scene)
            label.show()
#TRIANGLE 2
            if np.any(self.Triangle2Orig) and np.any(self.Triangle2):
                if isinstance(self.Triangle2[0], np.ndarray):
                    Super = np.append(self.Triangle2Orig, self.Triangle2, axis = 0)
                else:
                    Super = np.append(self.Triangle2Orig, [self.Triangle2], axis = 0)
                self.tri2 = Delaunay(Super)
            elif np.any(self.Triangle2):
                self.tri2 = Delaunay(self.Triangle2)
                Super = self.Triangle2
            else:
                self.tri2 = Delaunay(self.Triangle2Orig)
                Super = self.Triangle2Orig
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image2.shape) == 2:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0])
            if self.Blue2 == 1:
                plt.triplot(self.Triangle2[:, 0], self.Triangle2[:, 1], self.tri2.simplices.copy(), color = "blue", linewidth=2)
                plt.plot(self.Triangle2[:,0], self.Triangle2[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
            elif self.Exist2 == 1:
                plt.triplot(Super[:,0], Super[:,1], self.tri2.simplices.copy(), color="cyan", linewidth=2)
                if self.firstP == 1:
                    if len(self.Triangle2) > 2:
                        plt.plot(self.Triangle2[:,0], self.Triangle2[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                    elif isinstance(self.Triangle2[0], np.ndarray):
                        plt.plot(self.Triangle2[0][0], self.Triangle2[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                        plt.plot(self.Triangle2[1][0], self.Triangle2[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                    else:
                        plt.plot(self.Triangle2[0], self.Triangle2[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                plt.plot(self.Triangle2Orig[:,0], self.Triangle2Orig[:,1],"o", color="red", linewidth=4, markeredgecolor='red')



            else:
                plt.triplot(self.Triangle2Orig[:, 0], self.Triangle2Orig[:, 1], self.tri2.simplices.copy(), color = "red", linewidth=2)
                plt.plot(self.Triangle2Orig[:,0], self.Triangle2Orig[:,1],"o", color="red", linewidth=4, markeredgecolor='red')
            if self.Green == 2:
                line = np.loadtxt(self.Tpoint2)
                plt.plot(line[0], line[1],"o", color="green", linewidth=4, markeredgecolor='green')

            plt.savefig("New1.png")
            plt.close()
            self.Scene2 = QtGui.QPixmap("New1.png")
            self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label2 = QtGui.QLabel(self.graphicsView_2)
            label2.setPixmap(self.Scene2)
            label2.show()
            if self.LastPoint == 2:
                label.mousePressEvent = self.mouseClick1
            elif self.LastPoint == 1:
                label2.mousePressEvent = self.mouseClick2
            else:
                label.mousePressEvent = self.mouseClick1
#NO TRIANGLE
        elif (len(self.Triangle1) > 2 and len(self.Triangle2) > 2) or (len(self.Triangle1Orig) > 2 and len(self.Triangle2Orig) > 2):
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image1.shape) == 2:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0])
            if self.Blue1 == 1:
                plt.plot(self.Triangle1[:,0], self.Triangle1[:,1],"o", color = "blue", markeredgecolor='blue')
            elif self.Exist1 == 1:
                plt.plot(self.Triangle1Orig[:,0], self.Triangle1Orig[:,1],"o", color = "red", markeredgecolor='red')
                if self.firstP == 1:
                    if len(self.Triangle1) > 2:
                        plt.plot(self.Triangle1[:,0], self.Triangle1[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                    elif isinstance(self.Triangle1[0], np.ndarray):
                        plt.plot(self.Triangle1[0][0], self.Triangle1[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                        plt.plot(self.Triangle1[1][0], self.Triangle1[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                    else:
                        plt.plot(self.Triangle1[0], self.Triangle1[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
            else:
                plt.plot(self.Triangle1Orig[:,0], self.Triangle1Orig[:,1],"o", color = "red", markeredgecolor='red')
            if self.Green == 1 or self.Green == 2:
                line = np.loadtxt(self.Tpoint1)
                plt.plot(line[0], line[1],"o", color="green", linewidth=4, markeredgecolor='green')
            plt.savefig("New1.png")
            plt.close()
            self.Scene = QtGui.QPixmap("New1.png")
            self.Scene = self.Scene.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView)
            label.setPixmap(self.Scene)
            label.show()

#TRI2 NO TRIANGLE
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image2.shape) == 2:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0])
            if self.Blue2 == 1:
                plt.plot(self.Triangle2[:,0], self.Triangle2[:,1],"o", color = "blue", markeredgecolor='blue')
            elif self.Exist2 == 1:
                plt.plot(self.Triangle2Orig[:,0], self.Triangle2Orig[:,1],"o", color = "red", markeredgecolor='red')
                if self.firstP == 1:
                    if len(self.Triangle2) > 2:
                        plt.plot(self.Triangle2[:,0], self.Triangle2[:,1],"o", color="blue", linewidth=4, markeredgecolor='blue')
                    elif isinstance(self.Triangle2[0], np.ndarray):
                        plt.plot(self.Triangle2[0][0], self.Triangle2[0][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                        plt.plot(self.Triangle2[1][0], self.Triangle2[1][1], "o", color = "blue", linewidth =4, markeredgecolor='blue')
                    else:
                        plt.plot(self.Triangle2[0], self.Triangle2[1],"o", color="blue", linewidth=4, markeredgecolor='blue')
            else:
                plt.plot(self.Triangle2Orig[:,0], self.Triangle2Orig[:,1],"o", color = "red", markeredgecolor='red')
            if self.Green == 2:
                line = np.loadtxt(self.Tpoint2)
                plt.plot(line[0], line[1],"o", color="green", linewidth=4, markeredgecolor='green')
            plt.savefig("New1.png")
            plt.close()
            self.Scene2 = QtGui.QPixmap("New1.png")
            self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label2 = QtGui.QLabel(self.graphicsView_2)
            label2.setPixmap(self.Scene2)
            label2.show()
            if self.LastPoint == 2:
                label.mousePressEvent = self.mouseClick1
            elif self.LastPoint == 1:
                label2.mousePressEvent = self.mouseClick2


    def loadDataFromFile1(self, Thingy):
        self.Image1 = imageio.imread(Thingy)
        if os.path.exists('{}.txt'.format(Thingy)) and os.stat('{}.txt'.format(Thingy)).st_size != 0:
            line = np.loadtxt('{}.txt'.format(Thingy))
            with open('{}.txt'.format(Thingy)) as f:
                with open("tempred1.txt", "w") as f1:
                    f1.writelines(f.readlines())
            with open("tempBlue.txt", "w") as File1:
                File1.close()
            f.close()
            f1.close()
            self.IM1Name = '{}.txt'.format(Thingy)
            self.Triangle1Orig = line
            self.Exist1 = 1
            self.Check()
            self.tri1 = Delaunay(self.Triangle1Orig)
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image1.shape) == 2:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image1, extent=[0, self.Image1.shape[1], self.Image1.shape[0], 0])
            plt.plot(self.Triangle1Orig[:,0], self.Triangle1Orig[:,1],"o", color="red", linewidth=4, markeredgecolor='red')
            plt.savefig("New1.png")
            plt.close()
            self.Scene = QtGui.QPixmap("New1.png")
            self.Scene = self.Scene.scaled(291,211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView)
            label.setPixmap(self.Scene)
            label.show()
            self.click1F = 1
            label.mousePressEvent = self.mouseClick1
            self.startLabel = label
        else:
            self.Blue1 = 1
            with open('{}.txt'.format(Thingy), 'w') as IM1TXT:
                IM1TXT.close()
            self.IM1Name = '{}.txt'.format(Thingy)
            self.Triangle1 = []
            self.Scene = QtGui.QPixmap('{}'.format(Thingy))
            self.Scene = self.Scene.scaled(291,211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView)
            label.setPixmap(self.Scene)
            label.show()
            self.click1F = 1
            label.mousePressEvent = self.mouseClick1
            self.startLabel = label

    def loadData1(self):
            filePath, _ = QFileDialog.getOpenFileName(self, caption='Open Image file ...', filter="(*.png *.jpg)")
            if not filePath:
                return
            self.loadDataFromFile1(filePath)

    def loadDataFromFile2(self, Thingy):
        self.Image2 = imageio.imread(Thingy)
        if os.path.exists('{}.txt'.format(Thingy)) and os.stat('{}.txt'.format(Thingy)).st_size != 0:
            line = np.loadtxt('{}.txt'.format(Thingy))
            with open('{}.txt'.format(Thingy)) as f:
                with open("tempred2.txt", "w") as f1:
                    f1.writelines(f.readlines())
            with open("tempBlue2.txt", "w") as File1:
                File1.close()
            f.close()
            f1.close()
            self.IM2Name = '{}.txt'.format(Thingy)
            self.Triangle2Orig = line
            self.Exist2 = 1
            self.Check()
            self.tri2 = Delaunay(self.Triangle2Orig)
            a = plt.figure(frameon=False)
            a.add_axes([0,0,1,1])
            plt.axis("off")
            if len(self.Image2.shape) == 2:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0], cmap=bw)
            else:
                plt.imshow(self.Image2, extent=[0, self.Image2.shape[1], self.Image2.shape[0], 0])
            plt.plot(self.Triangle2Orig[:,0], self.Triangle2Orig[:,1],"o", color = "red", markeredgecolor='red')
            plt.savefig("New1.png")
            plt.close()
            self.Scene2 = QtGui.QPixmap("New1.png")
            self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView_2)
            label.setPixmap(self.Scene2)
            label.show()
            self.endLabel = label
        else:
            self.Blue2 = 1
            with open('{}.txt'.format(Thingy), 'w') as IM2TXT:
                IM2TXT.close()
            self.IM2Name = '{}.txt'.format(Thingy)
            self.Triangle2 = []
            self.Scene2 = QtGui.QPixmap('{}'.format(Thingy))
            self.Scene2 = self.Scene2.scaled(291, 211, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            label = QtGui.QLabel(self.graphicsView_2)
            label.setPixmap(self.Scene2)
            label.show()
            self.click2F = 1
            if self.BackF2 == 1:
                label.mousePressEvent = self.mouseClick2
            self.endLabel = label

    def loadData2(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open Image file ...', filter="(*.png *.jpg)")
        if not filePath:
            return
        self.loadDataFromFile2(filePath)

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MainWindow()

    currentForm.show()
    currentApp.exec_()



