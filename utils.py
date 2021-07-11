import brickschema
from brickschema.namespaces import BRICK, RDFS, OWL, TAG, RDF
from rdflib import URIRef

brick_graph = brickschema.Graph(load_brick=True)

def extract_triples(query): 
    triples = []
    where_clause = query.split('{')[1].split('}')[0]
    for where_line in where_clause.split('.'):
        line = where_line.strip()
        triple = []
        count = 0
        for i in line.split(' '):
            i = i.strip()
            
            if i!= "" and i!= " " and i!= "\n":
                if count == 0:
                    triple.append(i)
                elif count == 1:
                    triple.append(i)
                elif count == 2:
                    triple.append(i)
                count+=1
        triples.append(triple)
    return triples

def get_namespace(x):
    if ':' in x:
        ns = x.split(':')[0]
    else:
        ns = 'brick'
    if ns.lower() == 'brick':
        return BRICK
    elif ns.lower() == 'owl':
        return OWL
    elif ns.lower() == 'tag':
        return TAG
    elif ns.lower() == 'rdf':
        return RDF
    elif ns.lower() == 'rdfs':
        return RDFS
    elif ns.lower() == 'sh':
        return SH

def get_inverse_relationship(relationship):
    inverse_relns = list(brick_graph.triples((relationship, OWL['inverseOf'], None)))
    if len(inverse_relns) == 1:
        return inverse_relns[0][2]
    elif len(inverse_relns) == 0:
        return None
    else:
        inv_relns = []
        for reln in inverse_relns:
            inv_relns.append(reln[0][2])
        return inv_relns

def get_all_brick_relationships():
    relationships = []
    relationship_triples = brick_graph.triples((None, RDF['type'], OWL['ObjectProperty']))
    for r in relationship_triples:
        relationship = r[0]
        inv_relationship = get_inverse_relationship(relationship)
        if relationship not in relationships:# and inv_relationship not in relationships:
            relationships.append(relationship)
    return relationships

def get_relationship_domain_range_map():
    relationships = get_all_brick_relationships()
    
    relationship_domain_range_map = {}
    for relationship in relationships:
        relationship_domain_range_map[relationship] = {}

        range_triples = brick_graph.triples((relationship, RDFS['range'], None))
        for r in range_triples:
            if relationship_domain_range_map.get('relationship') is None:
                relationship_domain_range_map[relationship]['range'] = r[2]

        domain_triples = brick_graph.triples((relationship, RDFS['domain'], None))
        for d in domain_triples:
            if relationship_domain_range_map.get('relationship') is None:
                relationship_domain_range_map[relationship]['domain']= d[2]

    return relationship_domain_range_map

def get_all_equipment(t=None):
    if t is None:
        t = 'all'
    
    if t == 'all':
        return list(brick_graph.transitive_subjects(object=BRICK['Equipment'], predicate=RDFS['subClassOf']))
    elif t == 'hvac':
        return list(brick_graph.transitive_subjects(object=BRICK['HVAC_Equipment'], predicate=RDFS['subClassOf']))
    
def get_hvac_equipment():
    return get_all_equipment(t='hvac')

def get_super_classes(entity):
    if entity is None:
        return []
    else:
        super_classes = []
        for sup in brick_graph.transitive_objects(subject=entity, property=RDFS['subClassOf']):
            if isinstance(sup, URIRef):
                super_classes.append(sup)
        return super_classes