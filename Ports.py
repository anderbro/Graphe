### import librairies
import pandas as pd #représenter tableaux données sous forme de dataframe
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as ps


### import données
Ports = pd.read_csv('Ports_csv.csv',sep=",")
#création objet graphe orienté
G = nx.DiGraph()

G = nx.from_pandas_edgelist(Ports,source='Port_départ',target='Port_arrivée',edge_attr='Trajet(h)', create_using=G)


pos = nx.spring_layout(G) #placement des sommets
edge_labels_list=nx.get_edge_attributes(G,'Trajet(h)') # dico poids des arêtes

nx.draw_networkx(G,pos,with_labels=True)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels_list)
plt.show()


#ligne de la matrice d'adjacence qui correspond au Havre
print(nx.attr_matrix(G)[0][nx.attr_matrix(G)[1].index("Le Havre")])
print("###########################################################")
print(nx.attr_matrix(G)[0][nx.attr_matrix(G)[1].index("Le Havre"),nx.attr_matrix(G)[1].index("Dunkerque")])
print("###########################################################")
print(nx.attr_matrix(G)[0][nx.attr_matrix(G)[1].index("Marseille"),nx.attr_matrix(G)[1].index("Le Havre")])
print("###########################################################")
print(nx.attr_matrix(G,edge_attr='Trajet(h)')[0][nx.attr_matrix(G,edge_attr='Trajet(h)')[1].index("Toulon"),nx.attr_matrix(G,edge_attr='Trajet(h)')[1].index("Marseille")])
print("###########################################################")

def TrajetExiste(va,vb):
    if(nx.attr_matrix(G)[0][nx.attr_matrix(G)[1].index(va),nx.attr_matrix(G)[1].index(vb)]==1.0):
        tmps=nx.attr_matrix(G,edge_attr='Trajet(h)')[0][nx.attr_matrix(G,edge_attr='Trajet(h)')[1].index(va),nx.attr_matrix(G,edge_attr='Trajet(h)')[1].index(vb)]
        print( "La liasion " , va , vb , "existe, la durée de la traversée est de :" , tmps)
    else:
        print("La liasion ",va , vb," n'existe pas")

        
#test d'existance d'une ligne maritime
        
print("Recherchez votre traversée :")
va=input("entrez la ville de départ ")
vb=input("entrez la ville d'arrivée ")
TrajetExiste(va,vb)

    
print("###########################################################")
# nombre de possibilités d'arrivées; liste décroissante


d=dict()
for i in range(G.order()):
    d[nx.attr_matrix(G)[1][i]]=np.sum(nx.attr_matrix(G)[0],axis=1)[i,0]
    
dict_trie = sorted(d.items(), key=lambda x: x[1],reverse=True)
print("nb d'arrivées possible dans ce port: ", dict_trie)

print("###########################################################")

# nombre de ports atteignable depuis chaque port ; liste décroissante
d=dict()
for i in range(G.order()):
    d[nx.attr_matrix(G)[1][i]]=np.sum(nx.attr_matrix(G)[0],axis=0)[0,i]
dict_trie = sorted(d.items(), key=lambda x: x[1],reverse=True)
print("nb de départs: ", dict_trie)
### Centralité 
#évident : degré
print("###########################################################")



#Betweenness (utilise le # de + courts chemins entre 2 sommets passant par un sommet)
print("betweenness: ", nx.betweenness_centrality(G)) 
print("###########################################################")



#Closeness (utilise la distance moyenne entre un sommet et les autres)
print("closeness: ", nx.closeness_centrality(G)) 
print("###########################################################")




# valeur des gains (départs  - arrivées) ville ; liste décroissante
d=dict()
for i in range(G.order()):
    d[nx.attr_matrix(G)[1][i]]=np.sum(nx.attr_matrix(G,edge_attr='Trajet(h)')[0],axis=1)[i,0]-np.sum(nx.attr_matrix(G,edge_attr='Trajet(h)')[0],axis=0)[0,i]
    dict_trie = sorted(d.items(), key=lambda x: x[1],reverse=True)
print("gains: ", dict_trie)
print("###########################################################")



# temps de trajet total des départs depuis ce port ; liste décroissante
d=dict()
for i in range(G.order()):
    d[nx.attr_matrix(G)[1][i]]=np.sum(nx.attr_matrix(G,edge_attr='Trajet(h)')[0],axis=0)[0,i]
dict_trie = sorted(d.items(), key=lambda x: x[1],reverse=True)
print("temps de trajet des départs depuis ces ports: ", dict_trie)

print("###########################################################")




def gains(graph,weigth):
    d=dict()
    for i in range(graph.order()):
        d[nx.attr_matrix(graph)[1][i]]=np.sum(nx.attr_matrix(graph,edge_attr=weigth)[0],axis=1)[i,0]-np.sum(nx.attr_matrix(graph,edge_attr=weigth)[0],axis=0)[0,i]
    dict_trie = sorted(d.items(), key=lambda x: x[1],reverse=True)
    return (dict_trie)
    
print("""autre façon de faire, pour trouver le "gains" """, gains(G,'Trajet(h)'))





print("###########################################################")
sme=0
for i in range(Ports.shape[0]) :
    sme+=Ports.CO2[i]
moy=sme/129
print( "un voyage emet en moyenne ",moy," (C02 en kg/personne)")



def co2():

    x = []
    y = 0
    for i in range(Ports.shape[0]) :
        if (Ports.CO2[i] > moy):
            x.append(Ports.CO2[i])
            y+=1
    print("il y a donc ",y, "voyages qui emetent plus que la moyenne")        
    return x 
  
print(co2())







print("###########################################################")
# algorithme Dijkstra (longueurs des + court chemins entre un sommet et les autres)

def dijkstra(graph,source,weight):
    # graph: un graphe G ;
    #source:le sommet dont on veut connaitre les PCC ;
    #weight: nom de la distance nodes = list(graph.nodes)
    nodes = list(graph.nodes)#liste des sommets
    Distances=graph.adj #matrice d'adjacence
   
    unvisited = {node: None for node in nodes}  #Ce sont tous les sommets qui n’ont pas encore été visités
    visited = {} #liste des sommets vistés
    current = source  #sommet actuel = le premier sommet
    currentDistance = 0 #sommet de depart = 0, on commence l'algo
    unvisited[current] = currentDistance  #valeur dico pour clé current attribue distance 0

    # Exécution de la boucle tant que que tous les sommets n'ont pas été visités
    while True:
        for neighbour, distance in Distances[current].items():
            if neighbour not in unvisited:
                continue #si le sommet est visité on passe au prochain if
            
            newDistance = currentDistance + distance[weight] #"stock" la distance actuelle 
            if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                unvisited[neighbour] = newDistance
                # si la distance jusqu'au voisin n'a pas été visité ou est plus petit que la nouvelle distance
                # alors on prend cette derniere
        visited[current] = currentDistance #le sommet voulu est ajouté dans les sommets visité
        del unvisited[current] #il est logiquement supprimé des sommets non visités
        if not unvisited: break #des qu'on a fait le tour des sommets on sort de la boucle
        candidates = [node for node in unvisited.items() if node[1]]  #tout les sommets non-visités
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0] #tri par distance croissante des candidats avec fonction
        #lambda x : x[1] à key x j'associe value = le poids de l'arête pour aller à x 
    return visited #dico des distances entre la ville source et les autres villes


print("Dijktra: ",dijkstra(G,'Marseille','Trajet(h)'))
#algorithme A*: retourne le + court chemin entre 2 sommets ; calculé avec l'algorithme de Dijkstra
print("entrez les villes pour lesquelles vous voulez le plus court chemin, parmis Marseille, Le Havre, Dunkerque, Calais, Nantes, Rouen,")
print("Bordeaux,La Rochelle, Bayonne,Sète, Saint-Jean-de-Luz, Caen, Cherbourg, Lorient, Bastia, Brest, Saint-Malo,Ajaccio,Toulon, Nice, Granville, Vannes, Quimper, Boulogne")
x=input("entrez la ville de départ ")
y=input("entrez la ville d'arrivéex ")
print("Astar: ",nx.astar_path(G,x,y,weight='Trajet(h)'))





