#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef
from utils import *

brick_graph = brickschema.Graph(load_brick=True)

def ApplyRule_LowerClass(triple):

    t0 = parse_entity(triple[0])
    t1 = parse_entity(triple[1])
    t2 = parse_entity(triple[2])
    
    if t1 != 'a' and t1.lower() !='rdf:type':
        return []
    
    if t2[0] == '?':
        return []
    
    obj_ns = get_namespace(t2)

    if ':' in t2:
        obj_entity = t2.split(':')[1]
    elif '#' in t2:
        obj_entity = t2.split('#')[1]
    obj = obj_ns[obj_entity]
    
    relaxed_triples = []
    for lower_class in brick_graph.subjects(predicate=RDFS['subClassOf'], object=obj):
        if isinstance(lower_class, URIRef):
            relaxed_triples.append([t0,  t1, lower_class])
    return relaxed_triples

def ApplyRule_UpperClass(triple):
    
    t0 = parse_entity(triple[0])
    t1 = parse_entity(triple[1])
    t2 = parse_entity(triple[2])
    
    if t1 != 'a' and t1.lower() !='rdf:type':
        return []
    
    if t2[0] == '?':
        return []
    
    obj_ns = get_namespace(t2)
    if ':' in t2:
        obj_entity = t2.split(':')[1]
    elif '#' in t2:
        obj_entity = t2.split('#')[1]
    obj = obj_ns[obj_entity]

    relaxed_triples = []
    for upper_class in brick_graph.objects(subject=obj, predicate=RDFS['subClassOf']):
        if isinstance(upper_class, URIRef):
            relaxed_triples.append([t0, t1, upper_class])
    return relaxed_triples

def ApplyRule_SiblingClass(triple):
    
    t0 = parse_entity(triple[0])
    t1 = parse_entity(triple[1])
    t2 = parse_entity(triple[2])
    
    if t1 != 'a' and t1.lower() !='rdf:type':
        return []
    
    if t2[0] == '?':
        return []
    
    relaxed_triples = []
    upper_class_triples = ApplyRule_UpperClass(triple)
    for upper_class_triple in upper_class_triples:
#         upper_class_triple[2] = 'Brick:'+upper_class_triple[2].split('#')[1]
        relaxed_triples+=ApplyRule_LowerClass(upper_class_triple)
    return relaxed_triples