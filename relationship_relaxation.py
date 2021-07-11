import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef
from utils import *

brick_graph = brickschema.Graph(load_brick=True)
relationship_domain_range_map = get_relationship_domain_range_map()

def apply_rule_variable_relationship(triple):
    t0 = triple[0]
    t1 = triple[1]
    t2 = triple[2]
    
    sub = None
    rel = None
    obj = None
        
    variable_subject = False
    variable_object = False
    
    if t0[0] != '?':
        sub_ns = get_namespace(t0.split(':')[0])
        sub_entity = t0.split(':')[1]
        sub = sub_ns[sub_entity]
        
    if t1[0] != '?':
        if t1 == 'a':
            rel = RDF['type']
        elif ':' in t1:
            rel_ns = get_namespace(t1.split(':')[0])
            rel_entity = t1.split(':')[1]
            rel = rel_ns[rel_entity]
        else:
            rel_ns = get_namespace(t1)
            rel_entity = t1
            rel = rel_ns[rel_entity]
        
    if t2[0] != '?':
        obj_ns = get_namespace(t2.split(':')[0])
        obj_entity = t2.split(':')[1]
        obj = obj_ns[obj_entity]

    sub_super_classes = get_super_classes(entity=sub)
    obj_super_classes = get_super_classes(entity=obj)
    
    relaxed_triples = []
                
    for relationship in relationship_domain_range_map:
        
        d = relationship_domain_range_map.get(relationship, {}).get('domain', None)
        r = relationship_domain_range_map.get(relationship, {}).get('range', None)
        
        if sub is None and obj is None:
            relaxed_triples.append([t0, relationship, t2])
        elif sub is None:
            if r is None:
                relaxed_triples.append([t0, relationship, t2])
            else:
                if r in obj_super_classes:
                    relaxed_triples.append([t0, relationship, t2])
        elif obj is None:
            if d is None:
                relaxed_triples.append([t0, relationship, t2])
            else:
                if d in sub_super_classes:
                    relaxed_triples.append([t0, relationship, t2])
        else:
            if d is None and r is None:
                relaxed_triples.append([t0, relationship, t2])
            elif d is None:
                if r in obj_super_classes:
                    relaxed_triples.append([t0, relationship, t2])
            elif r is None:
                if d in sub_super_classes:
                    relaxed_triples.append([t0, relationship, t2])
            else:
                if r in obj_super_classes and d in sub_super_classes:
                    relaxed_triples.append([t0, relationship, t2])

    return relaxed_triples