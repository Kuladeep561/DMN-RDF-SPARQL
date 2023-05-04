from rdflib import*

def create_individuals(df, graph, class_and_individual_ns_mapping):
    for column in df.columns:
        if column in class_and_individual_ns_mapping:
            class_uri, namespace = class_and_individual_ns_mapping[column]
            for value in df[column].unique():
                individual_uri = URIRef(f"{namespace}{value}")
                graph.add((individual_uri, RDF.type, class_uri))
            


def link_individuals(df, graph, ns, relationships, literals=None):
    if literals is None:
        literals = {}
    
    for index, row in df.iterrows():
        for relationship, related_columns in relationships.items():
            subject_column, object_column = related_columns
            subject_value = row[subject_column]
            subject_uri = URIRef(f"{ns['dmn']}{subject_value}")

            if object_column in literals:
                object_value = row[object_column]
                object_datatype = literals[object_column]
                object_literal = Literal(object_value, datatype=object_datatype)
                graph.add((subject_uri, relationship, object_literal))
            else:
                object_value = row[object_column]
                object_uri = URIRef(f"{ns['dmn']}{object_value}")
                graph.add((subject_uri, relationship, object_uri))
    
    return graph

