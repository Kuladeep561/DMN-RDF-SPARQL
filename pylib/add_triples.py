from rdflib import *

def add_triples(dmn_Abox, ns, classes, properties, inputs, outputs, i):
    triples = [
        (inputs['activity'][i], RDF.type, classes['activity']),
        (inputs['activity'][i], properties['hasStartDate'], Literal(inputs.get('hasActivityStartDate')[i].strip('/"'), datatype=XSD.dateTime)),
        (outputs['hasInspection'][i], RDF.type, classes['inspection']),
        (outputs['hasInspection'][i], RDFS.comment, Literal(outputs.get('hasComments')[i], datatype=XSD.string)),
        (outputs['hasInspection'][i], properties['hasCodeOfConduct'], ns['dmn'][outputs['hasCodeOfConduct'][i]]),
        (outputs['hasResponsibleAgent'][i], RDF.type, classes['agent']),
        (outputs['hasInspection'][i], properties['hasResponsibleAgent'], ns['dmn'][outputs['hasResponsibleAgent'][i]]),
        (outputs['hasApprover'][i], RDF.type, classes['agent']),
        (outputs['hasInspection'][i], properties['hasApprover'], ns['dmn'][outputs['hasApprover'][i]]),
        (outputs['hasInspection'][i], properties['hasFrequency'], Literal(outputs.get('hasFrequency')[i], datatype=XSD.string)),
        (outputs['hasInspection'][i], properties['hasStartDate'], Literal(outputs.get('hasInspectionStartDate')[i].strip('/"'), datatype=XSD.dateTime)),
        (outputs['hasInspection'][i], properties['hasEndDate'], Literal(outputs.get('hasInspectionEndDate')[i].strip('/"'), datatype=XSD.dateTime)),
        (outputs['hasLocation'][i], RDF.type, classes['location']),
        (outputs['hasInspection'][i], properties['hasLocation'], ns['dmn'][outputs['hasLocation'][i]]),
        (outputs['hasInspectionProcedure'][i], RDF.type, classes['inspection_procedure']),
        (outputs['hasInspection'][i], properties['hasInspectionProcedure'], ns['dmn'][outputs['hasInspectionProcedure'][i]]),
    ]

    mat = inputs.get('material', [])[i]
    if mat.lower() == 'concrete':
        triples.extend([
            (mat, RDF.type, classes['composite_material']),
            (mat, properties['hasActivity'], ns['dmn'][inputs['activity'][i]]),
        ])
    else:
        triples.extend([
            (mat, RDF.type, classes['material']),
            (mat, properties['hasActivity'], ns['dmn'][inputs['activity'][i]]),
        ])

    for subject, predicate, obj in triples:
        dmn_Abox.add((ns['dmn'][subject], predicate, obj))


    return dmn_Abox