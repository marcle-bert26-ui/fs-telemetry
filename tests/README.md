# Formula Student Telemetry - Test Suite

This folder contains all unit tests to verify that each function works correctly.

## 📋 Test Files

| File | Tests |
|---------|-------|
| `test_csv_parser.py` | CSV data parsing (format conversion) |
| `test_telemetry_manager.py` | Data management (storage, history, stats) |
| `test_csv_logger.py` | CSV file logging |
| `test_csv_source.py` | CSV file reading |

## 🚀 Running Tests

### Install pytest
```bash
pip install pytest pytest-cov
```

### Run all tests
```bash
pytest
```

### Run tests with detailed output
```bash
pytest -v
```

### Run a specific test file
```bash
pytest tests/test_csv_parser.py -v
```

### Run a specific test function
```bash
pytest tests/test_csv_parser.py::TestParseCSVLine::test_valid_csv_line -v
```

### Check code coverage
```bash
pytest --cov=. --cov-report=html
```
This creates an HTML report in `htmlcov/index.html`

## 📝 Example Output

```
tests/test_csv_parser.py::TestParseCSVLine::test_valid_csv_line PASSED
tests/test_csv_parser.py::TestParseCSVLine::test_csv_line_with_whitespace PASSED
tests/test_csv_parser.py::TestParseCSVLine::test_header_line_returns_none PASSED
tests/test_telemetry_manager.py::TestTelemetryManager::test_manager_initialization PASSED
tests/test_csv_logger.py::TestCSVLogger::test_logger_writes_data PASSED
...

======================== 30 passed in 2.34s ========================
```

## 🧪 What's Tested

### CSV Parser (`test_csv_parser.py`)
- ✅ Parse a valid CSV line
- ✅ Handle whitespace and newlines
- ✅ Ignore headers
- ✅ Handle errors (wrong format, invalid values)
- ✅ Parse large values and zeros
- ✅ Handle negative values

### Telemetry Manager (`test_telemetry_manager.py`)
- ✅ Proper initialization
- ✅ Update with single data point
- ✅ Update with multiple data points
- ✅ Get current data
- ✅ Get history
- ✅ Calculate statistics (min, max, average)
- ✅ Clear history

### CSV Logger (`test_csv_logger.py`)
- ✅ Create files
- ✅ Écrit les en-têtes
- ✅ Enregistre les données
- ✅ Génère des noms de fichier uniques
- ✅ Ferme les fichiers correctement

### CSV Source (`test_csv_source.py`)
- ✅ Ouvre les fichiers CSV
- ✅ Lit les lignes une par une
- ✅ Gère la fin du fichier
- ✅ Gère les fichiers manquants
- ✅ Compte les lignes

## 📊 Fichier d'exemple

`sample_data.csv` - Données d'essai simulant un vrai run de Formula Student:
- 19 lignes de données
- Accélération, vitesse max, puis décélération
- Valeurs réalistes (RPM, température, etc.)

## 🔍 Ajouter de nouveaux tests

Pour tester une nouvelle fonction:

1. Créez un test dans le fichier approprié:
```python
def test_ma_nouvelle_fonction(self):
    """Description du test"""
    result = ma_fonction(input)
    assert result == expected_output
```

2. Lancez le test:
```bash
pytest tests/test_mon_module.py::TestMaClasse::test_ma_nouvelle_fonction -v
```

## 💡 Bonne pratique

- Un test = une seule responsabilité
- Les tests doivent être indépendants
- Utilisez des fixtures pour réutiliser du code
- Testez les cas normaux ET les erreurs
