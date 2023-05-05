from rdflib import RDFS, XSD

def init_classes_and_properties(ns):
    class_and_individual_ns_mapping  = {
        'CompositeMaterial': (ns['dicm'].CompositeMaterial, ns['dmn'])
        ,'Material': (ns['dicm'].Material, ns['dmn'])
        ,'Activity': (ns['dicp'].Activity, ns['dmn'])
        ,'SubActivity':(ns['dmn'].SubActivity, ns['dmn'])
        ,'Inspection': (ns['ocqa'].Inspection, ns['dmn'])
        ,'InspectionEquipment': (ns['ocqa'].InspectionEquipment, ns['dmn'])
        ,'InspectionProcedure': (ns['ocqa'].InspectionProcedure, ns['dmn'])
        ,'ISCode': (ns['dmn'].ISCode, ns['dmn'])
        ,'Agent': (ns['dica'].Agent, ns['dmn'])
        ,'Location': (ns['dice'].Location, ns['dmn'])
    }

    literals = {
        'hasComment': XSD.string
        ,'hasStartDate':XSD.dateTime
        ,'hasEndDate':XSD.dateTime
        ,'hasActivityStartDate':XSD.dateTime
}

    class_and_relations_mapping = {
         ns['dice'].isPartOf:('Inspection','ISCode')
        ,ns['dica'].hasAgent:('Inspection','Agent')
        ,ns['ocqa'].hasInspectionEquipment:('Inspection','InspectionEquipment')
        ,ns['dicp'].hasLocation:('Inspection','Location')
        ,ns['ocqa'].hasInspectionProcedure:('Inspection','InspectionProcedure')
        ,ns['dmn'].hasStartDate:('Inspection','hasStartDate')
        ,ns['dmn'].hasEndDate:('Inspection','hasEndDate')
        ,ns['dmn'].hasFrequency:('Inspection','hasFrequency')
        #,ns['dmn'].hasActivity:('Material','Activity')
        ,ns['dicp'].hasSubActivity:('Activity','SubActivity')
        ,ns['ocqa'].hasInspection:('SubActivity','Inspection')
        ,ns['dmn'].hasStartDate:('SubActivity','hasActivityStartDate')
        ,RDFS.comment:('Inspection','hasComment')




    }
    return class_and_individual_ns_mapping, literals, class_and_relations_mapping
