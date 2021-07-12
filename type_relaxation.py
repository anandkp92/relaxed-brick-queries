#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef
from utils import *

brick_graph = brickschema.Graph(load_brick=True)

def parse_triple(triple):
    t0 = triple[2]
    sub_ns = get_namespace(t0.split(':')[0])
    sub_entity = t0.split(':')[1]
    entity = sub_ns[sub_entity]
    
    return entity

def ApplyRule_LowerClass(entity):

    if entity is None:
        return []
    else:
        lower_class = []
        for subj, obj in brick_graph.subject_objects(predicate=RDFS.subClassOf):
            if obj in entity:
                thing = subj.rsplit('#')[-1]
                lower_class.append(thing)
        return lower_class

def ApplyRule_UpperClass(entity):

    upper_class = []
    if entity is None:
        return []
    else:
        super_classes = []
        for sup in brick_graph.transitive_objects(subject=entity, property=RDFS['subClassOf']):
            if isinstance(sup, URIRef):
                thing = sup.rsplit('#')[-1]
                super_classes.append(thing)
        #Retriving first layer of upper_class
        for upper in super_classes:
            sub = BRICK[upper]
            lower_list = ApplyRule_LowerClass(sub)
            entity = entity.rsplit('#')[-1]
            if entity in lower_list:
                upper_class.append(upper)
                
        return upper_class 

def ApplyRule_SiblingClass(entity):
    
    sibling_class = []
    if entity is None:
        return []
    else:
        upper_class = ApplyRule_UpperClass(entity)
        for upper in upper_class:
            upper = BRICK[upper]
            lower_list = ApplyRule_LowerClass(upper)
            sibling_class.extend(lower_list)
    sibling_class = list(set(sibling_class))
    entity = entity.rsplit('#')[-1]
    sibling_class.remove(entity)
    
    return sibling_class

