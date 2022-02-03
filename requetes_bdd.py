from neo4j import GraphDatabase
from credentials_valid import user_valid 
from fastapi import HTTPException


driver = GraphDatabase.driver('bolt://neo4j_prjt3:7687',
                              auth=('neo4j', 'neo4j'))


def affiche_info(x):
    query = '''
    MATCH (t:Techno) 
    WHERE t.name="{tech}"
    RETURN t.name as name, t.group AS group, t.nodesize AS nodesize
    '''.format(tech=x)

    with driver.session() as session:
       result = session.run(query).data()

    if len(result) < 1:
        raise HTTPException(status_code = 404, detail = "Not found")

    return result


def affiche_techno():
   query = '''
   MATCH (t:Techno) 
   RETURN DISTINCT(t.name) as techno, t.group AS groupe, t.nodesize AS nbr_tags
   '''

   with driver.session() as session:
      result = session.run(query).data()
      
   return result


def affiche_group_techno():
   query = '''
   MATCH (g:Group) <-[:FROM]- (t:Techno)
   RETURN g.name AS groupe, COLLECT(t.name) AS liste_technos
   ORDER BY toInteger(g.name)
   '''

   with driver.session() as session:
      result = session.run(query).data()

   return result


def affiche_group_count_element():
    query = '''
    MATCH (g:Group) <-[:FROM]- (t:Techno)
    RETURN g.name AS groupe, COUNT(DISTINCT t.name) AS nbr_techno
    ORDER BY toInteger(g.name)
    '''

    with driver.session() as session:
       result = session.run(query).data()

    return result


def affiche_group_item(id_item):
    try:
        id_group = int(id_item)
        if id_group in range(1,15):
            query = '''
            MATCH (g:Group) <-[:FROM]- (t:Techno)
            WHERE g.name = $name
            RETURN g.name AS groupe, COLLECT(t.name) AS liste_technos, COUNT(t.name) AS nbr_technos
            '''

            with driver.session() as session:
                result = session.run(query, name=id_item).data()

            return result
        
        else :
            return "Valeur en dehors de l'intervale [1,14]"

    except ValueError:
        return "La valeur du groupe doit etre un nombre entier"



def affiche_liaisons_techno(x):
    query = '''
    MATCH (t:Techno) WHERE t.name = $name
    RETURN t
    '''

    with driver.session() as session:
       result = session.run(query, name=x).data()

    if len(result) < 1:
        return "La techno est absent de la base"

    query = '''
    MATCH (t1:Techno) -[:LINK_TO]-> (t2:Techno) WHERE t1.name = $name
    RETURN t1.name AS nom_techno_source, t1.group AS groupe_techno_source, COLLECT(t2.name) AS nom_techno_target, COUNT(t2.name) AS nbr_techno_target
    '''

    with driver.session() as session:
       result = session.run(query, name=x).data()

    if len(result) < 1:
        raise HTTPException(status_code = 404, detail = "Not found")

    return result


def permissions(techno):
    if techno != None :
        print('techno :',techno)
        username = techno.split("=")[0]
        password = techno.split("=")[1]
        if user_valid(username,password) :
            return True
        else :
            raise HTTPException(status_code = 404, detail = "Access denied")
    else :
        raise HTTPException(status_code = 400, detail = "Bad request")


def ajout_techno_bdd(techno):
    print('techno :',techno)
    query = '''
    MERGE (:Techno {name: $name, group: $group, nodesize:toFloat($nodesize)});
    '''

    l = []

    with driver.session() as session:
       result = session.run(query, name=techno.name, group=techno.group, nodesize=techno.nodesize).data()
       

    query = '''
    MATCH (t:Techno), (g:Group) WHERE t.name=$name AND g.name=$group
    MERGE (t) -[:FROM]-> (g);
    '''

    with driver.session() as session:
       result = session.run(query, name=techno.name, group=techno.group).data()
       

    query = '''
    MATCH (t1:Techno) WHERE t1.name = $name
    MATCH (t2:Techno) WHERE t2.name = $target
    MERGE (t1)-[r:LINK_TO]->(t2)
    WITH r
    SET r.value=toFloat($value);
    '''

    print("techno.target.split(',') :", techno.target.split(','))

    with driver.session() as session:
       result = session.run(query, name=techno.name, target=techno.target, value=techno.value).data()
       l.append(result)

    return "Done"


def suppression_techno_bdd(techno):
    query = '''
    MATCH (t:Techno) WHERE t.name = $name
    DETACH DELETE t 
    '''

    with driver.session() as session:
       result = session.run(query, name=techno.name).data()

    return "Done"
