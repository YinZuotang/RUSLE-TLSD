# coding=utf-8
# -*- coding:gbk-*-
import arcpy
import os

arcpy.env.overwriteOutput = True
arcpy.ImportToolbox(r"C:\Program Files\TauDEM\TauDEM5Arc\TauDEM Tools.tbx", "TauDEM")
YearList = [年份列表]
StudyArea = r"研究区"
m = 2
with arcpy.EnvManager(snapRaster=r"D:\A_RUSLE\A2000.tif", scratchWorkspace=r"D:\Scratch",
                      workspace=r'D:\AD'): 
    RasterX = r"ST.tif"
    for a in np.arange(  ):
        for b in np.arange(  ):
            RasterY = arcpy.ia.Raster(RasterX) * a + b
            RasterY_2 = arcpy.ia.Con(RasterY < 0, 0, RasterY)
            RasterY_2.save("D:/Data/RasterY.tif")
            for y in range( ):
                year = YearList[y]
                InA_RUSLE = "D:/A_RUSLE/A" + str(year) + ".tif"
                OutAName = "D:/A/A" + str(year) + ".tif"
                A_RUSLE = arcpy.ia.RasterCalculator([InA_RUSLE, RasterY_2], ["x", "y"], "x*y")
                A_RUSLE.save(OutAName)

            for bt in [   ]:  
                for ye in range(  ):
                    year = YearList[ye]
                    InA = "D:/A/A" + str(year) + ".tif"
                    TC = "D:/TC_2/TC" + str(year) + ".tif"
                    InTC = arcpy.sa.Times(TC, bt)
                    InTC_name = "D:/InTC/TC" + str(year) + ".tif"
                    InTC.save(InTC_name)
                    OutTLAG = "D:/TLAG/TLAG" + str(year) + ".tif"
                    OutDEP = "D:/DEP/DEP" + str(year) + ".tif"
                    arcpy.TauDEM.DInfTransportLimited(r"D:\FlowDir\FlowDir2.tif", InA, InTC_name, None, None, False,
                                                      20, OutTLAG, OutDEP, None)
                AMax_list = [设置了累计百分比]
                DepMax_list = [  ]
                for AMax in AMax_list:
                    for DepMax in DepMax_list:
                        for ye_2 in range(   ):
                            year2 = YearList[ye_2]
                            InA1 = "D:/A/A" + str(year2) + ".tif"
                            OutDEP1 = "D:/DEP/DEP" + str(year2) + ".tif"
                            InA2 = arcpy.ia.Raster(InA1)
                            OutDEP2 = arcpy.ia.Raster(OutDEP1)
                            InAMax = arcpy.ia.ZonalStatistics(StudyArea, "FID", InA2, "PERCENTILE", "DATA", "CURRENT_SLICE", AMax,
                                                                 "AUTO_DETECT", "ARITHMETIC")
                            RaterA = arcpy.ia.Con(InA2 >= InAMax, InAMax, InA2)
                            RasterDEPMax = arcpy.ia.ZonalStatistics(StudyArea, "FID", OutDEP2, "PERCENTILE", "DATA", "CURRENT_SLICE", DepMax,
                                                                 "AUTO_DETECT", "ARITHMETIC")
                            RasterDEP = arcpy.ia.Con(OutDEP2 >= RasterDEPMax, RasterDEPMax, OutDEP2)
                            AD = arcpy.ia.RasterCalculator([RaterA, RasterDEP], ["x", "y"], "x-y")
                            AD_Name = "D:/AD/AD" + str(year2) + ".tif"
                            AD.save(AD_Name)
                        os.system("python D:/NSE_TLSD.py %s %s %s %s %s %s " % (a, b, bt, AMax, DepMax, m))
                        m = m+1



