# import des different composants necessaires

import vtk
from vtk import *

import string
import os

def testOnNodeFlag():
        test("/Users/julien/AAA_test_mesh_CETP.spis/Export/", "defaultMesh.msh","NodeFlag.dat")

def test(projectPath, meshFile, dataFile):
	
        # NB: In hte following, Id (initially starting at 1 in the mesh and data files) are
	# shifted to start at 0, as VTK (and most of the visualisation libraries) does. 
	
        print "START test"
        
        #projectPath = "/Users/julien/AAA_test_mesh_CETP.spis/Export/"
        meshSubDir = "Mesh"
        #meshFile = "defaultMesh.msh"
        dataSubDir = "DataField"
        #dataFile = "NodeFlag.dat"
        
        print "Nodes reading... "
        fileIn = open(projectPath+os.sep+meshSubDir+os.sep+meshFile)
        fileIn.readline() # to jump the balise
        nbNodes = string.atoi(fileIn.readline())
        print nbNodes
        pointCoord = range(nbNodes)
        for lineIndex in xrange(nbNodes):
            tmpLine = fileIn.readline().split()
	    # in the same time we re-order the nodes
            pointCoord[string.atoi(tmpLine[0])-1] = [string.atof(tmpLine[1]), string.atof(tmpLine[2]), string.atof(tmpLine[3])]
        print "DONE"
	
	print "Cells reading... "
	fileIn.readline() # to jump the balise
	fileIn.readline() # to jump the balise
	nbCells = string.atoi(fileIn.readline())
	cellList = range(nbCells)
	for lineIndex in xrange(nbCells):
	    tmpLine = []
            tmpLine.append(0) # we add an integer to flag the cell if it host data on its nodes
	    for elm in fileIn.readline().split():
		tmpLine.append(string.atoi(elm))
	    # in the same time we re-order the cells
	    cellList[tmpLine[1]-1] = tmpLine # NB: here the id of nodes on the cell are not shited yet.
        fileIn.close()
        print "DONE"
        
        # Definition des valeures correspondantes
        print "Data reading... "
        fileIn = open(projectPath+os.sep+dataSubDir+os.sep+dataFile)
        
        for i in xrange(6):
            fileIn.readline()
        nbValues = string.atoi(fileIn.readline())
        print nbValues
        ptData = [ None for i in range(nbNodes)]
        localisation = string.atoi(fileIn.readline())
        for lineIndex in xrange(nbValues):
            tmpLine = fileIn.readline().split()
	    # we re-order in the same order than nodes
            ptData[string.atoi(tmpLine[1])-1] = string.atof(tmpLine[0])
        fileIn.close()
        print "DONE"
      
        # mssing nodes
	for ptIndex in xrange(nbNodes):
            if ptData[ptIndex] == None:
	       print ptIndex, pointCoord[ptIndex], " not in data list"
      
        print "Cells filtering....  "
        # now we scan and flag the cells to 
	# here we suppose that data are on nodes and target cells are tetrahedrons
	for index in xrange(nbNodes):
	    if ptData[index] != None:
	        for cell in cellList:
		    if cell[2] == 4:
                       if index in [(cell[6]-1), (cell[7]-1), (cell[8]-1), (cell[9]-1)]:
                           cell[0] = cell[0] + 1   # by this, cell hosting data on all nodes (full)
		         			# should have this value aqual to 4
        print "DONE"
        
        # Constantes definissant le type de cellule
        VTK_TETRA = 10
        
	# creation of the grid
        unstructuredGrid =  vtkUnstructuredGrid()

	# node setting
        points = vtkPoints()
	indexVTK = 0
	corresp = [ None for i in range(nbNodes)] # this correspondance table is needed because 
						  # nodes are progressivelly added and omitted not (not
						  # hosting data) are jumped.
	for index in xrange(nbNodes):
            if ptData[index] != None:
                points.InsertNextPoint(pointCoord[index])
		corresp[index] = indexVTK
		indexVTK = indexVTK + 1
        
	# cell setting
        for cell in cellList:
            if cell[2] == 4 :
                idList = vtkIdList()
                idList.InsertNextId(corresp[cell[6]-1])
                idList.InsertNextId(corresp[cell[7]-1])
                idList.InsertNextId(corresp[cell[8]-1])
                idList.InsertNextId(corresp[cell[9]-1])
                unstructuredGrid.InsertNextCell( VTK_TETRA, idList)
        
        # attribution des valeurs aux noeuds
        data = vtkFloatArray()
        data.SetName("My data name")
        data.SetNumberOfTuples(1)
        data.SetNumberOfValues(nbValues)
        for i in range(nbValues):
	    if ptData[i] != None:
                data.InsertTuple1(corresp[i], ptData[i])
        
        unstructuredGrid.SetPoints(points)		
        unstructuredGrid.GetPointData().SetScalars(data)
        
        wr = vtk.vtkDataSetWriter()
        wr.SetInput(unstructuredGrid)
        wr.SetFileName(projectPath+os.sep+"test2_"+dataFile.split(".")[0]+".vtk")
        wr.Write()
        
        print "END test"
