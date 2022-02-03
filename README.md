## DataScientest : Projet 3 Data Engineer - Base de données & API de donnée

### <u>Introduction</u>
L’objectif de ce projet est de choisir, mettre en place, et peupler une base de données à partir d’un jeu de données de l’open data,
et d’implémenter une API permettant de requêter cette base de données.

### <u>Contexte des données</u>
Nous avons choisit pour ce projet [le jeu de données de **Stack Overflow**](https://www.kaggle.com/stackoverflow/stack-overflow-tag-network?select=stack_network_links.csv) sur les écosystèmes technologiques et à la façon dont les technologies sont liées les unes aux autres.    
Ce jeu de données comprends deux fichiers :
> * stacknetworklinks : qui contient les liens du réseau, les balises techniques source et cible ainsi que la valeur du lien entre chaque paire    
> * stacknetworknodes : qui contient les nœuds du réseau, le nom de chaque nœud, le groupe auquel ce nœud appartient (calculé via un cluster walktrap)

Afin de modéliser ces données, nous avons choisit la base de données [Neo4J](https://neo4j.com/cloud/neo4j-aura/?utm_program=emea-prospecting&utm_source=google&utm_medium=cpc&utm_campaign=emea-search-auradb-free&utm_adgroup=auradb-free-keywords&utm_content=auradb-free-keywords&gclid=CjwKCAiAl-6PBhBCEiwAc2GOVKUYUkd3vrIQyiT7ud3GHskOtEz2gtipje06ivNKXeF4u7d324KOtBoCZEAQAvD_BwE) avec deux types de nœud :    
> * **Techno** : les différentes technologies   
> * **Groupe** : les différents groupes de technologies

Et comme type de liens : 
> * **LINK** : le lien entre chaque techno
> * **FROM** : le lien entre une techno et son groupe associé

### <u>API</u>
L'API possède les routes suivantes :   
> * /status : Verification du status de l'API
> * /info/{item} : Retourne les informations de la techno (nom, groupe, nodesize) renseigné   
> * /techno/liste_technos : Affiche les technos de la base de données   
> * /groupe/liste_group_techno : Affiche le nombre de technos par groupe    
> * /groupe/{item} : Affiche les informations du groupe   
> * /techno/liaisons/{item} : Affiche la liste des technos assosié à la techno renseignée   
> * /techno/ajout : Ajout d'une nouvelle techno a la BDD   
> * /techno/suppression : Suppression d'une techno de la BDD   

PS : L'ajout et la suppression de techno se fait sans vérification au préalable.

### <u>Livrable</u>
> * **stacknetworklinks.csv** et **stacknetworknodes.csv** : les fichiers de données     
> * **requirements.txt** : contenant les packages nécessaires à l'execution des scripts python   
> * **load_data_into_neo4j_database.py** : le script python de peuplement de la base de données à partir du jeu de données     
> * **requetes_bdd.py** : le script python de requêtage de la base de données    
> * **credentials.enc** : le fichier des mots de passe encoder en base 64
> * **credentials_valid.py** : le script de décodage des mots de passe
> * **main.py** : le script de lancement de l'API réalisé avec FastAPI     
> * **Dockerfile** : le fichier de création de l'image docker de l'API    
> * **docker-compose.yml** : pour le lancement des containers de neo4j et l'API

### <u>Lancement du projet</u>
Pour lancer ce projet il faut :   
> * Avoir installer docker
> * Télécharger le fichier docker-compose.yml :   
>```bash 
>wget https://raw.githubusercontent.com/SiangbaMM/projet_3_de_bdd_api/main/docker-compose.yml -O docker-compose.yml
>```      
> * Ensuite, exécuter la commande :   
>```bash
>docker-compose up
>```  

L'API et la base de données seront disponible respectivement sur le port 8000 et 7474 de votre machine.
 
