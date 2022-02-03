import base64

def user_valid(username, password):
    """
       La fonction permet de valider la connexion d'un utilisateur grace au 
       fichier credentials.csv

       @params :
           username : nom de l'utilisateur
           password : mot de passe de l'utilisateur 

       @returns :
           True si ok 
           False sinon
    """

    with open("credentials.enc", 'r') as cred:
        lignes = cred.readlines()
        for ligne in lignes:
            base64_string = str(ligne)
            base64_bytes = base64_string.encode("utf-8")

            line_string_bytes = base64.b64decode(base64_bytes)
            line_string = line_string_bytes.decode("utf-8")

            if line_string.startswith(username) and (line_string.split(",")[1].rstrip()) == str(password) :
                return True
        return False

