
from rdflib import *
from pyshacl import validate
from DMN_reader import *
from shacl_validation import *




#parse DMN table as xml
dmn_filepath = r"C:\Users\kuk\OneDrive - Technische Universität Ilmenau\Thesis\Camunda\curinginspections_3.dmn"
parser = DMNParser(dmn_filepath)

#get DMN hit policy
hit_policy = parser.extract_hit_policy()

inputs, outputs = parser.extract_inputs_outputs()

inputs, outputs = parser.FEEL_converter(inputs, outputs)
# inputs, outputs =parser.extract_text_between_parentheses()


if (hit_policy.lower() == "collect"):

    # Load the ontology
    ontology = Graph().parse("./graphs/DMN-RDF-Dicon-OCQA-Tbox.ttl", format="ttl")
    dmn_Abox = Graph()

    namespace = dict(ontology.namespaces())
    ns = {k: Namespace(v) for k, v in namespace.items()} 

    # Bind the namespaces with their prefixes in dmn_Abox
    for prefix, uri in namespace.items():
        dmn_Abox.bind(prefix, uri)

    #Initializing the classes
    composite_material = ns['dicm'].CompositeMaterial
    material = ns['dicm'].Material
    activity = ns['dicp'].Activity
    inspection = ns['ocqa'].Inspection
    IScode = ns['dmn'].ISCode
    agent = ns['dica'].Agent
    location = ns['dice'].Location
    inspection_procedure = ns['ocqa'].InspectionProcedure

    #Initializing the properties
    hasMaterial = ns['dicm'].hasMaterial
    hasCodeOfConduct = ns['dmn'].hasCodeOfConduct
    hasActivity = ns['dmn'].hasActivity
    hasStartDate = ns['dmn'].hasStartDate
    hasEndDate = ns['dmn'].hasEndDate
    hasResponsibleAgent = ns['dica'].hasResponsibleAgent
    hasApprover = ns['dica'].hasApprover
    hasFrequency = ns['dmn'].hasFrequency
    hasLocation = ns['dmn'].hasLocation
    hasInspectionProcedure = ns['ocqa'].hasInspectionProcedure
    
    
    for i, mat in enumerate(inputs.get('material', [])):
        act = inputs['activity'][i]
        dmn_Abox.add((ns['dmn'][act], RDF.type, activity))
        dmn_Abox.add((ns['dmn'][act], hasStartDate, Literal(inputs.get('hasActivityStartDate')[i].strip('/"'), datatype=XSD.dateTime)))

        inspect = outputs['hasInspection'][i]
        dmn_Abox.add((ns['dmn'][inspect], RDF.type, inspection ))
        dmn_Abox.add((ns['dmn'][inspect], RDFS.comment, Literal(outputs.get('hasComments')[i],datatype=XSD.string)))

        code = outputs['hasCodeOfConduct'][i]
        dmn_Abox.add((ns['dmn'][code], RDF.type, IScode))
        dmn_Abox.add((ns['dmn'][inspect],hasCodeOfConduct,ns['dmn'][code]))

        ra = outputs['hasResponsibleAgent'][i]
        dmn_Abox.add((ns['dmn'][ra], RDF.type, agent))
        dmn_Abox.add((ns['dmn'][inspect],hasResponsibleAgent,ns['dmn'][ra]))

        apprv = outputs['hasApprover'][i]
        dmn_Abox.add((ns['dmn'][apprv], RDF.type, agent))
        dmn_Abox.add((ns['dmn'][inspect],hasApprover,ns['dmn'][apprv]))

        dmn_Abox.add((ns['dmn'][inspect], hasFrequency, Literal(outputs.get('hasFrequency')[i],datatype=XSD.string)))
        dmn_Abox.add((ns['dmn'][inspect], hasStartDate, Literal(outputs.get('hasInspectionStartDate')[i].strip('/"'), datatype=XSD.dateTime)))
        dmn_Abox.add((ns['dmn'][inspect], hasEndDate, Literal(outputs.get('hasInspectionEndDate')[i].strip('/"'), datatype=XSD.dateTime)))

        
        loc = outputs['hasLocation'][i]
        dmn_Abox.add((ns['dmn'][loc], RDF.type, location))
        dmn_Abox.add((ns['dmn'][inspect],hasLocation,ns['dmn'][loc]))

        process = outputs['hasInspectionProcedure'][i]
        dmn_Abox.add((ns['dmn'][process], RDF.type, inspection_procedure))
        dmn_Abox.add((ns['dmn'][inspect],hasInspectionProcedure,ns['dmn'][process]))

        if mat.lower() == 'concrete':
            dmn_Abox.add((ns['dmn'][mat], RDF.type, composite_material))
            dmn_Abox.add((ns['dmn'][mat], hasActivity, ns['dmn'][act]))
        else:
            dmn_Abox.add((ns['dmn'][mat], RDF.type, material))
            dmn_Abox.add((ns['dmn'][mat], hasActivity, ns['dmn'][act]))

    dmn_Abox.serialize("./inferred graphs/DMN-RDF-Abox.ttl", format='turtle')
      
    ##############################################################
    #Load data, and example files
    #DMNgraph = Graph().parse("./inferred graphs/DMN-RDF-Abox.ttl", format="ttl")
    data = Graph().parse("./graphs/Data.ttl", format="ttl")


    # Combine the graphs
    combined_graph = ontology + dmn_Abox + data

    # Load the SHACL rules graph
    rules_graph = Graph().parse("./graphs/rules.ttl", format="ttl")

    # Validate the combined graph and apply the rules
    conforms, inferred_graph, string  = validate(combined_graph, shacl_graph=rules_graph, 
                                                 data_graph_format='turtle', shacl_graph_format='turtle', 
                                                 debug=True, advanced=True, inplace=True)

    # Merge the original graph with the inferred graph
    new_graph = combined_graph + inferred_graph
    
    # Bind the 'dmn' namespace with the desired prefix in the new_graph
    dmn_namespace = ns['dmn']
    new_graph.bind("dmn", dmn_namespace)

    # Save the new graph to a new file
    new_graph.serialize(destination="./inferred graphs/Inferred_Rules.ttl", format="ttl")

    
else:
    raise ValueError(f"The hit policy is: {hit_policy}, it is unsupported. Script supports only 'COLLECT'")




