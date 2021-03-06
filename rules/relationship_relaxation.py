import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef
from utils import *

brick_graph = brickschema.Graph(load_brick=True)
relationship_domain_range_map = get_relationship_domain_range_map()
shacl_relationship_map = get_shacl_relationship_map()

def apply_rule_variable_relationship(triple, triples=None):
    t0 = parse_entity(triple[0])
    t1 = parse_entity(triple[1])
    t2 = parse_entity(triple[2])
    
    if t1.lower() == 'a' or t1.lower() =='rdf:type' or t1 == RDF['type']:
        return []
    
    sub = None
    rel = None
    obj = None
        
    variable_subject = False
    variable_object = False
    
    sub = get_entity_with_namespace(t0)
    if t1[0] != '?':
        if t1 == 'a':
            rel = RDF['type']
        else:
            rel = get_entity_with_namespace(t1)
    obj = get_entity_with_namespace(t2)
    
    if sub is None and triples is not None:
        sub = get_type_from_triples(entity=t0, triples=triples)
    if obj is None and triples is not None:
        obj = get_type_from_triples(entity=t2, triples=triples)

    sub_super_classes = get_super_classes(entity=sub)
    obj_super_classes = get_super_classes(entity=obj)
    
    relaxed_triples = []
                
    for relationship in relationship_domain_range_map:
        
        d = relationship_domain_range_map.get(relationship, {}).get('domain', None)
        r = relationship_domain_range_map.get(relationship, {}).get('range', None)
        
        possible_relaxation = False

        ## first check if the relaxed triple matches the properties (domain, range) of the relationships
        
        if sub is None and obj is None:
            # if subject and object are variables (?x, ?y), all relationships are possible
            possible_relaxation = True
        elif sub is None:
            if r is None:
                possible_relaxation = True
            else:
                if r in obj_super_classes:
                    possible_relaxation = True
        elif obj is None:
            if d is None:
                possible_relaxation = True
            else:
                if d in sub_super_classes:
                    possible_relaxation = True
        else:
            if d is None and r is None:
                possible_relaxation = True
            elif d is None:
                if r in obj_super_classes:
                    possible_relaxation = True
            elif r is None:
                if d in sub_super_classes:
                    possible_relaxation = True
            else:
                if r in obj_super_classes and d in sub_super_classes:
                    possible_relaxation = True
        
        ## below is checking to ensure that the relaxed triple conforms to the shacl shapes
        if possible_relaxation:
            shacl_shapes = shacl_relationship_map.get(relationship, None)
            if shacl_shapes is not None:
                
                shape_condition = False
                for shape in shacl_shapes:
                    allowed_subject = shape.get('subject', None)
                    allowed_object = shape.get('object', None)
                     
                    #TODO: add conditions when sub, obj are none
                    if sub is not None and obj is not None:
                        if allowed_subject in sub_super_classes and allowed_object in obj_super_classes:
                            shape_condition = True
                    elif sub is not None:
                        if allowed_subject in sub_super_classes:
                            shape_condition = True
                    elif obj is not None:
                        if allowed_object in obj_super_classes:
                            shape_condition = True
                    else:
                        # if subject and object are variables (?x, ?y), all relationships are possible
                        shape_condition = True
                
                if not shape_condition:
                    possible_relaxation = False
                    
        if possible_relaxation:
            relaxed_triples.append([t0, parse_entity(relationship), t2])

    return relaxed_triples


def apply_rule_transitive_relationship(triple):
    t0 = parse_entity(triple[0])
    t1 = parse_entity(triple[1])
    t2 = parse_entity(triple[2])
    
    if t1.lower() == 'a' or t1.lower() =='rdf:type' or t1 == RDF['type']:
        return []
    
    if t1[-1] == '+':
        return []
    
    return [[t0, t1+'+', t2]]