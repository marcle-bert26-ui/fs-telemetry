/*
 * 🏎️ Formula Student Telemetry Test for Arduino Mega
 * 
 * Ce code simule des données de télémétrie réalistes pour tester le mode live
 * de l'application fs-telemetry. Il envoie des données au format CSV attendu
 * par l'application via le port série.
 * 
 * Format CSV: time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr
 * 
 * Configuration:
 * - Baud rate: 115200
 * - Fréquence: 50Hz (une donnée toutes les 20ms)
 * - Port: COM3 (configurable dans config.py)
 */

// Variables de simulation
unsigned long startTime = 0;
unsigned long lastDataTime = 0;
const unsigned long DATA_INTERVAL = 20; // 50Hz = 20ms

// État de la simulation
enum DrivingState {
  IDLE,
  ACCELERATING,
  CRUISING,
  BRAKING,
  CORNERING,
  STOPPED
};

DrivingState currentState = IDLE;
unsigned long stateStartTime = 0;
float currentSpeed = 0.0;
int currentRPM = 0;
float currentThrottle = 0.0;
float currentBatteryTemp = 55.0;

// Variables pour les capteurs
float gForceLat = 0.0;
float gForceLong = 0.0;
float gForceVert = 1.0;
float accelX = 0.0;
float accelY = 0.0;
float accelZ = 0.0;

// GPS (simulation Circuit Paul Ricard)
float gpsLatitude = 43.2509;
float gpsLongitude = 5.7951;
float gpsAltitude = 150.0;

// Températures des pneus
float tireTempFL = 75.0;
float tireTempFR = 75.0;
float tireTempRL = 73.0;
float tireTempRR = 73.0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // Attendre la connexion série
  }
  
  startTime = millis();
  stateStartTime = millis();
  
  Serial.println("🏎️ Arduino Telemetry Test Started");
  Serial.println("Format: time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr");
  Serial.println("time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr");
}

void loop() {
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - startTime;
  
  // Envoyer des données à 50Hz
  if (currentTime - lastDataTime >= DATA_INTERVAL) {
    lastDataTime = currentTime;
    
    // Mettre à jour l'état de conduite
    updateDrivingState(currentTime);
    
    // Simuler les données de télémétrie
    simulateTelemetryData(currentTime);
    
    // Envoyer les données au format CSV
    sendTelemetryData(elapsedTime);
  }
}

void updateDrivingState(unsigned long currentTime) {
  unsigned long timeInState = currentTime - stateStartTime;
  
  switch (currentState) {
    case IDLE:
      if (timeInState > 1000) {
        currentState = ACCELERATING;
        stateStartTime = currentTime;
      }
      break;
      
    case ACCELERATING:
      currentSpeed += 0.8;
      currentRPM += 150;
      currentThrottle = min(1.0, currentThrottle + 0.02);
      gForceLong = 0.8; // Accélération longitudinale
      
      if (currentSpeed >= 120.0 || timeInState > 8000) {
        currentState = CRUISING;
        stateStartTime = currentTime;
      }
      break;
      
    case CRUISING:
      currentSpeed = 120.0 + sin(timeInState * 0.001) * 5.0;
      currentRPM = 9500 + sin(timeInState * 0.001) * 500;
      currentThrottle = 0.85;
      gForceLong = 0.0;
      
      if (timeInState > 5000) {
        currentState = CORNERING;
        stateStartTime = currentTime;
      }
      break;
      
    case CORNERING:
      currentSpeed = 80.0 + sin(timeInState * 0.002) * 10.0;
      currentRPM = 6500 + sin(timeInState * 0.002) * 800;
      currentThrottle = 0.6;
      gForceLat = sin(timeInState * 0.002) * 1.2; // Force latérale dans le virage
      gForceLong = -0.3; // Légère décélération
      
      // Simuler les changements de température des pneus
      tireTempFL += abs(gForceLat) * 0.1;
      tireTempFR += abs(gForceLat) * 0.1;
      
      if (timeInState > 3000) {
        currentState = BRAKING;
        stateStartTime = currentTime;
      }
      break;
      
    case BRAKING:
      currentSpeed = max(0.0, currentSpeed - 1.5);
      currentRPM = max(800, currentRPM - 300);
      currentThrottle = 0.0;
      gForceLong = -1.5; // Freinage fort
      gForceLat = 0.0;
      
      if (currentSpeed <= 5.0 || timeInState > 4000) {
        currentState = STOPPED;
        stateStartTime = currentTime;
      }
      break;
      
    case STOPPED:
      currentSpeed = 0.0;
      currentRPM = 800;
      currentThrottle = 0.0;
      gForceLong = 0.0;
      gForceLat = 0.0;
      
      if (timeInState > 2000) {
        // Recommencer le cycle
        currentState = IDLE;
        stateStartTime = currentTime;
        // Réinitialiser les températures
        tireTempFL = 75.0;
        tireTempFR = 75.0;
        tireTempRL = 73.0;
        tireTempRR = 73.0;
      }
      break;
  }
  
  // Limiter les valeurs
  currentSpeed = constrain(currentSpeed, 0.0, 250.0);
  currentRPM = constrain(currentRPM, 800, 12000);
  currentThrottle = constrain(currentThrottle, 0.0, 1.0);
}

void simulateTelemetryData(unsigned long currentTime) {
  // Température de la batterie (augmente avec le RPM)
  currentBatteryTemp = 55.0 + (currentRPM / 12000.0) * 15.0;
  
  // Forces G (avec un peu de bruit)
  gForceVert = 1.0 + sin(currentTime * 0.01) * 0.1;
  
  // Accélérations (conversion des forces G)
  accelX = gForceLat * 9.81;
  accelY = gForceLong * 9.81;
  accelZ = gForceVert * 9.81;
  
  // Simulation GPS (mouvement sur le circuit)
  float timeFactor = currentTime * 0.00001;
  gpsLatitude += sin(timeFactor) * 0.00001;
  gpsLongitude += cos(timeFactor) * 0.00001;
  
  // Températures des pneus (évolution progressive)
  tireTempFL = constrain(tireTempFL + (currentSpeed / 100.0) * 0.01 - 0.005, 70.0, 95.0);
  tireTempFR = constrain(tireTempFR + (currentSpeed / 100.0) * 0.01 - 0.005, 70.0, 95.0);
  tireTempRL = constrain(tireTempRL + (currentSpeed / 100.0) * 0.008 - 0.004, 68.0, 90.0);
  tireTempRR = constrain(tireTempRR + (currentSpeed / 100.0) * 0.008 - 0.004, 68.0, 90.0);
}

void sendTelemetryData(unsigned long elapsedTime) {
  // Formater et envoyer les données au format CSV
  Serial.print(elapsedTime);
  Serial.print(";");
  Serial.print(currentSpeed, 1);
  Serial.print(";");
  Serial.print(currentRPM);
  Serial.print(";");
  Serial.print(currentThrottle, 2);
  Serial.print(";");
  Serial.print(currentBatteryTemp, 1);
  Serial.print(";");
  Serial.print(gForceLat, 2);
  Serial.print(";");
  Serial.print(gForceLong, 2);
  Serial.print(";");
  Serial.print(gForceVert, 2);
  Serial.print(";");
  Serial.print(accelX, 1);
  Serial.print(";");
  Serial.print(accelY, 1);
  Serial.print(";");
  Serial.print(accelZ, 1);
  Serial.print(";");
  Serial.print(gpsLatitude, 6);
  Serial.print(";");
  Serial.print(gpsLongitude, 6);
  Serial.print(";");
  Serial.print(gpsAltitude, 1);
  Serial.print(";");
  Serial.print(tireTempFL, 1);
  Serial.print(";");
  Serial.print(tireTempFR, 1);
  Serial.print(";");
  Serial.print(tireTempRL, 1);
  Serial.print(";");
  Serial.println(tireTempRR, 1);
}
