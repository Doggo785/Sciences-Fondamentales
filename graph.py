"""
 Matrice d’adjacence (graphe non orienté)
     (0 0 1 1 1 0 0)
     (0 0 1 1 0 0 0)
     (1 1 0 0 0 1 0)
 M = (1 1 0 0 1 0 0)
     (0 0 0 0 0 1 0)
     (1 0 1 1 1 0 0)
     (0 0 0 0 0 0 0)
"""


graph = {
    'A': ['C', 'D', 'E'],
    'B': ['C', 'D'],
    'C': ['A', 'B', 'F'],
    'D': ['A', 'B', 'E'],
    'E': ['A', 'F'],
    'F': ['A', 'C', 'D', 'E'],
    'G': []
}


def DegresSommet(graphe, sommet):
    if sommet not in graphe:
        return 0
    return len(graphe[sommet])

def VoisinsSommet(graphe, sommet):
    if sommet not in graphe:
        return []
    return graphe[sommet]

print(DegresSommet(graph, 'A'))  # Retourne 3
print(VoisinsSommet(graph, 'A'))  # Retourne ['C', 'D', 'E']