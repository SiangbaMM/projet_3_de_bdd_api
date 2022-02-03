from neo4j import GraphDatabase

#driver = GraphDatabase.driver('bolt://0.0.0.0:7687', auth=('neo4j', 'neo4j'))
driver = GraphDatabase.driver('bolt://neo4j_prjt3:7687', auth=('neo4j', 'neo4j'))

# deleting data
print('Deleting previous data')

query = '''
MATCH (n) 
DETACH DELETE n
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')

# inserting data
print('Inserting Techno')

query = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/SiangbaMM/projet_3_de_bdd_api/main/stack_network_nodes.csv' AS row
MERGE (:Techno {name: row.name, group:row.group, nodesize:toFloat(row.nodesize)});
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')

print('Inserting group')

query = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/SiangbaMM/projet_3_de_bdd_api/main/stack_network_nodes.csv' AS row
MERGE (:Group {name: row.group});
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')

print('Creating relationships')

queries = [
    '''// Loading acting and changing the labels
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/SiangbaMM/projet_3_de_bdd_api/main/stack_network_nodes.csv' AS row
    MATCH (t:Techno) WHERE t.name = row.name
    MATCH (g:Group) WHERE g.name = row.group
    MERGE (t)-[:FROM]->(g)
    ;''',

    '''
    // Loading appearances
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/SiangbaMM/projet_3_de_bdd_api/main/stack_network_links.csv' AS row
    MATCH (t1:Techno) WHERE t1.name = row.source
    MATCH (t2:Techno) WHERE t2.name = row.target
    CREATE (t1)-[r:LINK_TO]->(t2)
    WITH r, row
    SET r.value=toFloat(row.value);
    '''
]

with driver.session() as session:
    for q in queries:
        print(q)
        session.run(q)

print('done')
