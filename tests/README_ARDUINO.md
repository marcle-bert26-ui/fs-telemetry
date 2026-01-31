# 🏎️ Arduino Telemetry Test

## Description

Ce code Arduino pour Mega simule des données de télémétrie réalistes pour tester le mode live de l'application fs-telemetry.

## Configuration

### Matériel requis
- Arduino Mega (ou Uno/compatible)
- Câble USB
- Ordinateur avec l'application fs-telemetry

### Configuration logicielle
1. Ouvrir le fichier `arduino_telemetry_test.ino` dans l'IDE Arduino
2. Sélectionner le bon port COM dans `config.py` (par défaut: COM3)
3. Téléverser le code sur l'Arduino

## Utilisation

### 1. Mode Live Test
```bash
# Modifier config.py pour désactiver le mode simulation
SIMULATION_MODE = False
SERIAL_PORT = "COM3"  # Adapter au port de votre Arduino

# Lancer l'application
python main.py
```

### 2. Données simulées

Le code simule un cycle de conduite réaliste :
- **Idle** (1s) : Démarrage
- **Accélération** (8s) : 0 → 120 km/h
- **Croisière** (5s) : Vitesse constante avec variations
- **Virage** (3s) : Forces latérales et températures des pneus
- **Freinage** (4s) : Arrêt complet
- **Arrêt** (2s) : Pause avant de recommencer

### 3. Format des données

Les données sont envoyées au format CSV à 50Hz :
```
time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr
```

### 4. Paramètres simulés

- **Vitesse** : 0-120 km/h (réaliste pour Formula Student)
- **RPM** : 800-12000 (moteur typique)
- **Throttle** : 0-100%
- **Température batterie** : 55-70°C
- **Forces G** : -1.5g à +1.2g (accélération, freinage, virages)
- **GPS** : Simulation Circuit Paul Ricard
- **Températures pneus** : 68-95°C (évolution progressive)

## Dépannage

### Problèmes courants
1. **Port COM incorrect** : Vérifier le port dans l'IDE Arduino et `config.py`
2. **Baud rate** : Assurez-vous que c'est 9600 dans les deux configurations
3. **Pas de données** : Vérifier que l'Arduino est bien connecté et le code téléversé

### Vérification
Ouvrir le Moniteur Série de l'IDE Arduino (9600 baud) pour voir les données en direct.

## Tests suggérés

1. **Test basic** : Vérifier que l'application reçoit les données
2. **Test stress** : Laisser tourner plusieurs minutes
3. **Test arrêt/démarrage** : Débrancher/rebrancher l'Arduino
4. **Test logging** : Vérifier que les données sont bien sauvegardées en CSV
