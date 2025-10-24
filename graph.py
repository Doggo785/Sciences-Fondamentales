# Construction d'un graphe d'intervalles à partir des CSV du dossier task_interval
import os
import csv
import random

def construire_graphe_intervalles_csv(fichier_csv):
	"""
	Construit un graphe d'intervalles à partir d'un seul fichier CSV.
	Chaque sommet est le nom de la tâche (première colonne).
	Une arête existe si deux intervalles se chevauchent.
	Retourne un dictionnaire (liste d'adjacence).
	"""
	intervalles = []
	with open(fichier_csv, newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		next(reader, None)  # saute l'en-tête
		for row in reader:
			if len(row) >= 3:
				try:
					tache = row[0]
					debut = float(row[1])
					fin = float(row[2])
					intervalles.append((debut, fin, tache))
				except ValueError:
					continue  # Ignore les lignes invalides

	intervalles.sort(key=lambda x: x[0])
	graphe = {interval[2]: [] for interval in intervalles}
	n = len(intervalles)
	for i in range(n):
		a_debut, a_fin, a_id = intervalles[i]
		for j in range(i+1, n):
			b_debut, b_fin, b_id = intervalles[j]
			if b_debut > a_fin:
				break
			if a_fin >= b_debut and b_fin >= a_debut:
				graphe[a_id].append(b_id)
				graphe[b_id].append(a_id)
	return graphe


def ordre_elimination_parfait_mcs(graphe):
	"""
	Calcule un Ordre d'Élimination Parfait (PEO) avec l'algorithme MCS simplifié.
	graphe : dictionnaire {noeud: [voisins]}
	Retourne une liste de noeuds dans l'ordre PEO.
	"""
	non_visites = set(graphe.keys())
	visites = set()
	peo = []
	# Choisir un noeud de départ au hasard
	if not non_visites:
		return peo
	courant = random.choice(list(non_visites))
	peo.append(courant)
	visites.add(courant)
	non_visites.remove(courant)
	while non_visites:
		# Pour chaque noeud non visité, compter le nombre de voisins déjà visités
		max_connex = -1
		prochain = None
		for noeud in non_visites:
			connex = sum(1 for v in graphe[noeud] if v in visites)
			if connex > max_connex:
				max_connex = connex
				prochain = noeud
		if prochain is None:
			# Si aucun n'est connecté, en prendre un au hasard
			prochain = random.choice(list(non_visites))
		peo.append(prochain)
		visites.add(prochain)
		non_visites.remove(prochain)
	return peo


def colorer_graphe_peo(graphe, peo):
	"""
	Colorie le graphe de manière gloutonne selon l'ordre PEO pour obtenir le nombre minimum de serveurs (χ(G)).
	graphe : dictionnaire {noeud: [voisins]}
	peo : liste des noeuds dans l'ordre PEO
	Retourne un tuple (couleurs_taches, nb_serveurs)
	"""
	couleurs_taches = {}
	for tache in peo:
		# Rassembler les couleurs utilisées par les voisins déjà colorés
		couleurs_utilisees = set()
		for voisin in graphe[tache]:
			if voisin in couleurs_taches:
				couleurs_utilisees.add(couleurs_taches[voisin])
		# Assigner la plus petite couleur disponible
		couleur = 1
		while couleur in couleurs_utilisees:
			couleur += 1
		couleurs_taches[tache] = couleur
	# Le nombre de serveurs est la couleur maximale utilisée
	nb_serveurs = max(couleurs_taches.values()) if couleurs_taches else 0
	return couleurs_taches, nb_serveurs


fichier = 'dataset/task_interval/task_intervals_1.csv'
graphe = construire_graphe_intervalles_csv(fichier)
print(graphe)

peo = ordre_elimination_parfait_mcs(graphe)
print("Ordre d'élimination parfait (PEO) :", peo)

couleurs_taches, nb_serveurs = colorer_graphe_peo(graphe, peo)
print("Assignation des serveurs :", couleurs_taches)
print("Nombre minimum de serveurs nécessaires :", nb_serveurs)
