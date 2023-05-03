import pyshacl
import rdflib

def load_shacl_shapes(file_path):
    shapes_graph = rdflib.Graph()
    shapes_graph.parse(file_path, format='turtle')
    return shapes_graph

def load_building_data(file_path):
    data_graph = rdflib.Graph()
    data_graph.parse(file_path, format='turtle')
    return data_graph

def validate_building_data(building_data_graph, shacl_shapes_graph):
    conforms, result_graph, result_text = pyshacl.validate(
        building_data_graph, shacl_graph=shacl_shapes_graph, inference='rdfs', abort_on_first=False)

    if not conforms:
        print("Validation failed:")
        print(result_text)
        return False
    else:
        print("Validation succeeded.")
        return True
