"""
Example Arduino sketch for Formula Student telemetry data transmission.

This shows how to format and send telemetry data to the Python application.
Adjust sensor reading functions based on your actual hardware.
"""

// Pin definitions (adjust to your setup)
#define SPEED_SENSOR_PIN A0
#define RPM_SENSOR_PIN A1
#define THROTTLE_PIN A2
#define TEMP_SENSOR_PIN A3

void setup() {
  Serial.begin(115200);
  
  // Send header once at startup
  delay(100);
  Serial.println("time_ms;speed_kmh;rpm;throttle;battery_temp");
  
  // Initialize sensor pins
  pinMode(SPEED_SENSOR_PIN, INPUT);
  pinMode(RPM_SENSOR_PIN, INPUT);
  pinMode(THROTTLE_PIN, INPUT);
  pinMode(TEMP_SENSOR_PIN, INPUT);
}

void loop() {
  // Timestamp
  unsigned long time_ms = millis();
  
  // Read sensors
  float speed_kmh = readSpeed();
  int rpm = readRPM();
  float throttle = readThrottle();
  float battery_temp = readBatteryTemp();
  
  // Send as CSV: time_ms;speed_kmh;rpm;throttle;battery_temp
  Serial.print(time_ms);           Serial.print(";");
  Serial.print(speed_kmh, 1);      Serial.print(";");
  Serial.print(rpm);               Serial.print(";");
  Serial.print(throttle, 2);       Serial.print(";");
  Serial.println(battery_temp, 1);
  
  // 50 Hz = 20ms per reading (adjust to your needs)
  delay(20);
}

// ============================================================
// Sensor reading functions - CUSTOMIZE FOR YOUR HARDWARE
// ============================================================

float readSpeed() {
  // Example: Convert analog reading to km/h
  // Adjust calibration constants for your speed sensor
  int raw = analogRead(SPEED_SENSOR_PIN);
  float voltage = (raw / 1023.0) * 5.0;
  float speed = voltage * 18.0;  // Your calibration factor
  return constrain(speed, 0.0, 100.0);
}

int readRPM() {
  // Example: Read RPM from hall sensor or other source
  int raw = analogRead(RPM_SENSOR_PIN);
  int rpm = map(raw, 0, 1023, 0, 12000);  // 0-12000 RPM range
  return rpm;
}

float readThrottle() {
  // Example: Throttle as percentage (0-100%)
  int raw = analogRead(THROTTLE_PIN);
  float throttle = (raw / 1023.0) * 100.0;
  return throttle;
}

float readBatteryTemp() {
  // Example: Temperature from thermistor
  int raw = analogRead(TEMP_SENSOR_PIN);
  // NTC thermistor conversion (simplified)
  float voltage = (raw / 1023.0) * 5.0;
  // Replace with actual thermistor calibration
  float temp = 20.0 + (voltage - 2.5) * 10.0;  // Rough conversion
  return constrain(temp, -10.0, 100.0);
}

/*
 * ============================================================
 * CALIBRATION TIPS
 * ============================================================
 * 
 * 1. SPEED SENSOR:
 *    - Measure actual speed vs analog reading
 *    - Create lookup table if not linear
 * 
 * 2. RPM SENSOR:
 *    - Pulses per revolution × frequency = RPM
 *    - Use interrupt for better accuracy
 * 
 * 3. THROTTLE:
 *    - Read potentiometer at 0% and 100%
 *    - Map accordingly
 * 
 * 4. TEMPERATURE:
 *    - Use proper thermistor Steinhart-Hart equation
 *    - Or reference table lookup
 * 
 * ============================================================
 */
