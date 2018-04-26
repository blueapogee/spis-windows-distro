# import des different composants necessaires

import vtk
from vtk import *

import string
import os

def test(projectPath, meshFile, dataFile):
        # ------------------------------------------------
        # creation de structure de donnee
        # ------------------------------------------------
        
        print "START test"
        
        #projectPath = "/Users/julien/AAA_test_mesh_CETP.spis/Export/"
        meshSubDir = "Mesh"
        #meshFile = "defaultMesh.msh"
        dataSubDir = "DataField"
        #dataFile = "NodeFlag.dat"
        
        print "mesh reading... "
        fileIn = open(projectPath+os.sep+meshSubDir+os.sep+meshFile)
        fileIn.readline()
        nbNodes = string.atoi(fileIn.readline())
        print nbNodes
        pointCoord = range(nbNodes)
        for lineIndex in xrange(nbNodes):
            tmpLine = fileIn.readline().split()
            pointCoord[string.atoi(tmpLine[0])-1] = [string.atof(tmpLine[1]), string.atof(tmpLine[2]), string.atof(tmpLine[3])]
        fileIn.close()
        print "DONE"
        
        # Definition des valeures correspondantes
        print "Data reading... "
        fileIn = open(projectPath+os.sep+dataSubDir+os.sep+dataFile)
        
        for i in xrange(6):
            print fileIn.readline()
        nbValues = string.atoi(fileIn.readline())
        print nbValues
        ptData = [ [0,0] for i in range(nbValues)]
        localisation = string.atoi(fileIn.readline())
        for lineIndex in xrange(nbValues):
            tmpLine = fileIn.readline().split()
            ptData[lineIndex] = [string.atoi(tmpLine[1])-1, string.atof(tmpLine[0])]
        fileIn.close()
        print "DONE"
        
        
        # Constantes definissant le type de cellule
        # NB: Deja definies dans VTK, redefinies ici que pour 
        # la lisibite de l'exemple
        #VTK_TETRA = 10
        #VTK_TRIANGLE = 5
        #VTK_LINE = 3
        VTK_VERTEX = 1
        
        unstructuredGrid =  vtkUnstructuredGrid()
        points = vtkPoints()
        
        for i in range(nbValues):
            print ptData[i][0], pointCoord[ptData[i][0]]
            points.InsertNextPoint(pointCoord[ptData[i][0]])
        
        
        # 1er tetrahedre
        #idList = vtkIdList()
        #idList.InsertNextId(0)
        #idList.InsertNextId(1)
        #idList.InsertNextId(2)
        #idList.InsertNextId(3)
        #unstructuredGrid.InsertNextCell( VTK_TETRA, idList) #VTK_TETRA = 10
        
        # le dernier noeud en tant que simple vertex
        idList = vtkIdList()
        for i in range(nbValues):
            idList.InsertNextId(i)
            unstructuredGrid.InsertNextCell( VTK_VERTEX, idList) #VTK_VERTEX = 1
        print "nodes set"
        
        # attribution des valeurs aux noeuds
        data = vtkFloatArray()
        data.SetName("My data name")
        data.SetNumberOfTuples(1)
        data.SetNumberOfValues(nbValues)
        for i in range(nbValues):
            print ptData[i][0], ptData[i][1]
            data.InsertTuple1(i, ptData[i][1])
        print "data set"
        
        unstructuredGrid.SetPoints(points)		
        unstructuredGrid.GetPointData().SetScalars(data)
        
        wr = vtk.vtkDataSetWriter()
        wr.SetInput(unstructuredGrid)
        wr.SetFileName("/Users/julien/AAA_test_mesh_CETP.spis/Export/"+os.sep+"test1_"+dataFile.split(".")[0]+".vtk")
        wr.Write()
        
        print "END test"