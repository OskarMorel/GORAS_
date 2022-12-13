# +----------------------------------------------------------------------------------------------------------------+
# | Author : Morel Oskar                                                                                           |
# |          Gouzy Antoine                                                                                         |
# |          Jauzion Rémi                                                                                          |
# |          Gautier Jalbaud                                                                                       |
# |          Lanay Simon                                                                                           |
# +----------------------------------------------------------------------------------------------------------------+
# | DSI/ serveur:                                                                                                  |
# | - Répond aux questions du client (cyberExpert)                                                                 |
# | - Utilisation des sockets en TCP.                                                                              |
# | - Coupage du code en plusieurs fonctions.                                                                      |
# | - Gestion des erreurs avec des try / except                                                                    |
# | - Le serveur (ce programme) montre son IP sur la console pour que le client puisse l'entrer dans son programme |
# +----------------------------------------------------------------------------------------------------------------+

import socket
import json
import os           

# TODO ***********************
# Noms plus explicite 
# constante pour le programme principal "question 1" "question 2"
# Fonctions moins longues

print("╔═══╗╔╗                       ╔╗ ")
print("║╔═╗║║║                      ╔╝║ ")
print("║╚═╝║║║ ╔══╗ ╔╗ ╔╗╔══╗╔═╗    ╚╗║ ")
print("║╔══╝║║ ╚ ╗║ ║║ ║║║╔╗║║╔╝     ║║ ")
print("║║   ║╚╗║╚╝╚╗║╚═╝║║║═╣║║     ╔╝╚╗")
print("╚╝   ╚═╝╚═══╝╚═╗╔╝╚══╝╚╝     ╚══╝")
print("             ╔═╝║")
print("             ╚══╝  ")

# Utilisés dans les échanges avec le client
QUESTION_1 = "question1"
QUESTION_2 = "question2"
QUESTION = "question"
CLE_NEXT = "cleNext"
REPONSE_1 = "reponse1"
REPONSE_2 = "reponse2"
REPONSE = "reponse"

# Récupération du chemin courant pour accéder au fichier des questions / réponses
path = os.getcwd()

# Ouverture du fichier JSON qui contient les questions / réponses
with open(path + '\QA.json') as QA:
    data = json.load(QA)
ipServeur = socket.gethostbyname(socket.gethostname())
print("Server'socketServeur IP : " + ipServeur)

# Création de la socket du serveur
def creationSocket():
    try:
        socketServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError:
        print('Socket creation failed')
    else:
        print('Socket creation success')
        coordServeur = (ipServeur, 65432)
        # Association des coordonnées à la socket créée 
        try:
            socketServeur.bind(coordServeur)
            socketServeur.listen(1)
        except OSError:
            print('bind() fail')
            socketServeur.close()
        else:
            print('bind() success')
    return socketServeur

# Acceptation de la connexion avec le client (l'expert en cybersécurité)
def accepter(socketServeur):
    (communication, coordonneesClient) = socketServeur.accept()
    print("connection established\n")
    return(communication)
    

def programmePrincipal(socketServeur, communication):
    ok = True
    premier = False
    choixAFaire = True
    # Explication du contexte
    print("You are a CIO, your company has been hacked. That'socketServeur why you called a cybersecurity expert.\nYou will have to answer his questions so that he can help you.\nGood luck.\n")
    while ok :
        question2 = True
        receptionClient = communication.recv(1024).decode()

        if receptionClient != "0":
            if premier:
                if data[cleAEnvoyer][QUESTION_1][CLE_NEXT] == receptionClient:
                    print(data[cleAEnvoyer][QUESTION_1][QUESTION]+ "\n")
                else:
                    print(data[cleAEnvoyer][QUESTION_2][QUESTION] + "\n")
            else:
                print(data["1"][QUESTION])

            # Choix de la réponse à envoyer au client (l'expert en cybersécurité)
            print("1) " + data[receptionClient][REPONSE_1][REPONSE])
            try:
                print("2) " + data[receptionClient][REPONSE_2][REPONSE] + "\n")
            except:
                print("")
                question2 = False

            choix = input("Choose between 1 and 2 : ")
            if choix == "1":
                cleAEnvoyer = data[receptionClient][REPONSE_1][CLE_NEXT]
            elif choix == "2" and question2 == True:
                cleAEnvoyer = data[receptionClient][REPONSE_2][CLE_NEXT]
            else:
                while(choix != "1" and choix !="2" or question2 == False):
                        choix = input("Choose between 1 and 2 : ")       
                        if choix == "1":
                            cleAEnvoyer = data[receptionClient][REPONSE_1][CLE_NEXT]
                            question2 = True
                        elif choix == "2" and question2 == True:
                            cleAEnvoyer = data[receptionClient][REPONSE_2][CLE_NEXT]

            premier = True
            # Arret de la boucle si arriver a la fin de l'arbre
            if cleAEnvoyer == "0":
                print("\nThis is the end of the game\n")
                ok = False
            communication.send(cleAEnvoyer.encode())

        else:
            print("\nThis is the end of the game\n")
            ok = False

# Fermeture de la socket
def fermetureSocket(socketServeur, communication):
    try:
        communication.close()
        socketServeur.close()
    except OSError:
        print('Socket is open !')
    else:
        print('Socket closed')

socketServeur = creationSocket()
communication = accepter(socketServeur)
programmePrincipal(socketServeur, communication)
fermetureSocket(socketServeur, communication)