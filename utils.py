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