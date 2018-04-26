'''
Created on Sep 13, 2010

@author: juju
'''

class BeanValidator():
    '''
    classdocs
    '''


    def __init__(self, beanTBC, refBean, filteredMemberList):
        '''
        Constructor
        '''
        self.beanTBC = benTBC
        self.refBean = refBean
        self.fiteredMemberList
        
    def checkBean(self):
        
        
        refBeanClass = repr(self.refBean).split()[0].split(".")[-1]
        beanTBCClass = repr(self.beanTBC).split()[0].split(".")[-1]
        
        for key in self.fiteredMemberList:
            cmdRef = "valRef = "+refBeanClass+"."+key
            cmdBean = "val ="+beanTBCClass+"."+key
            print cmdRef
            print cmdBean
            