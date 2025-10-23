graph = {
    'A': ['C', 'D', 'F'],
    'B': ['C', 'D'],
    'C': ['A', 'B', 'F'],
    'D': ['A', 'B', 'F'],
    'E': ['F'],
    'F': ['A', 'C', 'D', 'E'],
}


def DegresSommet(graphe, sommet):
    if sommet not in graphe:
        return 0
    return len(graphe[sommet])

def VoisinsSommet(graphe, sommet):
    if sommet not in graphe:
        return []
    return graphe[sommet]

def ParcoursLargeur(graphe, sommet):
    visites = []
    file = [sommet]

    while file:
        actuel = file.pop(0)
        if actuel not in visites:
            visites.append(actuel)
            file.extend([voisin for voisin in graphe.get(actuel, []) if voisin not in visites])
    
    return visites

def ParcoursProfondeur(graphe, sommet):
    visites = []
    pile = [sommet]

    while pile:
        actuel = pile.pop()
        if actuel not in visites:
            visites.append(actuel)
            pile.extend([voisin for voisin in graphe.get(actuel, []) if voisin not in visites])
    
    return visites

print(DegresSommet(graph, 'A'))  # Retourne 3
print(VoisinsSommet(graph, 'A'))  # Retourne ['C', 'D', 'F']
print(ParcoursLargeur(graph, 'A'))  # Retourne un ordre de visite en largeur à partir de 'A'
print(ParcoursProfondeur(graph, 'A'))  # Retourne un ordre de visite en profondeur à partir de 'A'