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
        if triple!= []:
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

def parse_entity(t):
    if isinstance(t, URIRef):
        ns_entity = t.rsplit('/',1)[1].split('#')
        ns = ns_entity[0].lower()
        entity = ns_entity[1]
        
        return ns+':'+entity
    else:
        return t
    
def get_entity_with_namespace(x):
    if x[0] != '?':
        ns = get_namespace(x)
        if ':' in x:
            entity = x.split(':')[1]
        elif '#' in x:
            entity = x.split('#')[1]
        else:
            entity = None
        if entity is not None and ns is not None:
            return ns[entity]
    return None

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
    # ignore isintsance(x, BRICK['EntityProperty'])
    relationship_triples = brick_graph.triples((None, RDF['type'], OWL['ObjectProperty']))
    ignore_relationships = [
                                BRICK['hasAssociatedTag'], BRICK['feedsAir'], BRICK['controls'], 
                                BRICK['hasTimeseriesId'], BRICK['isTagOf'], BRICK['storedAt'], 
                                BRICK['hasUnit'], BRICK['value'], BRICK['hasOutputSubstance'], 
                                BRICK['hasInputSubstance'], BRICK['measures'], BRICK['isMeasuredBy'],
                                BRICK['hasAddress'], BRICK['regulates'], BRICK['isRegulatedBy'],
                                BRICK['timeseries'], BRICK['hasTag'], BRICK['isAssociatedWith'],
                                BRICK['isControlledBy'], URIRef("http://www.w3.org/2006/vcard/ns#hasAddress")
                            ]
    for r in relationship_triples:
        relationship = r[0]
        inv_relationship = get_inverse_relationship(relationship)
        if relationship not in relationships and relationship not in ignore_relationships:
            relationships.append(relationship)
    return relationships

def get_relationship_domain_range_map():
    relationships = get_all_brick_relationships()
    
    relationship_domain_range_map = {}
    for relationship in relationships:
        relationship_domain_range_map[relationship] = {}

        range_triples = brick_graph.triples((relationship, RDFS['range'], None))
        for r in range_triples:
            if relationship_domain_range_map.get(relationship).get('range') is None:
                relationship_domain_range_map[relationship]['range'] = r[2]

        domain_triples = brick_graph.triples((relationship, RDFS['domain'], None))
        for d in domain_triples:
            if relationship_domain_range_map.get(relationship).get('domain') is None:
                relationship_domain_range_map[relationship]['domain']= d[2]

    return relationship_domain_range_map

def get_shacl_relationship_map():
    g = brickschema.Graph()
    g.parse("https://raw.githubusercontent.com/BrickSchema/Brick/master/shacl/BrickEntityShapeBase.ttl", format="ttl")

    q = """SELECT ?cls ?path ?allowed WHERE {
        ?sh a sh:NodeShape .
        ?sh sh:targetClass ?cls .
        ?sh sh:property ?prop .
        ?prop sh:path ?path .
        {
            ?prop sh:class ?allowed
        }
        UNION
        {
            ?prop sh:or/rdf:rest*/rdf:first/sh:class ?allowed
        }
    }"""

    shacl_results = g.query(q)
    
    shacl_relationship_map = {}
    for row in shacl_results:
        sub = row[0]
        rel = row[1]
        obj = row[2]

        if shacl_relationship_map.get(rel) is None:
            shacl_relationship_map[rel] = []

        shacl_relationship_map[rel].append({'subject': sub, 'object':obj})
    return shacl_relationship_map

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
    
def get_type_from_triples(entity, triples):
    if entity is None or triples is None:
        return None
    if len(triples) == 0:
        return None
    
    for triple in triples:
        t0 = triple[0]
        t1 = triple[1]
        if t0 == entity and (t1 == 'a' or t1 == 'rdf:type'):
            return get_entity_with_namespace(triple[2])
    return None

def run_brick_query(building_model, query):
    try:
        res = building_model.query(query)

        op = []
        for row in res:
            op.append(row[0])

        return op
    except:
        return []
    
def generate_brick_query_from_node(triples, select_statement=None):
    q = """"""
    if select_statement is not None:
        if select_statement[-1] != "\n":
            select_statement+="\n"
        q+=select_statement
    else:
        q="""SELECT ?vav WHERE {\n"""
    for triple in triples:
        t0 = parse_entity(triple[0])
        t1 = parse_entity(triple[1])
        t2 = parse_entity(triple[2])

        q+=" ".join([t0, t1, t2]) + " . \n"
    q+="}"
    return q