import os
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import cv2
from statistics import mode

#from MainController import MainController


class quemada(QThread):
    mask = pyqtSignal("PyQt_PyObject")
    modded = pyqtSignal("PyQt_PyObject","PyQt_PyObject")
    pixeles = pyqtSignal(str,str,str,str)
    mediamoda = pyqtSignal(str,str,str,str)
    
    def __init__(self,imagesDir,appDir):
        QThread.__init__(self)
        self.hmin = 0
        self.hmax = 180
        self.smin = 0
        self.smax = 255
        self.vmin = 0
        self.vmax = 255
        self.brillo = 0
        self.kernel = 5
        self.sigma = 0
        self.xmin,self.ymin,self.xmax,self.ymax = 0,0,0,0
        self.appDir = appDir
        self.imagesDir = imagesDir
        self.image = sorted(os.listdir(self.appDir + self.imagesDir))[0]

        self.start()
        

    def setBrilloRoi(self,brillo,kernel,sigma,xmin,ymin,xmax,ymax):
        self.brillo,self.kernel,self.sigma = brillo, int(kernel), int(sigma)
        self.xmin,self.ymin,self.xmax,self.ymax = int(xmin),int(ymin),int(xmax),int(ymax)
        

    def setImage(self,image):
        self.image = image

    def setHSVRange(self,hmin,hmax,smin,smax,vmin,vmax):
        self.hmin = hmin
        self.hmax = hmax
        self.smin = smin
        self.smax = smax
        self.vmin = vmin
        self.vmax = vmax


    def run(self): 

        print("Brillo: " + str(self.brillo))
        
        imOriginal = cv2.imread(self.appDir + self.imagesDir + self.image)
        self.brillo = int(self.brillo)
        b, g, r = cv2.split(imOriginal)

        if (int(self.brillo) >= 0):
            lim = 255 - self.brillo
            b[b > lim] = 255
            b[b <= lim] += self.brillo
            g[g > lim] = 255
            g[g <= lim] += self.brillo
            r[r > lim] = 255
            r[r <= lim] += self.brillo
        else:
            brillo2 = abs(self.brillo)
            lim = 0 + brillo2
            b[b < lim] = 0
            b[b >= lim] -= brillo2
            g[g < lim] = 0
            g[g >= lim] -= brillo2
            r[r < lim] = 0
            r[r >= lim] -= brillo2


        bgr = cv2.merge((b, g, r))
        hsvOriginal = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        imOriginal = cv2.cvtColor(hsvOriginal, cv2.COLOR_HSV2RGB)

        #BLUR
        if self.kernel != 0:
            imOriginal = cv2.GaussianBlur(imOriginal,(self.kernel,self.kernel),self.sigma)
                   

        if self.ymax == 0 or self.xmax == 0:
            img = imOriginal.copy()
        else:
            try:
                img = imOriginal[self.ymin:self.ymax, self.xmin:self.xmax]
            except:
                print("ERROR: NO SE HA PODIDO COGER LA REGION")
                img = imOriginal.copy()

        
        porc, hsv = self.HSV(img,hsvOriginal)
        
        
        value_s = []
        _,s,v = cv2.split(hsv)
        
        for i in s:
            for x in i:
                value_s.append(x)
        
        value_v = []
        #_,_,v = cv2.split(hsv)
        for i in v:
            for x in i:
                value_v.append(x)
        
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            fm = int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var())
        except:
            pass
        
        imRectanle = cv2.rectangle(imOriginal.copy(),(self.xmin,self.ymin),(self.xmax,self.ymax),(255,255,0),4)
        
        self.imMod = imOriginal.copy()

        self.modded.emit(imRectanle,imOriginal)
        self.mediamoda.emit(str(round(np.mean(value_s),2)),str(round(mode(value_s),2)),str(round(np.mean(value_v),2)),str(round(mode(value_v),2)))
        self.pixeles.emit(str(hsv.shape[0] * hsv.shape[1]), str(round(porc)),str(100-round(porc)),str(fm))



    def HSV(self,img,hsvOriginal):
        try:
            if hsvOriginal == None:
                im = cv2.imread(self.appDir + self.imagesDir + self.image)
                self.brillo = int(self.brillo)
                b, g, r = cv2.split(im)

                if (int(self.brillo) >= 0):
                    lim = 255 - self.brillo
                    b[b > lim] = 255
                    b[b <= lim] += self.brillo
                    g[g > lim] = 255
                    g[g <= lim] += self.brillo
                    r[r > lim] = 255
                    r[r <= lim] += self.brillo
                else:
                    brillo2 = abs(self.brillo)
                    lim = 0 + brillo2
                    b[b < lim] = 0
                    b[b >= lim] -= brillo2
                    g[g < lim] = 0
                    g[g >= lim] -= brillo2
                    r[r < lim] = 0
                    r[r >= lim] -= brillo2


                bgr = cv2.merge((b, g, r))
                hsvOriginal = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        except:
            pass

        low_white = np.array([self.hmin, self.smin, self.vmin])
        high_white = np.array([self.hmax, self.smax, self.vmax])

        white_maskOriginal = cv2.inRange(hsvOriginal, low_white, high_white)
        


        #Porcentaje en el que se redimensiona la imagen
        scale_percent = 50
        
        #calcular el 50 por ciento de las dimensiones originales
        width = int(white_maskOriginal.shape[1] * scale_percent / 100)
        height = int(white_maskOriginal.shape[0] * scale_percent / 100)
        
        # dsize
        dsize = (width, height)
        
        # cambiar el tamaño de la image
        output = cv2.resize(white_maskOriginal, dsize)

        

        try:
            if img == None:
                img = self.imMod.copy()
            
        except:
            pass

        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        white_mask = cv2.inRange(hsv, low_white, high_white)
        white = np.sum(white_mask == 255)
        
        negros = np.sum(white_mask == 0)

        # Porcentaje de pixeles que no estan quemados
        porc = (round(negros / (white_mask.shape[0] * white_mask.shape[1])*100,2))

        print("-----------------")
        print("IMAGEN: " + str(self.image))
        print("NEGROS: " + str(negros))
        print("BLANCOS: " + str(white))
        print("PORCENTAJE: ", porc)
        print("-----------------\n")

        self.mask.emit(output)

        return porc, hsv