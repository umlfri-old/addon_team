'''
Created on 17.4.2010

@author: Peterko
'''
def Indent(elem, level=0):
    """
    The indent function is a variant of the one in Fredrik Lundh's effbotlib.
    This function make XML Tree more human friendly.
    
    @param  elem: XML element to parse
    @type   elem: L{Element<xml.etree.ElementTree.Element>}
    
    @param  level: level of element
    @type   level: integer
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            Indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i