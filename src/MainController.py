import cv2
import os, cv2
from PyQt5.QtCore import  QObject
from ClassQuemada import quemada
from classCheckRangeDia import checkRangeDia
from classCheckRangeNoche import checkRangeNoche
from classCheckRangeIr import checkRangeIr
from classCheckRangeBlur import checkRangeBlur


class MainController(QObject):
    

    def __init__(self,imagesDirHSV,imagesDirProcess,appDir):
        super(QObject, self).__init__()
        self.imagesDirHSV = imagesDirHSV
        self.imagesDirProcess = imagesDirProcess
        self.appDir = appDir

        # Parte comprobacion HSV
        self.quemado = quemada(self.imagesDirHSV,self.appDir)
        
        self.images = sorted(os.listdir(self.appDir + self.imagesDirHSV))
        self.numImages = len(self.images)
        print("Numero imagenes: " + str(self.numImages))
        self.actualImage = 0

        # Parte procesados

        self.controlRangoDia = checkRangeDia(self.imagesDirProcess,self.appDir)
        self.controlRangoNoche = checkRangeNoche(self.imagesDirProcess,self.appDir)
        self.controlRangoIr = checkRangeIr(self.imagesDirProcess,self.appDir)
        self.controlRangoBlur = checkRangeBlur(self.imagesDirProcess,self.appDir)



        return


    # Funciones Procesados

    def iniciarComprobacionDia(self,xmin,ymin,xmax,ymax,brillo):
        self.controlRangoDia.Roi(xmin,ymin,xmax,ymax,brillo)

    def iniciarComprobacionNoche(self,xmin,ymin,xmax,ymax,brillo):
        self.controlRangoNoche.Roi(xmin,ymin,xmax,ymax,brillo)

    def iniciarComprobacionIr(self,xmin,ymin,xmax,ymax,brillo):
        self.controlRangoIr.Roi(xmin,ymin,xmax,ymax,brillo)

    def iniciarComprobacionBlur(self,xmin,ymin,xmax,ymax,kernel):
        self.controlRangoBlur.Roi(xmin,ymin,xmax,ymax,kernel)


    # Funciones comprobación HSV

    def InicioQuemada(self,brillo,kernel,sigma,xmin,ymin,xmax,ymax):
        if (int(kernel) %2 ==0) and (int(kernel) != 0):
            print("El kernel debe ser impar")
        else:
            self.quemado.setBrilloRoi(brillo,kernel,sigma,xmin,ymin,xmax,ymax)


    def cambiarImg(self,imagen):
        self.quemado.setImage(imagen)

    def imageMenos(self):
        if self.actualImage == 0:
            self.actualImage = self.numImages - 1
        else:
            self.actualImage = self.actualImage - 1
        self.cambiarImg(self.images[self.actualImage])
        

    def imageMas(self):
        if self.actualImage == self.numImages - 1:
            self.actualImage = 0
        else:
            self.actualImage = self.actualImage + 1
        self.cambiarImg(self.images[self.actualImage])
        
    
    def guardarImgQuemada(self,lineEdit_brillo,kernelBlur,moddedQuemada):
        self.moddedQuemada2 = cv2.cvtColor(moddedQuemada,cv2.COLOR_BGR2RGB)
        cv2.imwrite(self.appDir + "../IMG-OUT/" + f"Bri{lineEdit_brillo}_KerBlur_{kernelBlur}" + str(self.images[self.actualImage]),self.moddedQuemada2)
        print("Imagen modificada guardada")
