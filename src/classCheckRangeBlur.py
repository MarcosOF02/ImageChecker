import  os
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import cv2
import qimage2ndarray

class checkRangeBlur(QThread):
    valoresBlurredB = pyqtSignal(str,str)
   

    def __init__(self, imagesDir,appDir):
        QThread.__init__(self)

        self.appDir = appDir
        self.imagesDir = imagesDir + "blur/"
        self.work = True
        

    def Roi(self,xmin,ymin,xmax,ymax,kernel):
        self.xmin,self.ymin,self.xmax,self.ymax,self.kernel = int(xmin),int(ymin),int(xmax),int(ymax),int(kernel)
        try:
            self.imageList = sorted(os.listdir(self.appDir + self.imagesDir))
            self.work = True
        except:
            print("ERROR::BLUR::DIRECTORIO DE IMAGENES NO EXISTE")
            self.work = False
        self.start()
    
    def run(self):
        if self.work:
            self.valoresBlurMod()


    def valoresBlurMod(self):
        
        fm,fmMod = [],[]

        for i in range(len(self.imageList)):

            print(f"INFO::BLUR::PROCESANDO: {self.imageList[i]}")

            imOriginal = cv2.imread(self.appDir + self.imagesDir + self.imageList[i])

            hsvOriginal = cv2.cvtColor(imOriginal, cv2.COLOR_BGR2HSV)
            imOriginal = cv2.cvtColor(hsvOriginal, cv2.COLOR_HSV2RGB)
            
            img = imOriginal[self.ymin:self.ymax, self.xmin:self.xmax]
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            fm.append(round(int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var())))
            #BLUR
            if ((self.kernel / 2) != 0):
                imOriginal = cv2.GaussianBlur(imOriginal,(self.kernel,self.kernel),0)
            else:
                self.kernel = self.kernel-1
                imOriginal = cv2.GaussianBlur(imOriginal,(self.kernel,self.kernel),0)

            
            img = imOriginal[self.ymin:self.ymax, self.xmin:self.xmax]
            
            
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            if not (os.path.isdir("../IMG-OUT/blur/")):
                os.makedirs("../IMG-OUT/blur/")

            cv2.imwrite("../IMG-OUT/blur/" + self.imageList[i], cv2.putText(cv2.cvtColor(imOriginal, cv2.COLOR_BGR2RGB),f"fm: {round(int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var()))} Kernel: {self.kernel}",(imOriginal.shape[1]- 280,(imOriginal.shape[0]-30)),color=(0,0,0),fontFace=1,fontScale=1.2,thickness=2))

            fmMod.append(round(int(cv2.Laplacian(gray, cv2.CV_64F,ksize=5).var())))
            


        fmMod = str(round(np.mean(fmMod)))
        fm = str(round(np.mean(fm)))

        self.valoresBlurredB.emit(fm,fmMod)

            
            


