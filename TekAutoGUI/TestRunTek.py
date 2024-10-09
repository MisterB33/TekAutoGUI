import os  
import TekHandler as Th
import shutil



def runTek(WORK_DIR="",RN="main"):
    print("we are here")
    print(WORK_DIR)
    WORK_DIR.replace("/","\\")
    print(WORK_DIR)
    current_path = os.getcwd()
    print(current_path)
    shutil.copy('CelesticaTemplate.txt', WORK_DIR)
    shutil.copy('tekTemplate.txt', WORK_DIR)
    shutil.copy('tekTemplatePicture.txt', WORK_DIR)
    shutil.copy('CelesticaFirstPage.pdf', WORK_DIR)
    shutil.copy('CelesticaNextPages.pdf', WORK_DIR)
    os.system("copy "+current_path+"/tekTemplate.txt "+WORK_DIR)
    os.system("copy "+current_path+"/tekTemplatePicture.txt "+WORK_DIR)
    os.system("copy "+current_path+"/CelesticaFirstPage.pdf "+WORK_DIR)
    os.system("copy "+current_path+"/CelesticaNextPages.pdf "+WORK_DIR)
    os.chdir(WORK_DIR)
    Th.GenerateTekFile(WORK_DIR,RN)
    os.system("pdflatex "+RN+".tex")
    os.system("pdflatex "+RN+".tex")
    os.remove("CelesticaFirstPage.pdf")
    os.remove("CelesticaNextPages.pdf")
    os.remove ("tekTemplate.txt")
    os.remove ("CelesticaTemplate.txt")
    os.remove ("tekTemplatePicture.txt")
    os.remove(RN+".toc")
    os.remove(RN+".log")
    os.remove(RN+".aux")
    os.remove(RN+".tex")
    os.chdir(current_path)