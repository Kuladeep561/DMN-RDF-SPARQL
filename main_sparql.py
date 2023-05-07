from pyshacl import validate
from pylib.DMNParser import *
from pylib.shacl_validation import *
from pylib.add_triples import *
from pylib.init_classes_and_properties import *
from pylib.add_triples import *
from pylib.create_rule import *


### **parse DMN table as xml and create DataFrame**###

dmn_filepath = r"C:\Users\kuk\OneDrive - Technische Universität Ilmenau\Thesis\Camunda\curinginspections_5.dmn"


parser = DMNParser(dmn_filepath)
hit_policy = parser.extract_hit_policy()  # get DMN hit policy
inputs, outputs = parser.extract_inputs_outputs()
inputs, outputs = parser.FEEL_converter(inputs, outputs)  # Final inputs and Outputs

df_inputs, df_outputs = parser.dmn_as_dataframe(inputs, outputs)  # Convert into dataframes
#f_io = pd.concat([df_inputs, df_outputs], axis=1)  # Merge two DFs


###!SHACL validation and SPARQL construct based on hit polocy**###

if (hit_policy.lower() == "collect"):

    ontology = Graph().parse("./graphs/DMN-RDF-Dicon-OCQA-Tbox.ttl",
                             format="ttl")
    example_building = Graph().parse("./graphs/Duplex_A_20110505_LBD.ttl",
                                     format="ttl")
    
    _combined = ontology + example_building
    namespace = dict(_combined.namespaces())
    ns = {k: Namespace(v) for k, v in namespace.items()}
    
    classes, literals, relationships = init_classes_and_properties(ns)

    inferred_graph = Graph()
    for index, row in df_inputs.iterrows():
        g1 = Graph()  # Initialize the graph for the current row
        
        create_individuals_for_row(row,g1,classes)
        _combined = _combined + g1
        query = generate_select_query(row, classes, ns)
        query_result = _combined.query(query)

        if(query_result):
            output_row = df_outputs.iloc[index]
            
            create_individuals_for_row(output_row,g1, classes)          
            g1 = link_individual_for_row(row, g1, ns, classes, relationships, literals)
            subjects = [row[0] for row in query_result]
            construct_query = generate_construct_query(subjects, ns)
            
            construct_query_result = g1.query(construct_query)
            inferred_graph+=g1
            inferred_graph+=construct_query_result

        else:
            print("no matching data")
    combined_graph = _combined + inferred_graph
    combined_graph.serialize(destination="./inferred graphs/new_inspections.ttl", format="ttl")
    print("Validation hasbeen completed and a graph also created")

else:
    raise ValueError(f"The hit policy is: {hit_policy}, it is unsupported. The script supports only 'COLLECT'")

