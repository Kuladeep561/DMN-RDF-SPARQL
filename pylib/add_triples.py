from rdflib import*

def create_individuals(df, graph, ns, classes):
    for index, row in df.iterrows():
        for column in df.columns:
            if column in classes:
                individual_value = row[column]
                individual_uri = URIRef(f"{ns['dmn']}{individual_value}")
                class_uri = classes[column]
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

