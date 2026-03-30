"""
injection_table.py
==================
Table d'injection de base extraite de l'ECU du KTM 690 Duke 2016.

Ce module contient la cartographie d'injection brute telle qu'elle a été
extraite de l'ECU, ainsi qu'une fonction d'interpolation bilinéaire permettant
d'obtenir une durée d'injection précise pour n'importe quelle combinaison
de régime moteur et de position d'accélérateur.

Structure de la table
---------------------
La table est organisée sous la forme d'une grille à deux dimensions :
    - Axe vertical  : régime moteur en tours par minute (30 points de 0 à 9000 tr/min)
    - Axe horizontal : position de l'accélérateur en pourcentage (20 points de 0 à 100%)
    - Valeurs        : durée d'ouverture des injecteurs en microsecondes (µs)

La plage de valeurs acceptées par l'ECU est comprise entre 0 et 15 000 µs,
ce qui correspond à des durées d'injection de 0 à 15 millisecondes.

Méthode d'interpolation
-----------------------
Lorsque le régime moteur ou la position d'accélérateur ne correspondent pas
exactement à un point de la grille, une interpolation bilinéaire est appliquée.
Cette méthode consiste à calculer une valeur à l'intérieur d'un rectangle formé
par les quatre points de grille les plus proches, en pondérant chacun d'eux
proportionnellement à la distance.

Cette approche est préférable à une interpolation linéaire simple car elle
prend en compte les variations dans les deux dimensions simultanément, ce qui
produit une réponse plus lisse et plus représentative du comportement réel
de l'ECU.

Auteur  : Projet Fuel Tracker — KTM 690 Duke 2016
Version : 1.0
"""

import numpy as np


# ── Axes de la table d'injection ────────────────────────────────────────────────

# Points de la grille sur l'axe de la position d'accélérateur (en %)
# 20 points répartis de façon non uniforme, avec une densité plus élevée
# aux faibles ouvertures (zone de fonctionnement la plus fréquente)
AXE_ACCELERATEUR = [
    0.0, 0.9, 1.9, 2.8, 3.8, 5.6, 7.5, 9.4,
    11.9, 15.6, 18.8, 21.9, 25.0, 31.3, 37.5,
    43.8, 50.0, 60.0, 75.0, 100.0
]

# Points de la grille sur l'axe du régime moteur (en tr/min)
# 30 points répartis de façon non uniforme, couvrant la plage complète
# de fonctionnement du moteur, du démarrage jusqu'au régime maximum
AXE_REGIME = [
    0, 800, 1000, 1350, 1550, 1650, 1750, 1900,
    2100, 2300, 2600, 2750, 2900, 3200, 3500, 3750,
    4000, 4250, 4500, 4750, 5000, 5250, 5500, 6000,
    6500, 7000, 7500, 8000, 8500, 9000
]


# ── Valeurs de la table d'injection ─────────────────────────────────────────────
# Chaque ligne correspond à un régime moteur (ordre croissant de haut en bas)
# Chaque colonne correspond à une position d'accélérateur (ordre croissant de gauche à droite)
# Les valeurs sont exprimées en microsecondes (µs)

TABLE_INJECTION = [
    # 0tr/m
    [1209, 1250, 1335, 1364, 1603, 1742, 1894, 2046, 2185, 2325, 2430, 2563, 2828, 3225, 3861, 4675, 5053, 5768, 6583, 8332],
    # 800tr/m
    [1022, 1060, 1115, 1198, 1368, 1497, 1642, 1781, 1927, 2033, 2172, 2397, 2544, 2951, 3558, 4308, 4711, 5468, 6503, 8528],
    # 1000tr/m
    [1038, 1082, 1133, 1258, 1403, 1560, 1693, 1788, 1858, 1957, 2073, 2238, 2443, 2844, 3444, 4242, 4664, 5468, 6534, 8580],
    # 1350tr/m
    [1000, 1020, 1153, 1251, 1435, 1587, 1717, 1785, 1841, 1911, 1990, 2156, 2351, 2707, 3347, 4176, 4718, 5628, 6718, 8699],
    # 1550tr/m
    [1000, 1020, 1153, 1255, 1450, 1607, 1740, 1783, 1818, 1848, 1940, 2117, 2316, 2716, 3332, 4110, 4782, 5713, 6840, 8819],
    # 1650tr/m
    [1000, 1020, 1160, 1262, 1454, 1611, 1756, 1806, 1829, 1852, 1950, 2112, 2324, 2732, 3354, 4033, 4824, 5761, 6894, 8883],
    # 1750tr/m
    [1000, 1020, 1168, 1277, 1439, 1611, 1775, 1829, 1857, 1883, 1954, 2144, 2371, 2770, 3377, 3989, 4872, 5835, 7011, 8939],
    # 1900tr/m
    [1000, 1020, 1176, 1293, 1441, 1607, 1752, 1837, 1887, 1947, 2036, 2242, 2505, 2824, 3385, 3982, 4963, 5941, 7234, 9090],
    # 2100tr/m
    [1000, 1020, 1145, 1305, 1437, 1570, 1711, 1818, 1901, 2013, 2177, 2390, 2603, 2884, 3430, 4066, 5117, 6122, 7569, 9330],
    # 2300tr/m
    [1000, 1016, 1125, 1317, 1475, 1549, 1677, 1821, 1927, 2070, 2301, 2496, 2678, 2952, 3446, 4208, 5261, 6410, 7878, 9617],
    # 2600tr/m
    [1000, 1020, 1144, 1320, 1483, 1531, 1667, 1859, 1997, 2175, 2413, 2620, 2783, 3122, 3589, 4544, 5574, 6910, 8197, 9785],
    # 2750tr/m
    [1000, 1020, 1162, 1309, 1441, 1539, 1690, 1892, 2049, 2245, 2497, 2689, 2868, 3244, 3702, 4651, 5819, 7186, 8348, 9809],
    # 2900tr/m
    [1000, 1020, 1162, 1287, 1448, 1562, 1732, 1939, 2123, 2330, 2589, 2801, 2992, 3397, 3880, 4792, 6011, 7324, 8428, 9721],
    # 3200tr/m
    [1000, 1055, 1180, 1309, 1481, 1609, 1930, 2169, 2441, 2672, 2901, 3056, 3268, 3616, 4164, 5032, 6149, 7319, 8356, 9322],
    # 3500tr/m
    [1000, 1059, 1180, 1346, 1515, 1768, 2158, 2451, 2693, 2869, 3050, 3199, 3402, 3744, 4277, 5058, 6053, 6814, 7758, 8731],
    # 3750tr/m
    [1000, 1059, 1169, 1344, 1574, 1939, 2324, 2611, 2796, 2938, 3106, 3243, 3432, 3765, 4281, 5058, 5824, 6628, 7451, 8548],
    # 4000tr/m
    [1000, 1095, 1195, 1371, 1702, 2066, 2409, 2663, 2841, 2965, 3113, 3248, 3426, 3748, 4234, 5032, 5755, 6605, 7472, 8548],
    # 4250tr/m
    [1000, 1130, 1223, 1444, 1816, 2154, 2443, 2686, 2838, 2968, 3106, 3234, 3414, 3734, 4165, 4995, 5745, 6671, 7512, 8704],
    # 4500tr/m
    [1028, 1157, 1241, 1530, 1877, 2203, 2468, 2681, 2809, 2919, 3074, 3191, 3362, 3702, 4122, 5000, 5830, 6724, 7676, 9020],
    # 4750tr/m
    [1052, 1149, 1273, 1603, 1915, 2232, 2489, 2691, 2793, 2888, 3053, 3160, 3346, 3697, 4117, 5059, 5944, 6966, 8005, 9352],
    # 5000tr/m
    [1080, 1181, 1280, 1616, 1931, 2245, 2516, 2691, 2793, 2894, 3038, 3160, 3367, 3713, 4170, 5202, 6123, 7168, 8380, 9775],
    # 5250tr/m
    [1108, 1207, 1289, 1592, 1941, 2261, 2527, 2723, 2798, 2931, 3053, 3197, 3394, 3780, 4255, 5436, 6316, 7468, 8736, 10200],
    # 5500tr/m
    [1122, 1217, 1282, 1564, 1915, 2264, 2505, 2761, 2835, 2968, 3080, 3255, 3457, 3841, 4362, 5683, 6553, 7682, 9051, 10660],
    # 6000tr/m
    [1127, 1210, 1312, 1542, 1851, 2172, 2503, 2777, 2910, 3025, 3144, 3356, 3585, 4008, 4622, 6149, 7243, 8405, 9609, 11059],
    # 6500tr/m
    [1190, 1312, 1386, 1613, 1840, 2151, 2530, 2819, 2944, 3074, 3234, 3473, 3761, 4258, 4953, 6605, 7813, 9099, 10381, 11871],
    # 7000tr/m
    [1217, 1345, 1409, 1613, 1847, 2212, 2632, 2835, 2998, 3201, 3404, 3628, 3926, 4600, 5329, 7084, 8314, 9795, 11194, 12120],
    # 7500tr/m
    [1156, 1264, 1370, 1586, 1799, 2124, 2598, 2795, 2957, 3208, 3485, 3668, 4174, 4805, 5754, 7695, 8621, 10043, 11330, 12029],
    # 8000tr/m
    [1000, 1115, 1272, 1517, 1718, 1955, 2470, 2707, 2808, 3038, 3357, 3567, 4138, 4786, 5765, 7772, 8736, 10128, 11262, 11804],
    # 8500tr/m
    [1020, 1020, 1245, 1490, 1670, 1957, 2261, 2523, 2682, 2848, 3138, 3371, 3745, 4271, 5053, 7207, 8388, 9521, 10255, 11085],
    # 9000tr/m
    [1000, 1020, 1245, 1483, 1650, 1950, 2250, 2520, 2680, 2845, 3130, 3370, 3740, 4265, 5050, 7200, 8380, 9510, 10245, 11070],
]

# Conversion de la table en tableau numpy pour les calculs vectorisés
_tableau_numpy = np.array(TABLE_INJECTION, dtype=float)


def obtenir_duree_injection(regime_moteur: float, position_accelerateur: float) -> float:
    """
    Calcule la durée d'injection en microsecondes par interpolation bilinéaire.

    Cette fonction interroge la table d'injection extraite de l'ECU et retourne
    la durée d'ouverture de l'injecteur correspondant au point de fonctionnement
    actuel du moteur.

    Si les valeurs d'entrée se situent entre deux points de la grille, une
    interpolation bilinéaire est effectuée en utilisant les quatre points
    les plus proches dans la table.

    Paramètres
    ----------
    regime_moteur : float
        Régime moteur courant en tours par minute.
        Valeurs hors plage [0, 9000] sont ramenées aux bornes.
    position_accelerateur : float
        Position de l'accélérateur en pourcentage (0 à 100).
        Valeurs hors plage [0, 100] sont ramenées aux bornes.

    Retourne
    --------
    float
        Durée d'ouverture de l'injecteur en microsecondes (µs).
    """
    # Limitation des valeurs d'entrée aux bornes de la table
    regime_moteur        = np.clip(regime_moteur,        AXE_REGIME[0],        AXE_REGIME[-1])
    position_accelerateur = np.clip(position_accelerateur, AXE_ACCELERATEUR[0], AXE_ACCELERATEUR[-1])

    # ── Recherche des indices encadrants sur l'axe régime moteur ────────────
    indice_regime = np.searchsorted(AXE_REGIME, regime_moteur, side='right') - 1
    indice_regime = np.clip(indice_regime, 0, len(AXE_REGIME) - 2)

    regime_bas  = AXE_REGIME[indice_regime]
    regime_haut = AXE_REGIME[indice_regime + 1]

    # Facteur d'interpolation sur l'axe régime (compris entre 0 et 1)
    if regime_haut != regime_bas:
        facteur_regime = (regime_moteur - regime_bas) / (regime_haut - regime_bas)
    else:
        facteur_regime = 0.0

    # ── Recherche des indices encadrants sur l'axe accélérateur ─────────────
    indice_acc = np.searchsorted(AXE_ACCELERATEUR, position_accelerateur, side='right') - 1
    indice_acc = np.clip(indice_acc, 0, len(AXE_ACCELERATEUR) - 2)

    acc_bas  = AXE_ACCELERATEUR[indice_acc]
    acc_haut = AXE_ACCELERATEUR[indice_acc + 1]

    # Facteur d'interpolation sur l'axe accélérateur (compris entre 0 et 1)
    if acc_haut != acc_bas:
        facteur_acc = (position_accelerateur - acc_bas) / (acc_haut - acc_bas)
    else:
        facteur_acc = 0.0

    # ── Interpolation bilinéaire sur les quatre points encadrants ───────────
    # Les quatre coins du rectangle dans la table :
    valeur_bas_gauche  = _tableau_numpy[indice_regime,     indice_acc]
    valeur_bas_droite  = _tableau_numpy[indice_regime,     indice_acc + 1]
    valeur_haut_gauche = _tableau_numpy[indice_regime + 1, indice_acc]
    valeur_haut_droite = _tableau_numpy[indice_regime + 1, indice_acc + 1]

    # Combinaison pondérée des quatre valeurs
    duree_injection = (
        valeur_bas_gauche  * (1 - facteur_regime) * (1 - facteur_acc)
        + valeur_bas_droite  * (1 - facteur_regime) * facteur_acc
        + valeur_haut_gauche * facteur_regime        * (1 - facteur_acc)
        + valeur_haut_droite * facteur_regime        * facteur_acc
    )

    return duree_injection
