from rdflib import*
from pylib.add_triples import *
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

