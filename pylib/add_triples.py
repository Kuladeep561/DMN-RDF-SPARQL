from rdflib import*
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
        graph.add((subject_uri, relationship, object_uri))

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
