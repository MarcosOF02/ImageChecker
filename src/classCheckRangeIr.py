import  os
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import cv2
from statistics import mode,median
from PyQt5.QtGui import  QPixmap
import qimage2ndarray

class checkRangeIr(QThread):
    valoresNormalesIr = pyqtSignal(str,str,str,str,str,str,str,str,str)
    valoresQuemadaIr = pyqtSignal(str,str,str,str,str,str,str,str,QPixmap)
    valoresBlurredIr = pyqtSignal(str)
   

    def __init__(self, imagesDir,appDir):
        QThread.__init__(self)

        self.appDir = appDir
        self.imagesDir = imagesDir + "ir/"
        self.work = True
        

    def Roi(self,xmin,ymin,xmax,ymax,brillo):
        self.xmin,self.ymin,self.xmax,self.ymax,self.brillo = int(xmin),int(ymin),int(xmax),int(ymax),int(brillo)
        try:
            self.imageList = sorted(os.listdir(self.appDir + self.imagesDir))
            self.work = True
        except:
            print("ERROR::INFRARROJO::DIRECTORIO DE IMAGENES NO EXISTE")
            self.work = False
        self.start()
    
    def run(self):
        if self.work:
            self.valoresBase()
            self.valoresBrilloMod()
            self.valoresBlurMod()


    def valoresBase(self):
        
        media_s,moda_s,media_v,moda_v,medmod_s,medmod_v,max_s,max_v,fm = [],[],[],[],[],[],[],[],[]

        for i in range(len(self.imageList)):
            
            print(f"INFO::BASE::INFRAROJO::PROCESANDO: {self.imageList[i]}")

            imOriginal = cv2.imread(self.appDir + self.imagesDir + self.imageList[i])

            hsvOriginal = cv2.cvtColor(imOriginal, cv2.COLOR_BGR2HSV)
            imOriginal = cv2.cvtColor(hsvOriginal, cv2.COLOR_HSV2RGB)
            
            img = imOriginal[self.ymin:self.ymax, self.xmin:self.xmax]
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            
            value_s = []
            _,s,v = cv2.split(hsv)
            
            for z in s:
                for x in z:
                    value_s.append(x)
            
            value_v = []
            _,_,v = cv2.split(hsv)
            for z in v:
                for x in z:
                    value_v.append(x)
            
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                fm.append(round(int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var())))
            
            except:
                pass


            media_s.append(round(np.mean(value_s)))
            moda_s.append(round(mode(value_s)))
            media_v.append(round(np.mean(value_v)))
            moda_v.append(round(mode(value_v)))
            medmod_v.append(round((int(media_v[i]) + int(moda_v[i]))) / 2)
            medmod_s.append(round((int(media_s[i]) + int(moda_s[i]))) / 2)
            max_v.append(round(np.max(value_v)))
            max_s.append(round(np.max(value_s)))


        hsvimage = cv2.imread(self.appDir + "hsvcone.png")
        hsvimage = cv2.cvtColor(hsvimage,cv2.COLOR_BGR2RGB)
        coordenadax_min = int(((min(media_s) * 180) / 51)) + 144
        coordenaday_min = int(1022 - ((min(media_v) * 180) / 51))

        coordenadax_max = int(((max(media_s) * 180) / 51)) + 144
        coordenaday_max = int(1022 - ((max(media_v) * 180) / 51))

        cv2.rectangle(hsvimage,(coordenadax_min,coordenaday_min),(coordenadax_max,coordenaday_max),(0,0,255),3)
        cv2.putText(hsvimage,f"S: {min(media_s)} V: {max(media_v)}",(coordenadax_min,coordenaday_max - 10),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2)
        cv2.putText(hsvimage,f"S: {max(media_s)} V: {min(media_v)}",(coordenadax_max + 10,coordenaday_min),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2)
        
        self.hsvimage = hsvimage


        media_s = str(round(median(media_s)))
        moda_s = str(round(median(moda_s)))
        media_v = str(round(median(media_v)))
        moda_v = str(round(median(moda_v)))
        medmod_s = str(round(median(medmod_s)))
        medmod_v = str(round(median(medmod_v)))
        max_v = str(round(median(max_v)))
        max_s = str(round(median(max_s)))
        fm = str(round(median(fm)))


        self.valoresNormalesIr.emit(media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm)


    def valoresBrilloMod(self):

        media_s,moda_s,media_v,moda_v,medmod_s,medmod_v,max_s,max_v = [],[],[],[],[],[],[],[]

        for i in range(len(self.imageList)):
            print(f"INFO::BRILLOMOD::INFRAROJO::PROCESANDO: {self.imageList[i]}")

            imOriginal = cv2.imread(self.appDir + self.imagesDir + self.imageList[i])
            
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
            
            img = imOriginal[self.ymin:self.ymax, self.xmin:self.xmax]
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            
            value_s = []
            _,s,v = cv2.split(hsv)
            
            for z in s:
                for x in z:
                    value_s.append(x)
            
            value_v = []
            _,_,v = cv2.split(hsv)
            for z in v:
                for x in z:
                    value_v.append(x)
            
            
            media_s.append(round(np.mean(value_s)))
            moda_s.append(round(mode(value_s)))
            media_v.append(round(np.mean(value_v)))
            moda_v.append(round(mode(value_v)))
            medmod_v.append(round((int(media_v[i]) + int(moda_v[i]))) / 2)
            medmod_s.append(round((int(media_s[i]) + int(moda_s[i]))) / 2)
            max_v.append(round(np.max(value_v)))
            max_s.append(round(np.max(value_s)))

            if not (os.path.isdir("../IMG-OUT/ir/brillo/")):
                os.makedirs("../IMG-OUT/ir/brillo/")

            cv2.imwrite("../IMG-OUT/ir/brillo/" + self.imageList[i], cv2.putText(cv2.cvtColor(imOriginal, cv2.COLOR_BGR2RGB),f"S(media): {media_s[-1]} V(media): {media_v[-1]} Brillo: {self.brillo}",(imOriginal.shape[1]- 400,(imOriginal.shape[0]-30)),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2)) 
        
        coordenadax_min = int(((min(media_s) * 180) / 51)) + 144
        coordenaday_min = int(1022 - ((min(media_v) * 180) / 51))

        coordenadax_max = int(((max(media_s) * 180) / 51)) + 144
        coordenaday_max = int(1022 - ((max(media_v) * 180) / 51))

        cv2.rectangle(self.hsvimage,(coordenadax_min,coordenaday_min),(coordenadax_max,coordenaday_max),(252, 231, 3),3)
        cv2.putText(self.hsvimage,f"S: {min(media_s)} V: {max(media_v)}",(coordenadax_min,coordenaday_max - 10),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2)
        cv2.putText(self.hsvimage,f"S: {max(media_s)} V: {min(media_v)}",(coordenadax_max + 10,coordenaday_min),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2)

        hsvimage = QPixmap.fromImage(qimage2ndarray.array2qimage(self.hsvimage))

        media_s = str(round(median(media_s)))
        moda_s = str(round(median(moda_s)))
        media_v = str(round(median(media_v)))
        moda_v = str(round(median(moda_v)))
        medmod_s = str(round(median(medmod_s)))
        medmod_v = str(round(median(medmod_v)))
        max_v = str(round(median(max_v)))
        max_s = str(round(median(max_s)))

        self.valoresQuemadaIr.emit(media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,hsvimage)



    def valoresBlurMod(self):
        
        fm = []

        for i in range(len(self.imageList)):

            print(f"BLUR:: PROCESANDO: {self.imageList[i]}")

            imOriginal = cv2.imread(self.appDir + self.imagesDir + self.imageList[i])

            hsvOriginal = cv2.cvtColor(imOriginal, cv2.COLOR_BGR2HSV)
            imOriginal = cv2.cvtColor(hsvOriginal, cv2.COLOR_HSV2RGB)

            #BLUR
            imOriginal = cv2.GaussianBlur(imOriginal,(23,23),0)

            
            img = imOriginal[self.ymin:self.ymax, self.xmin:self.xmax]
            
            
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


            if not (os.path.isdir("../IMG-OUT/ir/blur/")):
                os.makedirs("../IMG-OUT/ir/blur/")

            cv2.imwrite("../IMG-OUT/ir/blur/" + self.imageList[i], cv2.putText(cv2.cvtColor(imOriginal, cv2.COLOR_BGR2RGB),f"fm: {round(int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var()))}",(imOriginal.shape[1]- 220,(imOriginal.shape[0]-30)),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2))

            fm.append(round(int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var())))


        fm = str(round(np.mean(fm)))

        self.valoresBlurredIr.emit(fm)

            
            


