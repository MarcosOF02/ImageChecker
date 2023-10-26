from ast import And
import cv2
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QMainWindow, QGraphicsScene
from PyQt5.QtGui import  QPixmap, QImage
from PyQt5 import QtCore
import qimage2ndarray
from main_ui import Ui_MainWindow


# CLASE PARA EVENTOS DEL RATON EN EL Graphics View

class GraphicsScene(QGraphicsScene):
    
    initialPosition = QtCore.QPointF(0,0)
    finalPosition = QtCore.QPointF(0,0)

    def __init__ (self, parent=None,mainGuiManager=None):
        super(GraphicsScene, self).__init__ (parent)
        self.x1new,self.x2new,self.y1new,self.y2new = 0,0,0,0
        self.track = False
        self.mainGuiManager = mainGuiManager


    def mousePressEvent(self, event):  
        if event.button() == QtCore.Qt.LeftButton:
            super(GraphicsScene, self).mousePressEvent(event)
               
            self.track = True

            self.initialPosition = QtCore.QPointF(event.scenePos())
            
            self.x1new = int(self.initialPosition.x())
            self.y1new = int(self.initialPosition.y())
            self.x2new = self.x1new
            self.y2new = self.y1new
                
            self.x2new = int(self.x2new)
            self.y2new = int(self.y2new)  


    def mouseMoveEvent(self, event):
        if self.track == True:
            super(GraphicsScene, self).mouseMoveEvent(event)
            self.finalPosition = QtCore.QPointF(event.scenePos())
            self.x2new = int(self.finalPosition.x())
            self.y2new = int(self.finalPosition.y())
            
            self.x2new = int(self.x2new)
            self.y2new = int(self.y2new)   

            self.renderScene()
    

    def mouseReleaseEvent(self, event):
        super(GraphicsScene, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.track = False
                

    def renderScene(self):
        
        if self.x2new>1919:
            self.x2new = 1919
        
        if self.y2new>1079:
            self.y2new = 1079

        if self.x2new<0:
            self.x2new = 0
        
        if self.y2new<0:
            self.y2new = 0
            
        if self.y1new<0:
            self.y1new = 0

        if self.x1new<0:
            self.x1new = 0
            
        self.x1new = int(self.x1new)
        self.y1new = int(self.y1new)
        self.x2new = int(self.x2new)
        self.y2new = int(self.y2new)
        self.mainGuiManager.showRect(self.x1new,self.y1new,self.x2new,self.y2new)

   


class MainGUIManager(QMainWindow):
    def __init__(self, mainController, app_dir):
        QMainWindow.__init__(self)
        self.mainController = mainController
        self.ui = Ui_MainWindow()
        self.appdir = app_dir
        self.contador = 0
        self.ui.setupUi(self)
        self.imAnchoOriginal = None
        self.imAltoOriginal = None

        # Parte de procesados        
        self.hsvcone = cv2.imread(self.appdir + "hsvcone.png")
        self.hsvcone = cv2.cvtColor(self.hsvcone, cv2.COLOR_BGR2RGB)

        self.ui.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # parte de comprobacion HSV

        # Cargar imagen paleta HSV
        image = cv2.imread(self.appdir + "paletaHSV.png")

        self.mainSceneHSV = QGraphicsScene(self.ui.graphicsView_5)
        
        self.ui.graphicsView_5.setScene(self.mainSceneHSV)
        
        self.mainSceneHSV.clear()
        self.mainSceneHSV.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(image)).scaled(self.ui.graphicsView_5.width() + 80, self.ui.graphicsView_5.height() + 80, QtCore.Qt.KeepAspectRatio))
        self.mainSceneHSV.update()
        
        self.refreshSlidesValue()


        self.ui.frame_brillo.setStyleSheet("background-position: center; background-image: url(info.png);background-repeat: no-repeat; ")
        self.ui.frame_brillo.setToolTip("Modificacion del brillo de la imagen")

        self.ui.frame_blur.setStyleSheet("background-position: center; background-image: url(info.png);background-repeat: no-repeat; ")
        self.ui.frame_blur.setToolTip("Aqui modificas el difuminado de la imagen, tiene que ser valor inpar o 0 que sera nada")

        self.ui.frame_valoresSV.setStyleSheet("background-position: center; background-image: url(info.png);background-repeat: no-repeat; ")
        self.ui.frame_valoresSV.setToolTip("Valores de la S y V de HSV que esta dando la imagen")

        self.ui.frame_region.setStyleSheet("background-position: center; background-image: url(info.png);background-repeat: no-repeat; ")
        self.ui.frame_region.setToolTip("Region en la que se tendra en cuenta las modificaciones, todo a 0 es la imagen completa")

        self.ui.frame_rangoHSV.setStyleSheet("background-position: center; background-image: url(info.png);background-repeat: no-repeat; ")
        self.ui.frame_rangoHSV.setToolTip("Modifica el rango HSV que se mostrara reflejado en la mascara de la imagen")
        
        
        self.mainScene1 = QGraphicsScene(self.ui.graphicsView)
        self.mainScene2 = GraphicsScene(self.ui.graphicsView_2,self)
        self.ui.graphicsView_2.setScene(self.mainScene2)
        

        self.set_GUI_signals()

        
        return


    def set_GUI_signals(self):

        # Parte comprobación HSV
        # De class quemada
        self.mainController.quemado.mask.connect(self.showMaskQuemadas)
        self.mainController.quemado.modded.connect(self.showModdedQuemadas)
        self.mainController.quemado.pixeles.connect(self.infoQuemadas)
        self.ui.pushButton_cambiarBrillo.clicked.connect(self.controlQuemadas)
        self.ui.pushButton_5.clicked.connect(self.guardarImagen)
        self.mainController.quemado.mediamoda.connect(self.MedModQuemadas)
        self.ui.pushButton_cambiar.clicked.connect(self.modifyHSVRange)

        self.ui.pushButton_2.clicked.connect(self.mainController.imageMenos)
        self.ui.pushButton.clicked.connect(self.mainController.imageMas)


        self.ui.horizontalSlider_hmin.valueChanged.connect(self.refreshSlidesValue)
        self.ui.horizontalSlider_hmin.valueChanged.connect(self.modifyHSVRangeWithSlide)

        self.ui.horizontalSlider_hmax.valueChanged.connect(self.refreshSlidesValue)
        self.ui.horizontalSlider_hmax.valueChanged.connect(self.modifyHSVRangeWithSlide)

        self.ui.horizontalSlider_smin.valueChanged.connect(self.refreshSlidesValue)
        self.ui.horizontalSlider_smin.valueChanged.connect(self.modifyHSVRangeWithSlide)

        self.ui.horizontalSlider_smax.valueChanged.connect(self.refreshSlidesValue)
        self.ui.horizontalSlider_smax.valueChanged.connect(self.modifyHSVRangeWithSlide)

        self.ui.horizontalSlider_vmin.valueChanged.connect(self.refreshSlidesValue)
        self.ui.horizontalSlider_vmin.valueChanged.connect(self.modifyHSVRangeWithSlide)

        self.ui.horizontalSlider_vmax.valueChanged.connect(self.refreshSlidesValue)
        self.ui.horizontalSlider_vmax.valueChanged.connect(self.modifyHSVRangeWithSlide)

        
        # Parte procesados

        self.mainController.controlRangoDia.valoresNormales.connect(self.valoresNormalesDia)
        self.mainController.controlRangoDia.valoresQuemada.connect(self.valoresQuemadaDia)
        self.mainController.controlRangoDia.valoresBlurred.connect(self.valorBlurDia)
        self.ui.pushButton_3.clicked.connect(self.envioRoiDia)

        ### SEÑALES TAB NOCHE
        self.mainController.controlRangoNoche.valoresNormalesNoche.connect(self.valoresNormalesNoche)
        self.mainController.controlRangoNoche.valoresQuemadaNoche.connect(self.valoresQuemadaNoche)
        self.mainController.controlRangoNoche.valoresBlurredNoche.connect(self.valorBlurNoche)
        self.ui.pushButton_4.clicked.connect(self.envioRoiNoche)

        ### SEÑALES TAB Infrarrojo
        self.mainController.controlRangoIr.valoresNormalesIr.connect(self.valoresNormalesIr)
        self.mainController.controlRangoIr.valoresQuemadaIr.connect(self.valoresQuemadaIr)
        self.mainController.controlRangoIr.valoresBlurredIr.connect(self.valorBlurIr)
        self.ui.pushButton_6.clicked.connect(self.envioRoiIr)

        ### SEÑALES TAB Blur
        self.mainController.controlRangoBlur.valoresBlurredB.connect(self.valorBlurBlur)
        self.ui.pushButton_7.clicked.connect(self.envioRoiBlur)


    def resizeEvent(self, event):
        super(QMainWindow, self).resizeEvent(event)
        try:
            self.showMaskQuemadas(self.maskImg)
        except:
            pass
        self.mainScene2.renderScene()


    # Funciones comprobación HSV

    def refreshSlidesValue(self):
        self.ui.label_hminBar.setText(f"H Min: {self.ui.horizontalSlider_hmin.value()}")
        self.ui.label_hmaxBar.setText(f"H Max: {self.ui.horizontalSlider_hmax.value()}")
        self.ui.label_sminBar.setText(f"S Min: {self.ui.horizontalSlider_smin.value()}")
        self.ui.label_smaxBar.setText(f"S Max: {self.ui.horizontalSlider_smax.value()}")
        self.ui.label_vminBar.setText(f"V Min: {self.ui.horizontalSlider_vmin.value()}")
        self.ui.label_vmaxBar.setText(f"V Max: {self.ui.horizontalSlider_vmax.value()}")


    def modifyHSVRangeWithSlide(self):
        self.mainController.quemado.setHSVRange(int(self.ui.horizontalSlider_hmin.value()),int(self.ui.horizontalSlider_hmax.value()),int(self.ui.horizontalSlider_smin.value()),int(self.ui.horizontalSlider_smax.value()),int(self.ui.horizontalSlider_vmin.value()),int(self.ui.horizontalSlider_vmax.value()))
        self.mainController.quemado.HSV(img=None,hsvOriginal=None)


    def infoQuemadas(self,totales,quemados,bien,fm):
        self.ui.label_fm.setText(fm)
        self.ui.label_pko.setText(quemados)
        self.ui.label_pok.setText(bien)


    def showMaskQuemadas(self,image):
        image = cv2.resize(image,(self.ui.graphicsView.width()-5,self.ui.graphicsView.height()-10))
        self.maskImg = image
        
        self.ui.graphicsView.setScene(self.mainScene1)
        
        self.mainScene1.clear()
        self.mainScene1.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(image)).scaled(self.ui.graphicsView.width(), self.ui.graphicsView.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainScene1.update()
        
        
    def showModdedQuemadas(self,modded,noRectangleImg):
        self.imAnchoOriginal = modded.shape[1]
        self.imAltoOriginal = modded.shape[0]
        modded = cv2.resize(modded,(self.ui.graphicsView_2.width()-5,self.ui.graphicsView_2.height()-10))
        noRectangleImg = cv2.resize(noRectangleImg,(self.ui.graphicsView_2.width()-5,self.ui.graphicsView_2.height()-10))
        self.moddedQuemada = modded
        self.moddedQuemadaNoRectangle = noRectangleImg
        
        self.mainScene2.clear()
        self.mainScene2.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(modded)))
        self.mainScene2.update()
    

    def showRect(self,x1,y1,x2,y2): 
        try:
            self.ui.lineEdit_xmin.setText(str(x1))
            self.ui.lineEdit_ymin.setText(str(y1))
            self.ui.lineEdit_xmax.setText(str(x2))
            self.ui.lineEdit_ymax.setText(str(y2))
            mod = self.moddedQuemada.copy()

            mod = cv2.resize(mod,(self.ui.graphicsView_2.width()-5,self.ui.graphicsView_2.height()-10))
            mod = cv2.rectangle(mod,(int(x1),int(y1)),(int(x2),int(y2)),(255,0,0),1)


            self.mainScene2.clear()
            #self.mainScene2.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(mod)).scaled(int(self.ui.graphicsView_2.width()), int(self.ui.graphicsView_2.height()) - 5, QtCore.Qt.KeepAspectRatio))
            self.mainScene2.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(mod)))
            self.mainScene2.update()

        except Exception as e:
            pass


    def controlQuemadas(self):
        try:
            escala_x = (self.ui.graphicsView_2.width()-5) / self.imAnchoOriginal
            escala_y = (self.ui.graphicsView_2.height()) / self.imAltoOriginal

            self.mainController.InicioQuemada(self.ui.lineEdit_brillo.text(),self.ui.lineEdit_kernel.text(),self.ui.lineEdit_sigma.text(),str(int(int(self.ui.lineEdit_xmin.text()) / escala_x)),str(int(int(self.ui.lineEdit_ymin.text()) / escala_y)),str(int(int(self.ui.lineEdit_xmax.text()) / escala_x)),str(int(int(self.ui.lineEdit_ymax.text()) / escala_y)))
        except:
            pass


    def MedModQuemadas(self,media,moda,mediav,modav):
        self.ui.label_smedia.setText(media)
        self.ui.label_smoda.setText(moda)
        self.ui.label_vmedia.setText(mediav)
        self.ui.label_vmoda.setText(modav)


    def guardarImagen(self):
        self.mainController.guardarImgQuemada(self.ui.lineEdit_brillo.text(),self.ui.lineEdit_kernel.text(),self.moddedQuemada,self.moddedQuemadaNoRectangle,self.maskImg)


    def modifyHSVRange(self):
        self.mainController.quemado.setHSVRange(int(self.ui.lineEdit_hmin.text()),int(self.ui.lineEdit_hmax.text()),int(self.ui.lineEdit_smin.text()),int(self.ui.lineEdit_smax.text()),int(self.ui.lineEdit_vmin.text()),int(self.ui.lineEdit_vmax.text()))
        self.mainController.quemado.start()


    # Funciones procesados


    def valoresNormalesDia(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm):
        self.ui.label_smedia_2.setText(media_s)
        self.ui.label_smoda_2.setText(moda_s)
        self.ui.label_smedmod.setText(medmod_s)
        self.ui.label_smax.setText(max_s)

        self.ui.label_vmedia_2.setText(media_v)
        self.ui.label_vmoda_2.setText(moda_v)
        self.ui.label_vmedmod.setText(medmod_v)
        self.ui.label_vmax.setText(max_v)

        self.ui.label_fmbien.setText(fm)


    def valoresQuemadaDia(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,hsvimage):
        self.ui.label_smediaM.setText(media_s)
        self.ui.label_smodaM.setText(moda_s)
        self.ui.label_smedmodM.setText(medmod_s)
        self.ui.label_smaxM.setText(max_s)

        self.ui.label_vmediaM.setText(media_v)
        self.ui.label_vmodaM.setText(moda_v)
        self.ui.label_vmedmodM.setText(medmod_v)
        self.ui.label_vmaxM.setText(max_v)
        self.setHSVImageDia(hsvimage)


    def valorBlurDia(self,fm):
        self.ui.label_fmmal.setText(fm)


    def envioRoiDia(self):
        self.mainController.iniciarComprobacionDia(self.ui.lineEdit_xmin_2.text(),self.ui.lineEdit_ymin_2.text(),self.ui.lineEdit_xmax_2.text(),self.ui.lineEdit_ymax_2.text(),self.ui.lineEdit_brillo_2.text())

        
    def setHSVImageDia(self,image):

        self.mainSceneDIA = QGraphicsScene(self.ui.graphicsView_3)
        self.ui.graphicsView_3.setScene(self.mainSceneDIA)
        
        self.mainSceneDIA.clear()
        self.mainSceneDIA.addPixmap(image.scaled(self.ui.graphicsView_3.width(), self.ui.graphicsView_3.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainSceneDIA.update()


    ### TAB NOCHE
    def valoresNormalesNoche(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm):
        self.ui.label_smedia_3.setText(media_s)
        self.ui.label_smoda_3.setText(moda_s)
        self.ui.label_smedmod_2.setText(medmod_s)
        self.ui.label_smax_2.setText(max_s)

        self.ui.label_vmedia_3.setText(media_v)
        self.ui.label_vmoda_3.setText(moda_v)
        self.ui.label_vmedmod_2.setText(medmod_v)
        self.ui.label_vmax_2.setText(max_v)

        self.ui.label_fmbien_2.setText(fm)


    def valoresQuemadaNoche(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,hsvimage):
        self.ui.label_smediaM_2.setText(media_s)
        self.ui.label_smodaM_2.setText(moda_s)
        self.ui.label_smedmodM_2.setText(medmod_s)
        self.ui.label_smaxM_2.setText(max_s)

        self.ui.label_vmediaM_2.setText(media_v)
        self.ui.label_vmodaM_2.setText(moda_v)
        self.ui.label_vmedmodM_2.setText(medmod_v)
        self.ui.label_vmaxM_2.setText(max_v)
        self.setHSVImageNoche(hsvimage)


    def valorBlurNoche(self,fm):
        self.ui.label_fmmal_2.setText(fm)


    def envioRoiNoche(self):
        self.mainController.iniciarComprobacionNoche(self.ui.lineEdit_xmin_3.text(),self.ui.lineEdit_ymin_3.text(),self.ui.lineEdit_xmax_3.text(),self.ui.lineEdit_ymax_3.text(),self.ui.lineEdit_brillo_3.text())

        
    def setHSVImageNoche(self,image):

        self.mainSceneNoche = QGraphicsScene(self.ui.graphicsView_4)
        self.ui.graphicsView_4.setScene(self.mainSceneNoche)
        
        self.mainSceneNoche.clear()
        self.mainSceneNoche.addPixmap(image.scaled(self.ui.graphicsView_4.width(), self.ui.graphicsView_4.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainSceneNoche.update()


    ## TAB Infrarrojo

    def valoresNormalesIr(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm):
        self.ui.label_smedia_4.setText(media_s)
        self.ui.label_smoda_4.setText(moda_s)
        self.ui.label_smedmod_3.setText(medmod_s)
        self.ui.label_smax_3.setText(max_s)

        self.ui.label_vmedia_4.setText(media_v)
        self.ui.label_vmoda_4.setText(moda_v)
        self.ui.label_vmedmod_3.setText(medmod_v)
        self.ui.label_vmax_3.setText(max_v)

        self.ui.label_fmbien_3.setText(fm)


    def valoresQuemadaIr(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,hsvimage):
        self.ui.label_smediaM_3.setText(media_s)
        self.ui.label_smodaM_3.setText(moda_s)
        self.ui.label_smedmodM_3.setText(medmod_s)
        self.ui.label_smaxM_3.setText(max_s)

        self.ui.label_vmediaM_3.setText(media_v)
        self.ui.label_vmodaM_3.setText(moda_v)
        self.ui.label_vmedmodM_3.setText(medmod_v)
        self.ui.label_vmaxM_3.setText(max_v)
        self.setHSVImageIr(hsvimage)


    def valorBlurIr(self,fm):
        self.ui.label_fmmal_3.setText(fm)


    def envioRoiIr(self):
        self.mainController.iniciarComprobacionIr(self.ui.lineEdit_xmin_4.text(),self.ui.lineEdit_ymin_4.text(),self.ui.lineEdit_xmax_4.text(),self.ui.lineEdit_ymax_4.text(),self.ui.lineEdit_brillo_4.text())

        
    def setHSVImageIr(self,image):

        self.mainSceneIr = QGraphicsScene(self.ui.graphicsView_6)
        self.ui.graphicsView_6.setScene(self.mainSceneIr)
        
        self.mainSceneIr.clear()
        self.mainSceneIr.addPixmap(image.scaled(self.ui.graphicsView_6.width(), self.ui.graphicsView_6.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainSceneIr.update()


    ## BLUR

    def envioRoiBlur(self):
        self.mainController.iniciarComprobacionBlur(self.ui.lineEdit_xmin_5.text(),self.ui.lineEdit_ymin_5.text(),self.ui.lineEdit_xmax_5.text(),self.ui.lineEdit_ymax_5.text(),self.ui.lineEdit_kernel_2.text())


    def valorBlurBlur(self,fm,fmMod):
        self.ui.label_fmbien_4.setText(fm)
        self.ui.label_fmmal_4.setText(fmMod)
