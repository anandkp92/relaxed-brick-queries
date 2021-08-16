import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF, SH
from rdflib import URIRef
from utils import *
from rules.relationship_relaxation import *
from rules.type_relaxation import *
import pandas as pd
import numpy as np

def get_total_num_instances(building_model, t):
    
    q = """SELECT * WHERE {
        ?x a """+t+"""
        }"""
    res = building_model.query(q)
    return len(res)

def sim_triple(t1, t2, g, total_instances):
    s1 = t1[0]
    s2 = t2[0]
    
    p1 = t1[1]
    p2 = t2[1]
    
    o1 = t1[2]
    o2 = t2[2]
    
    
    if s1 == s2 and p1 == p2 and o1 == o2:
        return 1
    
    if (p1 == 'rdf:type' or p1 == 'a') and (p2 == 'rdf:type' or p2 == 'a'):
        o1_num = get_total_num_instances(building_model=g, t=o1)
        o2_num = get_total_num_instances(building_model=g, t=o2)
        if o2_num == 0 or o1_num == 0:
            return 2/3.0
        
        score = 2/3.0 + np.log(o2_num/total_instances)/np.log(o1_num/total_instances)/3.0
        return score
    else:
        if p1 == p2+'+' or p1+'+' == p2 or p1 == p2:
            score = 1
        else:
            score = 0
        return score
    
def sim_score(triples1, triples2, g, total_instances):
    sim_score = 1
    for i in range(len(triples1)):
        sim_score *= sim_triple(triples1[i], triples2[i], g, total_instances)
    return sim_score