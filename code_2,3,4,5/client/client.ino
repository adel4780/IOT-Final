#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const char* ssid = "Tartarous";
const char* password = "ajhv6004";
const char* host = "https://danial.pythonanywhere.com/getStatus";

HTTPClient http;
WiFiClientSecure client2;
int ledPin = 4;
String status = "OFF";
int time_on = 0;
int time_off = 0;

void checkStatus() {
  client2.setInsecure();
  http.begin(client2, host); 
  int httpCode = http.GET();
  if (httpCode > 0) {
    String payload = http.getString();
    // Serial.println(payload);
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);
    status = doc["status"].as<String>();
    time_on = doc["scheduling"]["time_on"];
    time_off = doc["scheduling"]["time_off"];
  } else {
    Serial.printf("Error on HTTP request, code: %d\n", httpCode);
  }
  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(ledPin, OUTPUT);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void loop() {
  if (status == "OFF") {
    digitalWrite(ledPin, LOW);
  }
  if (status == "ON") {
    digitalWrite(ledPin, HIGH);
  }
  if (status == "Blink") {
    digitalWrite(ledPin, HIGH);
    delay(time_on);
    digitalWrite(ledPin, LOW);
    delay(time_off);
  }
  Serial.printf("Status: %s, time_ON: %d ms, time_OFF: %d ms\n", status.c_str(), time_on, time_off);
  delay(10);
  checkStatus();
}
