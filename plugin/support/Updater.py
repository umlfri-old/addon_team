'''
Created on 29.3.2010

@author: Peterko
'''
from Differ import CDiffer
from DiffActions import EDiffActions

class CUpdater(object):
    '''
    classdocs
    '''


    def __init__(self, coProject, wcProject, upProject):
        '''
        Constructor
        '''
        # nacita checkoutnuty projekt
        # nacita working copy project
        # nacita projekt, ktory chcem updatnut
        self.__coProject = coProject
        self.__wcProject = wcProject
        self.__upProject = upProject
        
        # spocitaj kompletny diff co a wc
        cowcDiffer = CDiffer(self.__coProject, self.__wcProject)
        self.__cowcDiff = cowcDiffer.diffProjects()
        
        # spocitaj kompletny diff co a up
        coupDiffer = CDiffer(self.__coProject, self.__upProject)
        self.__coupDiff = coupDiffer.diffProjects()
        self.__searchForConflicts()
        
    def __searchForConflicts(self):
        coupInserted = self.__coupDiff.get(EDiffActions.INSERT) or []
        coupModified = self.__coupDiff.get(EDiffActions.MODIFY) or []
        coupMoved = self.__coupDiff.get(EDiffActions.MOVE) or []
        coupDeleted = self.__coupDiff.get(EDiffActions.DELETE) or []
        cowcInserted = self.__cowcDiff.get(EDiffActions.INSERT) or []
        cowcModified = self.__cowcDiff.get(EDiffActions.MODIFY) or []
        cowcDeleted = self.__cowcDiff.get(EDiffActions.DELETE) or []
        cowcMoved = self.__cowcDiff.get(EDiffActions.MOVE) or []
        
#        for ci in coupInserted:
#            print ci
#        print '---'
#        for cm in coupModified:
#            print cm
#        print '---'
#        for cd in coupDeleted:
#            print cd
#        print '---'
#        for cm in coupMoved:
#            print cm
#        print '---'
#        for ci in cowcInserted:
#            print ci
#        print '---'
#        for cm in cowcModified:
#            print cm
#        print '---'
#        for cd in cowcDeleted:
#            print cd
#        print '---'
#        for cm in cowcMoved:
#            print cm
#        print '---'