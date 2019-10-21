from pyshacl import validate
from os import path

data_file = './graphs/SampleGraph.jsonld'
shape_file = './shapes/SampleShape.ttl'
data_file = path.abspath(data_file)
shape_file = path.abspath(shape_file)

shapes_file_format = 'turtle'
data_file_format = 'json-ld'


conforms, v_graph, v_text = validate(data_file, shacl_graph=shape_file,
                                     data_graph_format=data_file_format,
                                     shacl_graph_format=shapes_file_format,
                                     inference='rdfs', debug=True,
                                     serialize_report_graph=True)

print(conforms)
print(v_graph)
print(v_text)