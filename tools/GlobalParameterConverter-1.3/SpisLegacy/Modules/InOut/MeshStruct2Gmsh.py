###############################################################################
#                                                                             #
# Author : FW (Artenum)                                                       #
#                                                                             #
# COPYRIGHT 2001, 2002, 2003 ARTENUM SARL, FRANCE                             #
#                                                                             #
# Creation     : 02/07/2003                                                   #
#                                                                             #
# Modification : 02/07/2003  FW(Artenum)  Implementation                      #
#                                                                             #
# Vesion       : 0                                                            #
#                                                                             #
# Project ref  :                                                              #
#                                                                             #
# References   :                                                              #
#                                                                             #
# File name    :                                                              #
#                                                                             #
# File type    :                                                              #
#                                                                             #
# Command line :                                                              #
#                                                                             #
# Description  :                                                              #
#                                                                             #
# Comments/Notes :                                                            #
#                                                                             #
# Remarks :                                                                   #
#                                                                             #
# Inheritance       :                                                         #
#                                                                             #
# Inherited Fields  :                                                         #
#                                                                             #
# Inherited Methods :                                                         #
#                                                                             #
###############################################################################

# MERGED FILE

import os, string

Node = None
Element = None

ListOfOldSkeletonElmtNum = []
ListOfNewSkeltonElmtNum = []
ListOfOldNodeNum = []
ListOfNewNodeNum = []

def Reset_Variables():
   global ListOfOldNodeNum,ListOfNewNodeNum,ListOfOldSkeletonElmtNum,ListOfNewSkeltonElmtNum
   ListOfOldSkeletonElmtNum = []
   ListOfNewSkeltonElmtNum = []
   ListOfOldNodeNum = []
   ListOfNewNodeNum = []

Convert_Type = {}
Convert_Type['LINE'] = '1'
Convert_Type['TRIANGLE'] = '2'
Convert_Type['QuUADRANGLE'] = '3'
Convert_Type['TETRAHEDRON'] = '4'
Convert_Type['HEXAHEDRON'] = '5'
Convert_Type['PRISM'] = '6'
Convert_Type['PYRAMID'] = '7'
Convert_Type['POINT'] = '15'


def Convert(ListOfNode,ListOfSkeletonElmt,FileNameOut,ListOfSkeletonElmtNum = None,ListOfNodeNum = None):
    
    
   global Object,ListOfOldSkeletonElmtNum,ListOfNewSkeltonElmtNum,ListOfOldNodeNum,ListOfNewNodeNum
   NextLine = None
   Reset_Variables()
   if ListOfSkeletonElmtNum is not None:
      ListOfOldSkeletonElmtNum = ListOfSkeletonElmtNum[0]
      ListOfNewSkeltonElmtNum = ListOfSkeletonElmtNum[1]
   if ListOfNodeNum is not None:
      ListOfOldNodeNum = ListOfNodeNum[0]
      ListOfNewNodeNum = ListOfNodeNum[1]
   ReadRep = 'y'
   if os.path.isfile(FileNameOut):
      print ' File ',FileNameOut,', already exist: Overwrite (y/n) ?'
      while 1:
         print ' ',
         ReadRep = raw_input()
         if ((string.lower(ReadRep) == 'y') or (string.lower(ReadRep) == 'n')):
            break
         else:
            print 'Enter "y" or "n"'
   if string.lower(ReadRep) == 'y':
      print 'Write the OuputFile:',FileNameOut
      FileOut = open(FileNameOut,"w")
      FileOut.write('$NOD\n'+str(ListOfNode.NbNode)+'\n')
      for Node in ListOfNode.List:
         if len(ListOfOldNodeNum) > 0:
            NextLine = str(Node.NodeId)
         else:
            NextLine = str(Node.Id)
         NextLine = NextLine+' '+str(Node.Coord[0])+' '+str(Node.Coord[1])+' '+str(Node.Coord[2])+'\n'
         FileOut.write(NextLine)
      FileOut.write('$ENDNOD\n'+'$ELM\n'+str(ListOfSkeletonElmt.NbElement)+'\n')
      for Elmt in ListOfSkeletonElmt.List:
         if len(ListOfOldSkeletonElmtNum) > 0:
            NextLine = str(ListOfOldSkeletonElmtNum[ListOfNewSkeltonElmtNum.index(Elmt.Id)])
         else:
            NextLine = str(Elmt.Id)
         NextLine = NextLine+' '+Convert_Type[Elmt.Type]+' '+str(Elmt.GeoGroup.Id)+' '+str(Elmt.GeoElement.Id)+' '+str(Elmt.NodeNumber)
         #previously "for Node in Elmt.SkeletonNodeList:" manually modified at merge, TBC
         for Node in Elmt.SkeletonNodeList.List:
            if len(ListOfOldSkeletonElmtNum) > 0:
              NextLine = NextLine+' '+str(ListOfOldNodeNum[ListOfNewNodeNum.index(Node.Id)])
            else:
              NextLine = NextLine+' '+str(Node.Id)
         NextLine = NextLine+'\n'
         FileOut.write(NextLine)
      FileOut.write('$ENDELM\n')
      FileOut.close()
