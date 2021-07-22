import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF, SH
from rdflib import URIRef
from utils import *
from rules.relationship_relaxation import *
from rules.type_relaxation import *
import networkx
import itertools
import uuid

brick_graph = brickschema.Graph(load_brick=True)

def get_fast_relaxed_graph(query, max_level=-1):
    triples = extract_triples(query)
    relaxation_matrix = []
    level_matrix = []
    for triple in triples:
        t1 = triple[1]
        relaxation = []
        levels = []
        level = 0
        if t1 == 'a' or t1 == 'rdf:type':
            t2 = get_entity_with_namespace(triple[2])
            super_classes = get_super_classes(entity=t2)
            for super_class in super_classes:
                if parse_entity(super_class) == t2:
                    levels.append(0)
                else:
                    levels.append(level)
                    level+=1
                relaxation.append([triple[0], t1, parse_entity(super_class)])

        else:
            relaxation = apply_rule_variable_relationship(triple=triple, triples=triples)
            for i in range(len(relaxation)):
                if relaxation[i][1] == triple[1]:
                    levels.append(0)
                else:
                    levels.append(1)

            transitive_relations = []
            for i in range(len(relaxation)):
                transitive_relations.append(apply_rule_transitive_relationship(triple=relaxation[i])[0])
                levels.append(levels[i]+1)
            relaxation = relaxation+transitive_relations
        relaxation_matrix.append(relaxation)
        level_matrix.append(levels)
        
    ns = uuid.uuid4()
    num_nodes=0
    G = networkx.Graph()
    
    origin_uuid = uuid.uuid3(namespace=ns, name=str(triples))
    G.add_node(origin_uuid, query=triples, node_id=num_nodes, level=0)
    num_nodes+=1

    graph_levels = list(itertools.product(*level_matrix))
    node_idx = 0
    for element in itertools.product(*relaxation_matrix):
        level = sum(graph_levels[node_idx])
        node_idx+=1
        
        if max_level >= 0 and level >max_level:
            continue
        node_uuid = uuid.uuid3(namespace=ns, name=str(element))

        if node_uuid not in G.nodes():
            G.add_node(node_uuid, query=element, node_id=num_nodes, level=level)
    #         G.add_edge(source_uuid, node_uuid, rule=rule_names[r_index], triple=i, source_node_id=source_node_id, destn_node_id=num_nodes)
            num_nodes+=1
    
    return G

    