# -*- coding: utf-8 -*-
import re;
import copy;
import os, sys, glob;

pathToFile = os.path.abspath(os.curdir)
#pathToFile = os.path.abspath(os.path.dirname(sys.argv[0]))
#pathToFile2 = 'C:\\User\\I.Nuriakhmetov\\Desktop\\filefoMichail'
str = []
os.chdir(pathToFile)
for file in glob.glob("*.bdf"):
    string = str.append(file)
s = str[0].split('_')
apndx = s[0]

def getFileContent(pathToFile):
    with open(pathToFile, 'r') as f:
        data = f.read()
        f.close()
        return data

def createNewFile(pathToFile):
    NewFile = open(pathToFile,'w').close()
    return NewFile

#def copytofile(pathToFile):
 #   CopyFile = open(pathToFile, 'w').close()
  #  return CopyFile

textforcopy = getFileContent(pathToFile + '\\' + apndx + '_nm.bdf')
#print(textforcopy)
fileToCopy = createNewFile(pathToFile + '\\' + apndx + '_nm_loads.bdf')
fileToCopy = open(pathToFile + '\\' + apndx + '_nm_loads.bdf','w').write(textforcopy)

textforreplace = getFileContent(pathToFile + '\\' + apndx + '_nm_loads.bdf')
replacementtext1 = '$ Referenced Coordinate Frames'
indexofreplacementtext1 = textforreplace.index(replacementtext1)
sizeofreplacementtext = textforreplace[indexofreplacementtext1:]
#print(sizeofreplacementtext)
txt = ''
textforreplace = getFileContent(pathToFile + '\\' + apndx + '_nm_loads.bdf').replace(sizeofreplacementtext, txt)
fileforreplace = open(pathToFile + '\\' + apndx + '_nm_loads.bdf', 'w').write(textforreplace)

textold = getFileContent(pathToFile + '\\' + apndx + '_static.bdf')
tx1 = 'SUBCASE 1'
tx11 = '$ Subcase'
tx2 = '   ' + 'LOAD'
tx22 = '   DISPLACEMENT('
indextx1 = textold.index(tx1)
indextx11 = textold.index(tx11)
indextx2 = textold.index(tx2)
indextx22 = textold.index(tx22)
oldtext1 = textold[indextx1:indextx11]
oldtext2 = textold[indextx2:indextx22]
oldtext = oldtext1 + oldtext2
print('old:', oldtext1, 'old2:', oldtext2)

textnew = getFileContent(pathToFile + '\\' + apndx + '_nm_loads.bdf')
tx3 = 'SUBCASE 1'
#tx33 = ''
tx4 = '$ Direct Text Input for this Subcase'
tx11 = '$ Direct'
tx22 = '$ SUBCASE'
indextx3 = textnew.index(tx3)
indextx4 = textnew.index(tx4)
newtext = textnew[indextx3:indextx4]

textforchanges = getFileContent(pathToFile + '\\' + apndx + '_nm_loads.bdf').replace(newtext, oldtext)
f = open(pathToFile + '\\' + apndx + '_nm_loads.bdf','w').write(textforchanges)

#oldtext - заменяемый текстs
#newtext - то, на что заменяется

textend = getFileContent(pathToFile + '\\' + apndx + '_static.bdf')
tx5 ='$ Loads for Load Case : Default'
tx6 = ''
indextx5 = textend.index(tx5)
indextx6 = textend.index(tx6)+ len(tx6)
endtext = textend[indextx5:]
ff = open(pathToFile + '\\' + apndx + '_nm_loads.bdf','a+').write(endtext + '\n')
textfinish = getFileContent(pathToFile + '\\' + apndx + '_nm_loads.bdf')
#print('____',textfinish)
print('textfinish:', textfinish)
tx7 = '$ Displacement Constraints of Load Set'
tx8 = '$ Pressure Loads of Load Set'
indextx7 = textfinish.index(tx7)
indextx8 = textfinish.index(tx8)
indextx9 = textfinish[indextx8 + len(tx8):].index(tx8) + indextx8 + len(tx8)
#if tx8 in textfinish:
 #   indextx8 = textfinish.index(tx8)
  #  for n in range(2):
   #     n=n+1
    #    list.append(indextx8)
#print(list)

#if indextx7 <= indextx8:
#for tx8 in textfinish:
 #   k=k+1
#print(k)
 #else:
finishtext = textfinish[indextx7:indextx9]
textfinish = getFileContent(pathToFile + '\\' + apndx + '_nm_loads.bdf').replace(finishtext, '')
fff = open(pathToFile + '\\' + apndx + '_nm_loads.bdf', 'w').write(textfinish)
print(indextx7, indextx9, 'finish:', finishtext)












