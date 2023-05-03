from rdflib import *
from pyshacl import validate
from pylib.DMN_reader import *
from pylib.shacl_validation import *
from pylib.add_triples import *
from pylib.init_classes_and_properties import *


#parse DMN table as xml
dmn_filepath = r"C:\Users\kuk\OneDrive - Technische Universität Ilmenau\Thesis\Camunda\curinginspections_3.dmn"
parser = DMNParser(dmn_filepath)

#get DMN hit policy
hit_policy = parser.extract_hit_policy()

inputs, outputs = parser.extract_inputs_outputs()

#Final inputs and Outputs
inputs, outputs = parser.FEEL_converter(inputs, outputs)


if (hit_policy.lower() == "collect"):

    # Load the ontology
    ontology = Graph().parse("./graphs/DMN-RDF-Dicon-OCQA-Tbox.ttl", format="ttl")
    namespace = dict(ontology.namespaces())
    ns = {k: Namespace(v) for k, v in namespace.items()} 
    classes, properties = init_classes_and_properties(ns)
    

    #initialize the datagraph
    dmn_Abox = Graph()

    # Bind the namespaces with their prefixes in dmn_Abox
    for prefix, uri in namespace.items():
        dmn_Abox.bind(prefix, uri)

    # Process inputs and outputs
    for i, mat in enumerate(inputs.get('material', [])):
        add_triples(dmn_Abox, ns, classes, properties, inputs, outputs, i)
    
    #serialize the Abox into ttl file
    dmn_Abox.serialize("./inferred graphs/DMN-RDF-Abox.ttl", format='turtle')
      
    #**SHACL validation and SPARQL construct**#

    #Load  example files
    example_building = Graph().parse("./graphs/Data.ttl", format="ttl")


    # Combine the graphs
    combined_graph = ontology + dmn_Abox + example_building

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




