def GenerateTekFile(WORK_DIR="",ReportName=""):
    f = open(ReportName+".tex","a")
    print(WORK_DIR)
    list = open(WORK_DIR+"\\list.txt")


    Template = open("tekTemplate.txt")
    PicTemp = open("tekTemplatePicture.txt")
    FirstPage = open("CelesticaTemplate.txt")

    PicTempLines = PicTemp.readlines()
    TestPoints = list.readlines()
    FirstPageLines = FirstPage.readlines()


    content = Template.readlines()
    # Remember to print out directly you need to add an extra slash for it to print out 




    #for line in content:
    #    line.replace("Blah")
    #    f.write(line)

    for someLine in FirstPageLines:
        print(someLine)
        f.write(someLine)
        
    f.write("\n")
    f.write("\n")
    f.write("\\newpage\n")
    f.write("\\section{\color{black}I2C Results}") 
    for tp in TestPoints:
        f.write("\\TileWallPaper{\paperwidth}{\paperheight}{CelesticaNextPages.pdf}\n")
        tp = tp.replace("\n",'')
        location = tp+"/results.txt"
        figurename = "\\subsection{\color{black}blah}\n"
        figurename = figurename.replace("blah",tp+" Waveform characterestics")
        figurename = figurename.replace("_"," ")
        f.write(figurename)
        
        #Creating Table starts here
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\begin{tabular}{llll}\n")
        f.write("\\hline\n")
        f.write("\\multicolumn{1}{|l|}{Parameter} & \\multicolumn{1}{l|}{Specification} & \\multicolumn{1}{l|}{Measured Results} & \\multicolumn{1}{l|}{Status} \\\ \\hline\n")
        #Opens Results to load the results 
        TestResults = open(location)
        results = TestResults.readlines()
        #loads results into the template loaded from Tektemplate need to change to I2C Template 
        for i in range(len(content)):
            results[i] = results[i].replace("\n", '')
            results[i] = results[i].replace('"', '')
            content[i] = content[i].replace("blah", results[i])
            print(content[i])
            f.write(content[i])
        f.write("\n")
        f.write("\\end{tabular} \n")
        f.write("\\end{table} \n")
        print("\n")
        f.write("\n")
        location = tp+"/PicList.txt"
        picnames = open(location)
        
        # setting up Pictures 
        pic = picnames.readlines()
        f.write("\\newpage\n")
        f.write("\\TileWallPaper{\paperwidth}{\paperheight}{CelesticaNextPages.pdf}\n")
        # Loading pictures from the pictures template and updating them, you can only fit two screen shots per page. 
        # Need to generalize by moding 2 and setting if statement to 0 becasue we only generate new page every two screen shots 
        for i in range(len(PicTempLines)):
            if i == 2:
                f.write("\\newpage\n")
                f.write("\\TileWallPaper{\paperwidth}{\paperheight}{CelesticaNextPages.pdf}\n")
            pic[i] = pic[i].replace("\n","")
            location = tp +"/"+pic[i]
            piclocation = PicTempLines[i].replace("BLAH",location)
            f.write(piclocation)
        f.write("\n")
        f.write("\n")
        f.write("\\newpage\n")
    f.write("\\end{document}")

        




    PicTempLines[2] = PicTempLines[2].replace("BLAH",TestPoints[0])
    print(PicTempLines[2])  

    #from pylatex import Document 
    f.close()
    #
    #doc = Document('basic')
    #doc.generate_pdf('main',clean_tex=False)