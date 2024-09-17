import os
from PIL import Image
import customtkinter as ctk

RunMode : None
class Img:

    Camera=1
    Camera1=1
    ImgWidth=920
    ImgHeight=520
    TempDb = "C:\\ELVIS\\TmpDB\\" #Windows
    TempDB = "/ELVIS/TmpDB/"     #Linux
    InTempCreate=["001_Master", "002_Model", "003_Configuration",]
    GeneralPath=TempDb

    Master= GeneralPath+InTempCreate[0]+"\\Master.jpg"
    CutOriginalPicture = GeneralPath+InTempCreate[0]+"\\NotFilter.jpg"
    WithFilter=GeneralPath+InTempCreate[0]+"\\WithFilter.jpg"
    Contorns= GeneralPath+InTempCreate[0]+"\\Contorns.jpg"
    Model=GeneralPath+InTempCreate[1]

    InspectionData=[] #More relevant
    Inspection=[]
    InspectionArea=[]
    ThresholdFilter=127

    LoadAndSaveConfiguration=GeneralPath+InTempCreate[2]+"\\Configuration.ini"
class Cam:
    id=None
    StatusLight=None
    LightConfiguration=None
    Tool=None
    InspectionArea=[]
    Umbral=None
    CloseContourns=None
    MinContourn=None
    MaxContourn=None
    ValueContorn=None
    Invert=None

class Calibration:
    CalibrationX=3
    CalibrationY=2
    CalibrationFitler=7

class Inherit:


    SelectionFilter=""
    Inspection1="0,0,0,0,0"
    #In this moment i need only one Inspection zone
    #Inspection2="0,0,0,0,0"

#class Canny:





class PlayStopStatus:
    Status=""

class MenuConfig:
    MenuPictureSize = 25
    MenuTXTSize = 20
    TextNormalSize = 50
    MenuIconSize=30

class Picture:
    XY = MenuConfig.MenuPictureSize
    IXY = MenuConfig.MenuIconSize
    ixy = MenuConfig.MenuIconSize-10
    Ico = os.path.join("Img", "Logo", "Logo.png")
    Hom = os.path.join("Img", "Buttons", "Icon_Home.png")  
    Tra = os.path.join("Img", "Buttons", "Icon_MTrain.png")  
    Too = os.path.join("Img", "Buttons", "Icon_Config.png") 
    
    Home = ctk.CTkImage(light_image=Image.open(Hom), size=(XY, XY))
    Training = ctk.CTkImage(light_image=Image.open(Tra), size=(XY, XY))
    Tools = ctk.CTkImage(light_image=Image.open(Too), size=(XY, XY))
    Icon = ctk.CTkImage(light_image=Image.open(Ico), size=(IXY, IXY))
    #---------------------------------------------------------------#
    # Buttons for Main interface
    RUE = os.path.join("Img", "Buttons", "Icon_RunEnable.png")
    RUD = os.path.join("Img", "Buttons", "Icon_RunDisable.png")
    PAE = os.path.join("Img", "Buttons", "Icon_PauseEnable.png")
    PAD = os.path.join("Img", "Buttons", "Icon_PauseDisable.png")
    
    RunE = ctk.CTkImage(light_image=Image.open(RUE), size=(XY, XY))
    RunD = ctk.CTkImage(light_image=Image.open(RUD), size=(XY, XY))
    PauseE = ctk.CTkImage(light_image=Image.open(PAE), size=(XY, XY))
    PauseD = ctk.CTkImage(light_image=Image.open(PAD), size=(XY, XY))


    # ---------------------------------------------------------------#
    #Controls for Manipulation Picture
    CamPl = os.path.join("Img","Camera","Zoom_Plus.png")
    CamMi = os.path.join("Img","Camera","Zoom_Min.png")
    CamRe = os.path.join("Img","Camera","Zoom_Restart.png")
    RowUp = os.path.join("Img","Camera","Row_Up.png")
    RowDo = os.path.join("Img","Camera","Row_Do.png")
    RowLe = os.path.join("Img","Camera","Row_Le.png")
    RowRi = os.path.join("Img","Camera","Row_Ri.png")

    CameraPl = ctk.CTkImage(light_image=Image.open(CamPl),size=(ixy,ixy))
    CameraMi = ctk.CTkImage(light_image=Image.open(CamMi),size=(ixy,ixy))
    CameraRe = ctk.CTkImage(light_image=Image.open(CamRe),size=(ixy,ixy))

    RowUP = ctk.CTkImage(light_image=Image.open(RowUp), size=(ixy-10,ixy-15))
    RowDO = ctk.CTkImage(light_image=Image.open(RowDo), size=(ixy-10,ixy-15))
    RowLE = ctk.CTkImage(light_image=Image.open(RowLe), size=(ixy-15,ixy-10))
    RowRI = ctk.CTkImage(light_image=Image.open(RowRi), size=(ixy-15,ixy-10))


    # ---------------------------------------------------------------#
    #Controls for Light Intensity
    LMaxk = os.path.join("Img", "LightControls","MaxLightOk.png")
    LMaxN = os.path.join("Img", "LightControls","MaxLightNo.png")

    LMidK = os.path.join("Img", "LightControls", "MidLightOk.png")
    LMidN = os.path.join("Img", "LightControls", "MidLightNo.png")

    LMinK = os.path.join("Img", "LightControls", "MinLightOk.png")
    LMinN = os.path.join("Img", "LightControls", "MinLightNo.png")

    LightMaxOk = ctk.CTkImage(light_image=Image.open(LMaxk),size=(IXY,IXY))
    LightMaxNo = ctk.CTkImage(light_image=Image.open(LMaxN),size=(IXY,IXY))

    LightMidOk = ctk.CTkImage(light_image=Image.open(LMidK),size=(IXY,IXY))
    LightMidNo = ctk.CTkImage(light_image=Image.open(LMidN),size=(IXY,IXY))

    LightMinOk = ctk.CTkImage(light_image=Image.open(LMinK),size=(IXY,IXY))
    LightMinNo = ctk.CTkImage(light_image=Image.open(LMinN),size=(IXY,IXY))

    #---------------------------------------------------------------#
    #Controls for Light Direction
    LUpK = os.path.join("Img", "LightControls", "UpLightOk1.png")
    LUpN = os.path.join("Img", "LightControls", "UpLightNo.png")

    LDonK = os.path.join("Img", "LightControls","DowLightOk.png")
    LDonN = os.path.join("Img", "LightControls","DowLightNo.png")

    LCenk = os.path.join("Img","LightControls","CentLightOk.png")
    LCenN = os.path.join("Img","LightControls","CentLightNo.png")

    LLefK = os.path.join("Img","LightControls","LefLightOk.png")
    LLefN = os.path.join("Img","LightControls","LefLightNo.png")

    LRigK = os.path.join("Img","LightControls","RigLightOk.png")
    LRigN = os.path.join("Img","LightControls","RigLightNo.png")

    LightUpOk = ctk.CTkImage(light_image=Image.open(LUpK),size=(IXY,IXY))
    LightUpNo = ctk.CTkImage(light_image=Image.open(LUpN),size=(IXY,IXY))

    LightDowOk = ctk.CTkImage(light_image=Image.open(LDonK),size=(IXY,IXY))
    LightDowNo = ctk.CTkImage(light_image=Image.open(LDonN),size=(IXY,IXY))

    LightCenOk = ctk.CTkImage(light_image=Image.open(LCenk),size=(IXY,IXY))
    LightCenNo = ctk.CTkImage(light_image=Image.open(LCenN),size=(IXY,IXY))

    LightLefOk = ctk.CTkImage(light_image=Image.open(LLefK),size=(IXY,IXY))
    LightLefNo = ctk.CTkImage(light_image=Image.open(LLefN),size=(IXY,IXY))

    LightRigOk = ctk.CTkImage(light_image=Image.open(LRigK),size=(IXY,IXY))
    LightRigNo = ctk.CTkImage(light_image=Image.open(LRigN),size=(IXY,IXY))