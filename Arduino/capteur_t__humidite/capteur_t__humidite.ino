//On rajoute une LEd témoin sur pin 13

#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
int PinLed = 13;
int seuil_alerte = 28; // valeur du seuil apartir duquel l'alerte sécheresse est donnée 


void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 Affichage des données de la temperature et l'humidité!");
  pinMode(PinLed, OUTPUT);

  dht.begin();
}

void loop() {  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT11 sensor!"));
    return;
  }

  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  if(hic > seuil_alerte){
    digitalWrite(PinLed, HIGH); // LED Allumée
  }else{
    digitalWrite(PinLed, LOW); //LED Eteinte
  }
  delay(1000);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  indice de température: ")); // HeatIndex = indice de temperature (pour obtenir la température ressentie)
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));
  
  
}