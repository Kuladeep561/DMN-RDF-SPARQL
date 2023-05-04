from rdflib import RDFS, XSD

def init_classes_and_properties(ns):
    classes = {
        'CompositeMaterial': ns['dicm'].CompositeMaterial
        ,'Material': ns['dicm'].Material
        ,'Activity': ns['dicp'].Activity
        ,'SubActivity':ns['dmn'].SubActivity
        ,'Inspection': ns['ocqa'].Inspection
        ,'InspectionEquipment': ns['ocqa'].InspectionEquipment
        ,'InspectionProcedure': ns['ocqa'].InspectionProcedure
        ,'ISCode': ns['dmn'].ISCode
        ,'Agent': ns['dica'].Agent
        ,'Location': ns['dice'].Location
    }

    literals = {
        'hasComment': XSD.string
        ,'hasStartDate':XSD.dateTime
        ,'hasEndDate':XSD.dateTime
        ,'hasActivityStartDate':XSD.dateTime
}

    relationships = {
         ns['dice'].isPartOf:('Inspection','ISCode')
        ,ns['dica'].hasAgent:('Inspection','Agent')
        ,ns['ocqa'].hasInspectionEquipment:('Inspection','InspectionEquipment')
        ,ns['dicp'].hasLocation:('Inspection','Location')
        ,ns['ocqa'].hasInspectionProcedure:('Inspection','InspectionProcedure')
        ,ns['dmn'].hasStartDate:('Inspection','hasStartDate')
        ,ns['dmn'].hasEndDate:('Inspection','hasEndDate')
        ,ns['dmn'].hasFrequency:('Inspection','hasFrequency')
        ,ns['dmn'].hasActivity:('Material','Activity')
        ,ns['dicp'].hasSubActivity:('Activity','SubActivity')
        ,ns['ocqa'].hasInspection:('SubActivity','Inspection')
        ,ns['dmn'].hasStartDate:('SubActivity','hasActivityStartDate')
        ,RDFS.comment:('Inspection','hasComment')




    }
    return classes, literals, relationships
