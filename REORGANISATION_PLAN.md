# 📁 Organisation Optimisée du Projet fs-telemetry

## 🎯 Objectif
Structurer le projet de manière logique et professionnelle pour faciliter la maintenance et l'évolution.

## 📂 Structure Proposée

```
fs-telemetry/
├── 📄 Fichiers principaux
│   ├── README.md                    # Documentation principale
│   ├── app_config.py               # Configuration de l'application
│   ├── main.py                     # Point d'entrée principal
│   ├── run.py                      # Script de lancement
│   └── start.py                    # Alternative de lancement
│
├── 📁 src/                        # Code source organisé par fonctionnalités
│   ├── 📁 core/                   # Cœur du système
│   │   ├── telemetry_manager.py     # Gestion des données
│   │   ├── telemetry_source.py      # Interface des sources
│   │   └── __init__.py
│   │
│   ├── 📁 data/                   # Gestion des données
│   │   ├── csv_parser.py           # Parser CSV
│   │   ├── csv_logger.py           # Logger CSV
│   │   ├── csv_source.py           # Source CSV
│   │   └── __init__.py
│   │
│   ├── 📁 sources/                # Sources de données externes
│   │   ├── serial_source.py        # Source série (Arduino)
│   │   └── __init__.py
│   │
│   ├── 📁 gui/                     # Interface graphique
│   │   ├── main_window.py          # Fenêtre principale
│   │   ├── live_mode_widget.py     # Mode live
│   │   ├── replay_mode_widget.py    # Mode replay
│   │   ├── temporal_analysis_widget.py # Analyse temporelle
│   │   ├── file_selector_widget.py  # Sélecteur de fichiers
│   │   └── __init__.py
│   │
│   ├── 📁 visualization/           # Composants de visualisation
│   │   ├── telemetry_charts.py     # Graphiques de télémétrie
│   │   ├── spider_charts.py        # Graphiques spider
│   │   └── __init__.py
│   │
│   ├── 📁 utils/                   # Utilitaires
│   │   ├── console_display.py      # Affichage console
│   │   ├── console_handler.py      # Gestion console
│   │   ├── replay_thread.py        # Thread de replay
│   │   └── __init__.py
│   │
│   ├── gui_app.py                 # Application GUI
│   └── __init__.py
│
├── 📁 tests/                       # Tests organisés par type
│   ├── 📁 unit/                   # Tests unitaires
│   │   ├── test_csv_parser.py
│   │   ├── test_csv_logger.py
│   │   ├── test_csv_source.py
│   │   ├── test_telemetry_manager.py
│   │   └── __init__.py
│   │
│   ├── 📁 integration/            # Tests d'intégration
│   │   ├── test_integration.py
│   │   └── __init__.py
│   │
│   ├── 📁 gui/                    # Tests GUI
│   │   ├── test_gui_components.py
│   │   ├── test_temporal.py
│   │   └── __init__.py
│   │
│   ├── 📁 fixtures/               # Données de test
│   │   ├── sample_data.csv
│   │   ├── enhanced_sample_data.csv
│   │   ├── full_circuit_data.csv
│   │   └── __init__.py
│   │
│   ├── conftest.py                # Configuration pytest
│   └── __init__.py
│
├── 📁 data/                        # Données utilisateur
│   ├── 📁 samples/                # Exemples de données
│   ├── 📁 logs/                   # Logs de l'application
│   └── 📁 exports/                # Exportations
│
├── 📁 docs/                        # Documentation
│   ├── 📁 api/                    # Documentation API
│   ├── 📁 user_guide/             # Guide utilisateur
│   ├── 📁 developer_guide/         # Guide développeur
│   └── 📁 architecture/           # Documentation architecture
│
├── 📁 assets/                      # Ressources statiques
│   ├── 📁 icons/                  # Icônes
│   ├── 📁 images/                 # Images
│   └── 📁 styles/                 # Styles CSS/thèmes
│
├── 📁 scripts/                     # Scripts utilitaires
│   ├── setup_dev.py               # Configuration développement
│   ├── build_exe.py               # Création exécutable
│   └── run_tests.py               # Lancement tests
│
├── 📁 tools/                       # Outils de développement
│   ├── debug_cursors.py           # Débogage curseurs
│   └── test_new_charts.py        # Test graphiques
│
├── 📁 executables/                 # Exécutables générés
│
├── 📁 .github/                     # Configuration GitHub
│   └── workflows/
│       └── tests.yml
│
├── 📄 Configuration
│   ├── requirements.txt            # Dépendances
│   ├── requirements-ci.txt         # Dépendances CI
│   ├── pyproject.toml             # Configuration projet
│   ├── pytest.ini                # Configuration pytest
│   ├── pyrightconfig.json         # Configuration Pyright
│   └── .gitignore                # Fichiers ignorés
│
├── 📄 Documentation
│   ├── CHANGELOG.md               # Historique modifications
│   ├── CONTRIBUTING.md            # Guide contribution
│   ├── INSTALL.md                 # Instructions installation
│   ├── LICENSE                    # Licence
│   └── PUSH_INSTRUCTIONS.md      # Instructions push
│
└── 📁 build/                       # Fichiers de build
    └── dist/                     # Distribution
```

## 🔄 Plan de Migration

### Étape 1: Créer la nouvelle structure
```bash
mkdir -p src/core src/data src/sources src/gui src/visualization src/utils
mkdir -p tests/unit tests/integration tests/gui tests/fixtures
mkdir -p data/samples data/logs data/exports
mkdir -p docs/api docs/user_guide docs/developer_guide docs/architecture
mkdir -p assets/icons assets/images assets/styles
mkdir -p scripts build/dist
```

### Étape 2: Déplacer les fichiers
- `src/telemetry_manager.py` → `src/core/`
- `src/telemetry_source.py` → `src/core/`
- `src/csv_*.py` → `src/data/`
- `src/serial_source.py` → `src/sources/`
- `src/*_widget.py` → `src/gui/`
- `src/*_charts.py` → `src/visualization/`
- `src/console_*.py` → `src/utils/`
- `src/replay_thread.py` → `src/utils/`

### Étape 3: Mettre à jour les imports
- Mettre à jour tous les imports relatifs
- Ajouter les fichiers `__init__.py` nécessaires

### Étape 4: Nettoyer
- Supprimer les fichiers temporaires
- Mettre à jour la documentation

## ✅ Avantages

1. **Clarté**: Chaque dossier a une responsabilité claire
2. **Maintenance**: Facile de trouver et modifier le code
3. **Scalabilité**: Simple d'ajouter de nouvelles fonctionnalités
4. **Tests**: Organisation logique des tests par type
5. **Documentation**: Séparation claire de la documentation
6. **Professionnalisme**: Structure standard de projet Python

## 🚀 Prêt à commencer ?

Dites-moi si vous voulez que j'exécute cette réorganisation !
