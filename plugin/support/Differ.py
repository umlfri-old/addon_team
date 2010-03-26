'''
Created on 27.2.2010

@author: Peterko
'''
from difflib import *
from DiffResult import CDiffResult
from DiffActions import EDiffActions
#from DictDiffer import CDictDiffer
from dictToTuple import dictToTuple
import copy

class CDiffer(object):
    '''
    classdocs
    '''


    def __init__(self, project1, project2):
        '''
        Constructor
        '''
        self.__project1 = project1
        self.__project2 = project2
        
    def diffProjects(self):
        result = []
        elements1 = self.__project1.GetElements().values()
        elements2 = self.__project2.GetElements().values()
        smElements = SequenceMatcher(None, elements1, elements2)
        
        diagrams1 = self.__project1.GetDiagrams().values()
        diagrams2 = self.__project2.GetDiagrams().values()
        smDiagrams = SequenceMatcher(None, diagrams1, diagrams2)
        
        connections1 = self.__project1.GetConnections().values()
        connections2 = self.__project2.GetConnections().values()
        smConnections = SequenceMatcher(None, connections1, connections2)
        
        diagramsOpcodes = smDiagrams.get_opcodes()
        elementsOpcodes = smElements.get_opcodes()
        connectionsOpcodes = smConnections.get_opcodes()
        self.__computeDiff(diagramsOpcodes, diagrams1, diagrams2, result)
        self.__computeDiff(elementsOpcodes, elements1, elements2, result)
        self.__computeDiff(connectionsOpcodes, connections1, connections2, result)
        
        return result
        

    def __computeDiff(self, opcodes, sequence1, sequence2, result):
        for tag, i1, i2, j1, j2 in opcodes:
            if (tag == EDiffActions.DELETE):
                # ak z prveho nieco zmizlo
                for si in sequence1[i1:i2]:
                    newDiffResult = CDiffResult(EDiffActions.DELETE, si)
                    result.append(newDiffResult)
            elif (tag == EDiffActions.INSERT):
                # ak v druhom nieco pribudlo
                for si in sequence2[j1:j2]:
                    newDiffResult = CDiffResult(EDiffActions.INSERT, si)
                    result.append(newDiffResult)
            elif (tag == EDiffActions.REPLACE):
                #replace nemoze byt
                #muselo iba ubudnut alebo pribudnut
                for si1 in sequence1[i1:i2]:
                    result.append(CDiffResult(EDiffActions.DELETE, si1))
                for si2 in sequence2[j1:j2]:                    
                    result.append(CDiffResult(EDiffActions.INSERT, si2))
            elif (tag == EDiffActions.EQUAL):
                # ak sa tvaria rovnako, chod do hlbky, porovnaj data
                for si1, si2 in zip(sequence1[i1:i2], sequence2[j1:j2]):
                    self.__diffElementsData(si1, si2, result)
                    

    def __diffElementsData(self, el1, el2, result):
        data1 = el1.GetData()
        data2 = el2.GetData()
        tuple1 = dictToTuple(data1)
        tuple2 = dictToTuple(data2)
        # dictionaries 
        if data1 == data2:
            #klasicke porovnanie dvoch dict, ak nahodou su celkom rovnake
            pass
        else:
            self.__diffData(el1, el2, tuple1, tuple2, result, [])
    
    def __diffData(self, el1, el2, tuple1, tuple2, result, dataPath):
        sm = SequenceMatcher(None, tuple1, tuple2)
        op = sm.get_opcodes()
        for tag, i1, i2, j1, j2 in op:
            if (tag == EDiffActions.EQUAL):
                pass
            elif (tag == EDiffActions.DELETE):
                # nieco bolo vymazane
                for seq in tuple1[i1:i2]:
                    result.append(CDiffResult(EDiffActions.DELETE, el1, seq, None, dataPath))
            elif (tag == EDiffActions.INSERT):
                for seq in tuple2[j1:j2]:
                    result.append(CDiffResult(EDiffActions.INSERT, el2, None, seq, dataPath))
                # nieco bolo pridane
                pass
            elif (tag == EDiffActions.REPLACE):
                #nieco bolo zmenene
                if (j2 - j1 > i2 - i1):
                    r = j2 - j1
                else :
                    r = i2 - i1
                for i in range(r):
                    try:
                        seq1 = tuple1[i1+i]
                    except :
                        seq1 = ()
                    try:
                        seq2 = tuple2[j1+i]
                    except:
                        seq2 = ()
                    if (seq2 == ()):
                        seq1 = (seq1,)
                    if (seq1 == ()):
                        seq2 = (seq2,)
                    try:
                        if type(seq1[0]) == type('') and type(seq1[1]) == type(u''):
                            myPath = copy.deepcopy(dataPath)
                            myPath.append(seq1[0])
                            result.append(CDiffResult(EDiffActions.MODIFY, el1, seq1, seq2, myPath))
                        else:
                            myPath = copy.deepcopy(dataPath)
                            print tuple1
                            print seq1
                            if type(seq1[0]) == type(''):
                                myPath.append(seq1[0])
                            elif type(tuple1[0]) != type(''):
                                myPath.append(tuple1.index(seq1))
                            
                            self.__diffData(el1, el2, seq1, seq2, result, myPath)
                    except:
                        myPath = copy.deepcopy(dataPath)
                        if type(seq2[0] == type('')):
                            myPath.append(seq2[0])
                        elif type(tuple2[0]) != type(''):
                            myPath.append(tuple1.index(seq2))
                        self.__diffData(el1, el2, seq1, seq2, result, myPath)
#                result.append(CDiffResult(EDiffActions.MODIFY, el1, tuple1[i1:i2], tuple2[j1:j2], dataPath))
                
    def __computeVisualDiff(self, diagram):
        pass
        