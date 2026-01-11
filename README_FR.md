# Système de Télémétrie Formula Student

🏎️ Application professionnelle de télémétrie en temps réel pour véhicules Formula Student.

[![Tests](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml/badge.svg)](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

**[Documentation Complète](README_APP.md)** • **[Guide d'Installation](INSTALL.md)** • **[Contribution](CONTRIBUTING.md)** • **[Historique](CHANGELOG.md)**

---

## ✨ Caractéristiques

### 🟢 MODE EN DIRECT
- Acquisition de données Arduino en temps réel
- Affichage de télémétrie en direct (Vitesse, RPM, Accélérateur, Température)
- Enregistrement automatique en CSV
- Statistiques en temps réel

### 🔄 MODE REPLAY  
- Charger et analyser des fichiers CSV enregistrés
- Statistiques et analytiques de session
- Visualisation de données historiques
- Métriques de performance

### 📊 Capacités principales
- ✅ Interface graphique professionnelle PyQt5
- ✅ Architecture multi-thread
- ✅ Tests complets (35+ tests)
- ✅ Multi-plateforme (Windows/Linux/macOS)
- ✅ Enregistrement de données CSV
- ✅ Calcul des statistiques
- ✅ Gestion des erreurs robuste

---

## 🚀 Démarrage Rapide

### Windows
```bash
double-cliquez sur run.bat    # Mode GUI
# ou
python review.py             # Vue d'ensemble
```

### Linux / macOS
```bash
bash run.sh                   # Mode GUI
# ou
python3 review.py            # Vue d'ensemble
```

Ou manuellement :
```bash
python app.py                # Mode GUI
python main.py               # Mode CLI
python review.py             # Résumé et statistiques
```

---

## 📋 Configuration Requise

- **Python** : 3.8 ou supérieur
- **OS** : Windows, Linux ou macOS
- **Dépendances** : Voir [requirements.txt](requirements.txt)
- **Arduino** : (Optionnel, pour le MODE EN DIRECT)

---

## 📦 Installation

### Installation Rapide
```bash
# Cloner le dépôt
git clone https://github.com/marcle-bert26-ui/fs-telemetry.git
cd fs-telemetry

# Créer un environnement virtuel
python -m venv venv

# Activer (Windows)
venv\Scripts\activate
# ou (Linux/macOS)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

**Pour des instructions détaillées**, voir [INSTALL.md](INSTALL.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README_APP.md](README_APP.md) | Documentation complète des fonctionnalités |
| [INSTALL.md](INSTALL.md) | Guide d'installation spécifique à chaque plateforme |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Directives pour les développeurs |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions |
| [tests/README.md](tests/README.md) | Documentation des tests |

---

## 🏗️ Structure du Projet

```
fs-telemetry/
├── gui/                 # Application graphique
├── acquisition/         # Acquisition de données
├── parsing/            # Analyse de données
├── data/               # Gestion des données
├── log_handlers/       # Enregistrement CSV
├── visualization/      # Utilitaires d'affichage
├── tests/              # Tests unitaires
├── app.py              # Point d'entrée GUI
├── main.py             # Point d'entrée CLI
├── config.py           # Configuration
└── requirements.txt    # Dépendances
```

---

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/ -v

# Exécuter avec couverture de code
pytest tests/ --cov=. --cov-report=html

# Exécuter un test spécifique
pytest tests/test_csv_parser.py::TestParseCSVLine::test_valid_csv_line -v
```

**Résultats des tests** : ✅ 35/35 tests réussis

---

## ⚙️ Configuration

Modifier `config.py` :

```python
# Configuration Série
SERIAL_PORT = "COM3"        # Changer au port Arduino
SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 1

# Enregistrement
LOG_DIRECTORY = "data_logs"
LOG_FILENAME_PREFIX = "run"

# Format CSV
CSV_DELIMITER = ";"
CSV_HEADER = ["time_ms", "speed_kmh", "rpm", "throttle", "battery_temp"]

# Mode
SIMULATION_MODE = False     # Mettre à True pour le mode replay
```

---

## 🔌 Intégration Arduino

Format CSV attendu :
```
time_ms;speed_kmh;rpm;throttle;battery_temp
100;10.5;2000;25;35.2
200;15.3;2500;40;35.5
```

Trouver votre port Arduino :
- **Windows** : Gestionnaire de périphériques → Ports (COM et LPT)
- **Linux** : `ls /dev/ttyUSB*`
- **macOS** : `ls /dev/cu.*`

---

## 🤝 Contribution

Nous accueillons les contributions ! S'il vous plaît :

1. Forker le dépôt
2. Créer une branche de fonctionnalité (`git checkout -b feature/ma-fonction`)
3. Faire vos modifications
4. Écrire des tests pour les nouvelles fonctionnalités
5. Vérifier que tous les tests réussissent
6. Commiter clairement (`git commit -m "Ajouter ma fonction"`)
7. Pousser et ouvrir une Pull Request

**[Directives de Contribution](CONTRIBUTING.md)**

---

## 📝 Licence

Ce projet est sous licence **MIT** - voir [LICENSE](LICENSE) pour plus de détails.

---

## 🔗 Liens

- [Dépôt GitHub](https://github.com/marcle-bert26-ui/fs-telemetry)
- [Signaler des Problèmes](https://github.com/marcle-bert26-ui/fs-telemetry/issues)
- [Discussions](https://github.com/marcle-bert26-ui/fs-telemetry/discussions)
- [Site Web](https://eigsiformulateam.fr/)
- [Formula Student](https://www.formulastudent.com/)

---

## 💡 Astuces et Conseils

### Performance
- Fermer les autres applications pour une meilleure réactivité
- Utiliser un SSD pour des opérations CSV plus rapides
- Mettre à jour régulièrement Python et les dépendances

### Dépannage
- Port série non trouvé ? Vérifier le Gestionnaire de périphériques
- ModuleNotFoundError ? Installer les dépendances : `pip install -r requirements.txt`
- GUI ne démarre pas ? Vérifier PyQt5 : `pip install PyQt5`

### Tâches Courantes
```bash
# Créer un nouveau journal CSV
python main.py

# Analyser des données enregistrées  
python main.py  # Mettre SIMULATION_MODE = True

# Exécuter les tests avec couverture
pytest --cov=.

# Vérifier les problèmes
pylint *.py acquisition/*.py
```

---

## 🎓 Valeur Pédagogique

Ce projet démontre :
- ✅ Architecture d'application Python professionnelle
- ✅ Développement d'interface graphique avec PyQt5
- ✅ Communication série avec matériel
- ✅ Traitement et analyse de données
- ✅ Bonnes pratiques des tests unitaires
- ✅ Documentation et configuration de projet
- ✅ Contrôle de version et CI/CD

Parfait pour les étudiants et développeurs apprenant Python en conditions réelles !

---

## 🎯 Feuille de Route

### Version 1.1.0 (Prévue)
- [ ] Graphiques et jauges en temps réel
- [ ] Export de données (JSON, Excel)
- [ ] Filtrage avancé

### Version 1.2.0 (Futur)
- [ ] Comparaison multi-session
- [ ] Interface web
- [ ] Stockage cloud

---

## 📞 Support

Besoin d'aide ?
1. Vérifier [INSTALL.md](INSTALL.md) pour les problèmes courants
2. Consulter [README_APP.md](README_APP.md) pour les fonctionnalités
3. Ouvrir un [problème sur GitHub](https://github.com/marcle-bert26-ui/fs-telemetry/issues)

---

<div align="center">

**Fait avec ❤️ pour Formula Student**

[⬆ Retour au haut](#système-de-télémétrie-formula-student)

</div>
