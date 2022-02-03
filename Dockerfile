FROM ubuntu:latest

ADD credentials.enc     /my_server/credentials.enc 
ADD credentials_valid.py    /my_server/credentials_valid.py
ADD load_data_into_neo4j_database.py    /my_server/load_data_into_neo4j_database.py
ADD main.py             /my_server/main.py
ADD requetes_bdd.py     /my_server/requetes_bdd.py
ADD requirements.txt    /my_server/requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip3 install fastapi neo4j requests uvicorn

WORKDIR /my_server/

EXPOSE 8000

CMD sleep 15; python3 load_data_into_neo4j_database.py; python3 main.py
