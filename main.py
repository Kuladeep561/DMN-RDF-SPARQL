from pyshacl import validate
from pylib.DMNParser import *
from pylib.shacl_validation import *
from pylib.add_triples import *
from pylib.init_classes_and_properties import *
from pylib.add_triples import *


#parse DMN table as xml
dmn_filepath = r"C:\Users\kuk\Downloads\curinginspections-2-dmn.dmn"
parser = DMNParser(dmn_filepath)


hit_policy = parser.extract_hit_policy() #get DMN hit policy
inputs, outputs = parser.extract_inputs_outputs()
inputs, outputs = parser.FEEL_converter(inputs, outputs) #Final inputs and Outputs

df_inputs, df_outputs = parser.dmn_as_dataframe(inputs,outputs) #Convert into dataframes
df_io = pd.concat([df_inputs, df_outputs], axis=1) #Merge two DFs

###**SHACL validation and SPARQL construct based on hit polocy**### 
if (hit_policy.lower() == "collect"):

    ontology = Graph().parse("./graphs/DMN-RDF-Dicon-OCQA-Tbox.ttl", format="ttl")
    namespace = dict(ontology.namespaces())
    ns = {k: Namespace(v) for k, v in namespace.items()} 

    g = Graph() #initialize emptz graph to store individuals
    
    for prefix, uri in namespace.items():          # Bind the namespaces with their prefixes in dmn_Abox
        g.bind(prefix, uri)

    classes, literals, relationships = init_classes_and_properties(ns)
    create_individuals(df_io, g, ns, classes)
    DMN_graph = link_individuals(df_io, g, ns, relationships, literals)

    #serialize the Abox into ttl file
    DMN_graph.serialize("./inferred graphs/DMN-RDF-Abox.ttl", format='turtle')
    
    
    #**SHACL validation and SPARQL construct**#
    example_building = Graph().parse("./graphs/Data.ttl", format="ttl") #Load  example files


    # Combine the graphs
    combined_graph = ontology + DMN_graph + example_building

    # Load the SHACL rules graph
    rules_graph = Graph().parse("./graphs/WaterCuringRule.ttl", format="ttl")

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
    new_graph.serialize(destination="./inferred graphs/Inferred_WaterCuring_inspections.ttl", format="ttl")

else:
    raise ValueError(f"The hit policy is: {hit_policy}, it is unsupported. Script supports only 'COLLECT'")


