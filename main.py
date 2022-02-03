from fastapi import FastAPI, Header, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import requests
import requetes_bdd as rbdd
import uvicorn

api = FastAPI(
        title='API : Projet DE #3 - Base de données',
        description="""L’objectif de ce projet est de choisir, mettre en place, et peupler une base de données à
                       partir d’un jeu de données de l’open data, et d’implémenter une API vous permettant de
                       requêter cette base de données""",
        version="1.0.0",
        openapi_tags=[
            { 
                'name': 'Techno',
                'description': 'Requetes sur technos'
               },
            {  
                'name': 'Groupe',
                'description': 'Requetes sur les groupes de technos'
               },
            {
                'name': 'Admin',
                'description': 'Administration des technos et groupes'
               }
        ]
)



@api.get('/status', tags=["Status de l'API"], name="Status de l'API")
async def get_status():
    """
    Verification du status de l'API
    """
    return "L'API fonctionne"


@api.get("/info/{item}", tags=['Techno', 'Groupe'], name="Info sur la techno")
async def get_inf(item:str):
    """
    Retourne les informations de la techno (nom, groupe, nodesize)
    """
    return rbdd.affiche_info(item)
    
    
@api.get("/techno/liste_technos", tags=['Techno'], name="Listes des technos" )
async def get_tech():
    """
    Affiche les technos de la base de données
    """
    return rbdd.affiche_techno()


@api.get("/groupe/liste_group_techno", tags=['Groupe'], name="Listes des technos par groupe")
async def get_group_techno():
    """
    Affiche la liste des technos par groupe
    """
    return rbdd.affiche_group_techno()


@api.get("/groupe/liste_group_count_element", tags=['Groupe'], name="Nombre de technos par groupe")
async def get_group_count_element():
    """
    Affiche le nombre de technos par groupe
    """
    return rbdd.affiche_group_count_element()


@api.get("/groupe/{item}", tags=['Groupe'], name="Info sur le groupe")
async def get_group_item(item:str):
    """
    Affiche les informations du groupe
    """
    return rbdd.affiche_group_item(item)

@api.get("/techno/liaisons/{item}", tags=['Techno'], name="Liaison associée à la techno")
async def get_link(item:str):
    """
    Affiche la liste des technos assosié à la techno renseignée
    """
    return rbdd.affiche_liaisons_techno(item)


class AddTechno(BaseModel):
    """
    Paramètres nécessaires à l'ajout d'une techno
    """
    name: str
    group: str
    nodesize: str 
    target: str
    value: str
    authorization: str

class DelTechno(BaseModel):
    """
    Paramètres nécessaires à la suppression d'une techno
    """
    name: str
    group: str
    authorization: str

@api.put("/techno/ajout", tags=['Admin'], name="Ajout techno a la BDD")
async def add_techno(techno: AddTechno):
    """
    Ajout d'une nouvelle techno a la BDD
    """
    try :
        if rbdd.permissions(techno.authorization):
            return rbdd.ajout_techno_bdd(techno)

    except IndexError:
        raise HTTPException(
            status_code=404,
            detail="'authorization': 'name=password'"
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Access denied'
        )


@api.put("/techno/suppression", tags=['Admin'], name="Suppression techno de la BDD")
async def add_techno(techno: DelTechno):
    """
    Suppression d'une techno de la BDD
    """
    if rbdd.permissions(techno.authorization):
        return rbdd.suppression_techno_bdd(techno)
    return rbdd.permissions(techno.authorization)


if __name__ == '__main__':
    uvicorn.run(api, host="0.0.0.0", port=8000)
