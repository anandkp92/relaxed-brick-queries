import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef
import networkx
from utils import *
from relaxation_graphs.full_relaxation_graph import *
import datetime

brick_graph = brickschema.Graph(load_brick=True)

def get_evaluation_metrics(file, query):
    g = brickschema.Graph(load_brick=True)
    g.load_file(file)
    g.expand(profile="owlrl")
    select_statement = query.split("{")[0] + "{\n"
    
    relaxation_start_time = datetime.datetime.now()
    G = get_relaxed_graph(query=query)
    relaxation_end_time = datetime.datetime.now()
    
    querying_start_time = datetime.datetime.now()
    nodes_with_data = []
    for uuid, node in G.nodes().data():
        brick_query = generate_brick_query_from_node(node['query'], select_statement=select_statement)
        res = run_brick_query(building_model=g, query=brick_query)
        if len(res) > 0:
            nodes_with_data.append(uuid)
    querying_end_time = datetime.datetime.now()
    
    max_level = 0
    for level_data in G.edges().data('level'):
        if level_data[2] > max_level:
            max_level = level_data[2]
        
    min_level_with_data = -1
    min_nodes_with_data = []
    for edge in G.edges().data():
        if edge[1] in nodes_with_data:
            if min_level_with_data == -1:
                min_level_with_data = edge[2]['level']
                min_nodes_with_data = [edge[1]]
            elif min_level_with_data > edge[2]['level']:
                min_level_with_data = edge[2]['level']
                min_nodes_with_data = [edge[1]]
            elif min_level_with_data == edge[2]['level']:
                min_nodes_with_data.append(edge[1])
    
    metrics = {}
    metrics['number_relaxed_queries'] = len(G.nodes())
    metrics['number_queries_with_data'] = len(nodes_with_data)
    metrics['max_leve'] = max_level
    
    relaxation_time = (relaxation_end_time - relaxation_start_time).total_seconds()
    querying_time = (querying_end_time - querying_start_time).total_seconds()
    metrics['relaxation_time'] = relaxation_time
    metrics['querying_time'] = querying_time
    metrics['total_time'] = relaxation_time+querying_time

    metrics['minimum_edits_for_result'] = min_level_with_data
    metrics['graph'] = G
    return metrics