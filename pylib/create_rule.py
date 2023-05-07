from rdflib import*
from itertools import count

def create_individuals_for_row(row, graph, class_and_individual_ns_mapping):
    for column, value in row.items():
        if column in class_and_individual_ns_mapping:
            class_uri, namespace = class_and_individual_ns_mapping[column]
            individual_uri = URIRef(f"{namespace}{value}")
            graph.add((individual_uri, RDF.type, class_uri))
    return graph

def link_individual_for_row(row, graph, ns, class_and_individual_ns_mapping, relationships, literals=None):
    if literals is None:
        literals = {}
    
    for relationship, related_columns in relationships.items():
        subject_column, object_column = related_columns

        if subject_column not in row or object_column not in row:
            continue
        subject_value = row[subject_column]

        if subject_column in class_and_individual_ns_mapping:
            subject_ns = class_and_individual_ns_mapping[subject_column][1]
        else:
            subject_ns = ns['dmn']
        subject_uri = URIRef(f"{subject_ns}{subject_value}")

        if object_column in literals:
            object_value = row[object_column]
            object_datatype = literals[object_column]
            object_literal = Literal(object_value, datatype=object_datatype)
            graph.add((subject_uri, relationship, object_literal))
        else:
            object_value = row[object_column]
            if object_column in class_and_individual_ns_mapping:
                object_ns = class_and_individual_ns_mapping[object_column][1]
            else:
                object_ns = ns['dmn']
            object_uri = URIRef(f"{object_ns}{object_value}")
            graph.add((subject_uri, relationship, object_uri))

    return graph


def generate_select_query( row, classes, ns):
    # Generate the PREFIX declarations
    prefix_declarations = "\n".join([f"PREFIX {prefix}: <{uri}>" for prefix, uri in ns.items()])

    triple_patterns = ""
    for i, (col, value) in enumerate(row.items()):
        class_uri, namespace = classes[col]
        triple_patterns += f"?{i + 1} <{namespace}{value}> ;\n"

    triple_patterns = triple_patterns.strip()[:-1]  # Remove the last semicolon and newline

    select_query = f"""
        {prefix_declarations}

        SELECT ?elements
        WHERE {{
            ?elements {triple_patterns} .
        }}
    """

    return select_query

def generate_construct_query(subjects, ns):
    prefix_declarations = "\n".join([f"PREFIX {prefix}: <{uri}>" for prefix, uri in ns.items()])
    subjects_values = " ".join([f"<{subject}>" for subject in subjects])

    sparql_construct_query = f"""
        {prefix_declarations}
        CONSTRUCT {{
            ?subject ocqa:hasInspection ?inspections
        }}
        WHERE {{
            VALUES ?subject {{ {subjects_values} }}
            ?inspections a ocqa:Inspection .
        }}
    """

    return sparql_construct_query



def construct_sparql(ontology, example, df_inputs, df_outputs, literals, class_and_individual_ns_mapping, relationships):
    namespace = dict(ontology.namespaces())
    ns = {k: Namespace(v) for k, v in namespace.items()}

    combined = ontology+example
    
    inferred = Graph()  # Graph to store the final result
    c = count(1)

    for index, row in df_inputs.iterrows():
        _temp = Graph()  # Initialize the graph for the current row

        # Create individuals for the current row in inputs
        _temp = create_individuals_for_row(_temp, row, class_and_individual_ns_mapping)
        combined = combined + _temp
