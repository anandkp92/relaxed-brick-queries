import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF, SH
from rdflib import URIRef
from utils import *
from rules.relationship_relaxation import *
from rules.type_relaxation import *
import networkx
import uuid

brick_graph = brickschema.Graph(load_brick=True)

def get_optimized_relaxed_graph(query, building_model, max_level=-1):
    triples = extract_triples(query)
    select_statement = query.split("{")[0] + "{\n"
    
    rules = [ApplyRule_UpperClass, apply_rule_variable_relationship, apply_rule_transitive_relationship]
    rule_names = ['upper', 'relationship', 'transitive_relationship']

    G = networkx.Graph()
    ns = uuid.uuid4()

    num_nodes = 0
    origin_uuid = uuid.uuid3(namespace=ns, name=str(sorted(triples)))
    G.add_node(origin_uuid, query=sorted(triples), node_id=num_nodes, level=0)
    num_nodes+=1
    results = {}
    
    brick_query = generate_brick_query_from_node(triples, select_statement=select_statement)
    res = run_brick_query(building_model=building_model, query=brick_query)
    results[origin_uuid] = res
    if len(res) == 0:
        nodes_to_parse = [origin_uuid]
    else:
        nodes_to_parse = []

    already_parsed_uuids = []
    level = 1

    while len(nodes_to_parse) > 0:
        if max_level >= 0 and level > max_level:
            return G, results
        new_nodes_to_parse = []

        for source_uuid in nodes_to_parse:
            triples = G.nodes().data()[source_uuid].get('query')
            source_node_id = G.nodes.data()[source_uuid].get('node_id')
            already_parsed_uuids.append(source_uuid)

            for r_index in range(len(rules)):
                rule = rules[r_index]

                for i in range(len(triples)):
                    triple = sorted(triples)[i]
                    if rule_names[r_index] == 'relationship':
                        relaxed_triples = rule(triple, triples=triples)
                    else:
                        relaxed_triples = rule(triple)

                    if len(relaxed_triples) > 0:
                        for relaxed_triple in relaxed_triples:
                            triples_copy = triples.copy()
                            triples_copy[i] = relaxed_triple

                            ordered_list = sorted(triples_copy)
                            node_uuid = uuid.uuid3(namespace=ns, name=str(sorted(triples_copy)))

                            if node_uuid not in G.nodes():
                                brick_query = generate_brick_query_from_node(triples, select_statement=select_statement)
                                res = run_brick_query(building_model=building_model, query=brick_query)
                                
                                G.add_node(node_uuid, query=sorted(triples_copy), node_id=num_nodes, level=level)
                                G.add_edge(source_uuid, node_uuid, rule=rule_names[r_index], triple=i, source_node_id=source_node_id, destn_node_id=num_nodes)
                                results[node_uuid] = res
                                num_nodes+=1
                                
                                if len(res) == 0:
                                    new_nodes_to_parse.append(node_uuid)
                                

        nodes_to_parse = new_nodes_to_parse
        print("level {} completed".format(level))
        level+=1
    print("Graph completed")
    return G, results