def init_classes_and_properties(ns):
    classes = {
        'composite_material': ns['dicm'].CompositeMaterial,
        'material': ns['dicm'].Material,
        'activity': ns['dicp'].Activity,
        'inspection': ns['ocqa'].Inspection,
        'IScode': ns['dmn'].ISCode,
        'agent': ns['dica'].Agent,
        'location': ns['dice'].Location,
        'inspection_procedure': ns['ocqa'].InspectionProcedure,
    }

    properties = {
        'hasMaterial': ns['dicm'].hasMaterial,
        'hasCodeOfConduct': ns['dmn'].hasCodeOfConduct,
        'hasActivity': ns['dmn'].hasActivity,
        'hasStartDate': ns['dmn'].hasStartDate,
        'hasEndDate': ns['dmn'].hasEndDate,
        'hasResponsibleAgent': ns['dica'].hasResponsibleAgent,
        'hasApprover': ns['dica'].hasApprover,
        'hasFrequency': ns['dmn'].hasFrequency,
        'hasLocation': ns['dmn'].hasLocation,
        'hasInspectionProcedure': ns['ocqa'].hasInspectionProcedure,
    }

    return classes, properties
