#include "DHT.h"

#define DHTTYPE DHT11
#define DHTPIN 2
#define IN1 3
#define IN2 4
#define ENA 5

DHT dht(DHTPIN, DHTTYPE); //instance de l'interface du capteur
int PinLed = 13; //LED témoin sur pin 13
int seuil_alerte = 28; // valeur du seuil a partir duquel l'alerte sécheresse est donnée 

void moteur_stop(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
}

void moteur_avancer(){
  analogWrite(ENA, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 255);
  delay(60);
  analogWrite(ENA, 127);
  delay(2000);
}

void moteur_reculer(){
  analogWrite(ENA, 0);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 255);
  delay(60);
  analogWrite(ENA, 127);
  delay(2000);
}

void setup(){
  Serial.begin(9600);
  Serial.println("DHT11: Affichage des données de la temperature et l'humidité");
  pinMode(PinLed, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  //moteur_stop();
  dht.begin();
}

void loop(){
  //lire les données du capteur
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  String s=Serial.readString();
  int n=s.length();
  char s2[n];
  s.toCharArray(s2,n);
  //Serial.println(s);
  Serial.write(s2);

  //test de lecture
  if (isnan(h) || isnan(t) || isnan(f)) {
    //Serial.println(F("Failed to read from DHT11 sensor!"));
    return;
  }

  //calcul des indices de températures
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  //réaction de la LED
  if(hic > seuil_alerte){
    digitalWrite(PinLed, HIGH); // LED Allumée
    //moteur_avancer();
  }else{
    digitalWrite(PinLed, LOW); //LED Eteinte
    //moteur_stop();
  }
  delay(1000);

  //affichage des données lues
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
