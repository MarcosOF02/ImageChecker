import cv2
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene
from PyQt5.QtGui import  QPixmap
from PyQt5 import QtCore
import qimage2ndarray

class MainGUIManager(QMainWindow):
    def __init__(self, MainWindow,mainController, app_dir):
        QMainWindow.__init__(self)
        self.mainController = mainController
        self.ui = MainWindow()
        self.appdir = app_dir
        self.contador = 0
        self.ui.setupUi(self)

        # Parte de procesados

        self.ui.setupUi(self)
        
        self.hsvcone = cv2.imread(self.appdir + "hsvcone.png")
        self.hsvcone = cv2.cvtColor(self.hsvcone, cv2.COLOR_BGR2RGB)


        # parte de comprobacion HSV

        # Cargar imagen paleta HSV
        image = cv2.imread(self.appdir + "paletaHSV.png")

        self.mainSceneHSV = QGraphicsScene(self.ui.graphicsView_5)
        
        self.ui.graphicsView_5.setScene(self.mainSceneHSV)
        
        self.mainSceneHSV.clear()
        self.mainSceneHSV.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(image)).scaled(self.ui.graphicsView_5.width() + 80, self.ui.graphicsView_5.height() + 80, QtCore.Qt.KeepAspectRatio))
        self.mainSceneHSV.update()


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




    # Funciones comprobación HSV

    def infoQuemadas(self,totales,quemados,bien,fm):
        self.ui.label_fm.setText(fm)
        self.ui.label_pko.setText(quemados)
        self.ui.label_pok.setText(bien)


    def showMaskQuemadas(self,image):
        self.mainScene1 = QGraphicsScene(self.ui.graphicsView)
        
        self.ui.graphicsView.setScene(self.mainScene1)
        
        self.mainScene1.clear()
        self.mainScene1.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(image)).scaled(self.ui.graphicsView.width(), self.ui.graphicsView.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainScene1.update()
        
        
    def showModdedQuemadas(self,modded):
        self.moddedQuemada = modded
        self.mainScene2 = QGraphicsScene(self.ui.graphicsView_2)
        
        self.ui.graphicsView_2.setScene(self.mainScene2)
        
        self.mainScene2.clear()
        self.mainScene2.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(modded)).scaled(self.ui.graphicsView_2.width(), self.ui.graphicsView_2.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainScene2.update()

    def controlQuemadas(self):
        self.mainController.InicioQuemada(self.ui.lineEdit_brillo.text(),self.ui.lineEdit_kernel.text(),self.ui.lineEdit_sigma.text(),self.ui.lineEdit_xmin.text(),self.ui.lineEdit_ymin.text(),self.ui.lineEdit_xmax.text(),self.ui.lineEdit_ymax.text())

    def MedModQuemadas(self,media,moda,mediav,modav):
        self.ui.label_smedia.setText(media)
        self.ui.label_smoda.setText(moda)
        self.ui.label_vmedia.setText(mediav)
        self.ui.label_vmoda.setText(modav)

    def guardarImagen(self):
        self.mainController.guardarImgQuemada(self.ui.lineEdit_brillo,self.ui.lineEdit_kernel.text(),self.moddedQuemada)


    def modifyHSVRange(self):
        self.mainController.quemado.setHSVRange(int(self.ui.lineEdit_hmin.text()),int(self.ui.lineEdit_hmax.text()),int(self.ui.lineEdit_smin.text()),int(self.ui.lineEdit_smax.text()),int(self.ui.lineEdit_vmin.text()),int(self.ui.lineEdit_vmax.text()))



    # Funciones procesados


    def valoresNormalesDia(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm):
        self.ui.label_smedia.setText(media_s)
        self.ui.label_smoda.setText(moda_s)
        self.ui.label_smedmod.setText(medmod_s)
        self.ui.label_smax.setText(max_s)

        self.ui.label_vmedia.setText(media_v)
        self.ui.label_vmoda.setText(moda_v)
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
        self.mainController.iniciarComprobacionDia(self.ui.lineEdit_xmin.text(),self.ui.lineEdit_ymin.text(),self.ui.lineEdit_xmax.text(),self.ui.lineEdit_ymax.text(),self.ui.lineEdit_brillo_2.text())

        
    def setHSVImageDia(self,image):

        self.mainSceneDIA = QGraphicsScene(self.ui.graphicsView_3)
        self.ui.graphicsView_3.setScene(self.mainSceneDIA)
        
        self.mainSceneDIA.clear()
        self.mainSceneDIA.addPixmap(image.scaled(self.ui.graphicsView_3.width(), self.ui.graphicsView_3.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainSceneDIA.update()

    ### TAB NOCHE
    def valoresNormalesNoche(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm):
        self.ui.label_smedia_2.setText(media_s)
        self.ui.label_smoda_2.setText(moda_s)
        self.ui.label_smedmod_2.setText(medmod_s)
        self.ui.label_smax_2.setText(max_s)

        self.ui.label_vmedia_2.setText(media_v)
        self.ui.label_vmoda_2.setText(moda_v)
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
        self.mainController.iniciarComprobacionNoche(self.ui.lineEdit_xmin_2.text(),self.ui.lineEdit_ymin_2.text(),self.ui.lineEdit_xmax_2.text(),self.ui.lineEdit_ymax_2.text(),self.ui.lineEdit_brillo_3.text())

        
    def setHSVImageNoche(self,image):

        self.mainSceneNoche = QGraphicsScene(self.ui.graphicsView_4)
        self.ui.graphicsView_4.setScene(self.mainSceneNoche)
        
        self.mainSceneNoche.clear()
        self.mainSceneNoche.addPixmap(image.scaled(self.ui.graphicsView_4.width(), self.ui.graphicsView_4.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainSceneNoche.update()

    ## TAB Infrarrojo

    def valoresNormalesIr(self,media_s,moda_s,medmod_s,media_v,moda_v,medmod_v,max_v,max_s,fm):
        self.ui.label_smedia_3.setText(media_s)
        self.ui.label_smoda_3.setText(moda_s)
        self.ui.label_smedmod_3.setText(medmod_s)
        self.ui.label_smax_3.setText(max_s)

        self.ui.label_vmedia_3.setText(media_v)
        self.ui.label_vmoda_3.setText(moda_v)
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
        self.mainController.iniciarComprobacionIr(self.ui.lineEdit_xmin_3.text(),self.ui.lineEdit_ymin_3.text(),self.ui.lineEdit_xmax_3.text(),self.ui.lineEdit_ymax_3.text(),self.ui.lineEdit_brillo_4.text())

        
    def setHSVImageIr(self,image):

        self.mainSceneIr = QGraphicsScene(self.ui.graphicsView_6)
        self.ui.graphicsView_6.setScene(self.mainSceneIr)
        
        self.mainSceneIr.clear()
        self.mainSceneIr.addPixmap(image.scaled(self.ui.graphicsView_6.width(), self.ui.graphicsView_6.height() - 5, QtCore.Qt.KeepAspectRatio))
        self.mainSceneIr.update()

    ## BLUR

    def envioRoiBlur(self):
        self.mainController.iniciarComprobacionBlur(self.ui.lineEdit_xmin_4.text(),self.ui.lineEdit_ymin_4.text(),self.ui.lineEdit_xmax_4.text(),self.ui.lineEdit_ymax_4.text(),self.ui.lineEdit_kernel.text())


    def valorBlurBlur(self,fm,fmMod):
        self.ui.label_fmbien_4.setText(fm)
        self.ui.label_fmmal_4.setText(fmMod)
