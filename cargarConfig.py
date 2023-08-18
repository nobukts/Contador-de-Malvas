def loadConfiguration():
    #Declarate globals variables
    global textFont
    global fontSize

    #load config file
    f = open("config.txt","r")
    preConfgFontConditional = f.readline().split("\"")[1]
    if preConfgFontConditional == "Verdana":
        textFont = "Verdana"
    if preConfgFontConditional == "Monospace":
        textFont = "Monospace"
    if preConfgFontConditional == "Consolas":
        textFont = "Consolas"
    preConfgSizeConditional = f.readline()[13:15]
    if preConfgSizeConditional == "12":
        fontSize = 12
    if preConfgSizeConditional == "24":
        fontSize = 24
    if preConfgSizeConditional == "36":
        fontSize = 36
    preConfgDark = f.readline()
    if preConfgDark[11] == '1':
        darkMode = "dark"
    else:
        darkMode = "light"
    f.close()
    return textFont,fontSize, darkMode