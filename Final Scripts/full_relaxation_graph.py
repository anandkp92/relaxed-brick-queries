import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF, SH
from rdflib import URIRef
from utils import *
from relationship_relaxation import *
from type_relaxation import *
import networkx
brick_graph = brickschema.Graph(load_brick=True)


def create_ordered_list(triples_copy):
    ordered_list = []
    for item in triples_copy:
        for item_i in item:
            item_new = item_i.split('#')[-1]
            ordered_list.append(item_new)
    ordered_list.sort()
    return ordered_list
                
def relax_triples(G, triples, rules, rule_names, level_itr, node_idx, k_node):
    
    for r_index in range(len(rules)):
        rule = rules[r_index]
    
        for i in range(len(triples)):
            triple = triples[i]
            relaxed_triples = rule(triple)
            print(relaxed_triples)
        
            if len(relaxed_triples) > 0:
                for relaxed_triple in relaxed_triples:
                    triples_copy = triples.copy()
                    triples_copy[i] = relaxed_triple
                    
                    #Checking to see if it exists within graph
                    ordered_list = create_ordered_list(triples_copy)
                    
                    if any(G.nodes.data()[node]['ordered_id'] == ordered_list for node in G) == False:
                        G.add_node(node_idx, query=triples_copy, ordered_id = ordered_list)
                        G.add_edge(k_node, node_idx, rule=rule_names[r_index], level=level_itr, triple=i)
                        node_idx+=1
                        #print('node pass')
                    else:
                        #print('node deleted')
                        pass
                        
    return G, node_idx

def relaxtion_graph(query, limit_level):
    rules = [ApplyRule_LowerClass, ApplyRule_SiblingClass, ApplyRule_UpperClass, apply_rule_variable_relationship,
             apply_rule_transitive_relationship]
    rule_names = ['lower', 'sibling', 'upper', 'relationship', 'transitive_relationship']
    
    if limit_level == True:
        limit_num = int(input('Enter desired level of relaxation:- '))
    else:
        limit_num = 10000000
                        
    triples = extract_triples(query)

    G = networkx.Graph()
    node_idx = 1
    ordered_list = create_ordered_list(triples)
    G.add_node(node_idx, query=triples, ordered_id = ordered_list)
    node_idx+=1
    G_old = G.copy()
        
    # Create First Layer
    start_node = node_idx
    level_itr = 1
    G_new, node_idx = relax_triples(G, triples, rules, rule_names, level_itr, node_idx, k_node=1)
    print('Level '+ str(level_itr) + ' complete')
    end_node = node_idx
    G_new = G.copy()

    while len(G_old) < len(G_new):
        level_itr += 1
        for k_node in range(start_node, end_node+1):
            query = G.nodes.data()[k_node]['query']
            triples = query.copy()
            G_old = G_new.copy()
            G_new, node_idx = relax_triples(G, triples, rules, rule_names, level_itr, node_idx, k_node)
        print('Level '+ str(level_itr) + 'complete')
        start_node = end_node+1
        end_node = node_idx
        if level_itr > limit_num:
            break

    return G_new

def main(query, limit_level=False, export=False):
    G_relaxed = relaxtion_graph(query, limit_level)
    print('Relaxed query graph generated')
    if export == True:
        # saving graph created above in gexf format, can be visualized using Gephi
        nx.write_gexf(G_relaxed, "full_relaxed_query.gexf")
        print('GEXF file generated')
        
    return G_relaxed
