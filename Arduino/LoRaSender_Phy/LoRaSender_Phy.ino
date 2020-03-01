#include <SPI.h>
#include <LoRa.h>
#include <ArduinoJson.h>
#include "DHT.h"

#define DHTTYPE DHT11
#define DHTPIN 5

// Parameters you can play with :
int txPower = 14; // from 0 to 20, default is 14
int spreadingFactor = 12; // from 7 to 12, default is 12
long signalBandwidth = 125E3; // 7.8E3, 10.4E3, 15.6E3, 20.8E3, 31.25E3,41.7E3,62.5E3,125E3,250E3,500e3, default is 125E3
int codingRateDenominator=5; // Numerator is 4, and denominator from 5 to 8, default is 5
int preambleLength=8; // from 2 to 20, default is 8

#define SS 10
#define RST 8
#define DI0 2
#define BAND 865E6  // Here you define the frequency carrier

DHT dht(DHTPIN, DHTTYPE); //instance de l'interface du capteur

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("LoRa Sender");
  Serial.print("SetFrequency : ");
  Serial.print(BAND);
  Serial.println("Hz");
  Serial.print("SetSpreadingFactor : SF");
  Serial.println(spreadingFactor);

  SPI.begin();
  LoRa.setPins(SS,RST,DI0);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
 LoRa.setTxPower(txPower,1);
 LoRa.setSpreadingFactor(spreadingFactor);
 LoRa.setSignalBandwidth(signalBandwidth);
 LoRa.setCodingRate4(codingRateDenominator);
 LoRa.setPreambleLength(preambleLength);
// LoRa.setPolarity(1);
 //LoRa.setFSK(); 
 dht.begin(); // Initialise le DHT
}

void loop() {
  //lire les données du capteur
  float hf = dht.readHumidity();
  float tf = dht.readTemperature();
  //float f = dht.readTemperature(true);

  //test de lecture des données du capteur
  if(isnan(hf) || isnan(tf)){
    Serial.println(F("Failed to read from DHT11 sensor!"));
    //return;
  }else{
    //calcul des indices de températures
    int hic = dht.computeHeatIndex(tf, hf, false);
    //float hif = dht.computeHeatIndex(f, h);
    int h=(int)hf;
    int t=(int)tf;
    
    //affichage des données lues
    Serial.print(F("Humidity: "));
    Serial.print(h);
    Serial.print(F("%  Temperature: "));
    Serial.print(t);
    Serial.print(F("°C "));
    //Serial.print(f);
    Serial.print(F("Indice de température: ")); // HeatIndex = indice de temperature (pour obtenir la température ressentie)
    Serial.print(hic);
    Serial.println(F("°C "));
    //Serial.print(hif);
    //Serial.println(F("°F"));

    //String donnees = String(h)+";"+String(t)+";"+String(hic);
    char data[10];
    sprintf(data, "%03d;%02d;%02d", h, t, hic);
    
    // send packet LoRa
    LoRa.beginPacket();
    LoRa.print(data);
    LoRa.endPacket();
    Serial.print("Sending packet with payload { ");
    Serial.print(data);
    Serial.println(" }");
  }
  delay(1000);
}
