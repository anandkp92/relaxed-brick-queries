import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef
import networkx
from utils import *
from relaxation_graphs.full_relaxation_graph import *
import datetime

brick_graph = brickschema.Graph(load_brick=True)

def get_evaluation_metrics(file, query, max_level=-1):
    g = brickschema.Graph(load_brick=True)
    g.load_file(file)
    g.expand(profile="owlrl")
    select_statement = query.split("{")[0] + "{\n"
    
    relaxation_start_time = datetime.datetime.now()
    G = get_relaxed_graph(query=query, max_level=max_level)
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
    for idx, node in G.nodes().data():
        level = node['level']
        if level > max_level:
            max_level = level

    min_level_with_data = -1
    min_nodes_with_data = []        
    for node_uuid in nodes_with_data:
        level = G.nodes()[node_uuid]['level']
        if min_level_with_data == -1:
            min_level_with_data = level
            min_nodes_with_data = [node_uuid]
        elif min_level_with_data > level:
            min_level_with_data = level
            min_nodes_with_data = [node_uuid]
        elif min_level_with_data == level:
            min_nodes_with_data.append(node_uuid)
    
    metrics = {}
    metrics['number_relaxed_queries'] = len(G.nodes())
    metrics['number_queries_with_data'] = len(nodes_with_data)
    metrics['max_level'] = max_level
    
    relaxation_time = (relaxation_end_time - relaxation_start_time).total_seconds()
    querying_time = (querying_end_time - querying_start_time).total_seconds()
    metrics['relaxation_time'] = relaxation_time
    metrics['querying_time'] = querying_time
    metrics['total_time'] = relaxation_time+querying_time

    metrics['minimum_edits_for_result'] = min_level_with_data
    metrics['graph'] = G
    return metrics