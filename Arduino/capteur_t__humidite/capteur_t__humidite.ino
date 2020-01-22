#include <WiFi.h>
#include <SPI.h>
#include "DHT.h"

#define DHTTYPE DHT11
#define DHTPIN 2
#define IN1 3
#define IN2 4
#define ENA 5

/*================ WIFI =======================*/
void print_connection_status( ) {
  Serial.print("WiFi status : \n");
  Serial.print("\t IP address : ");
  Serial.println(WiFi.localIP());
  //Serial.print("\tMAC address : ");
  //Serial.println(WiFi.macAddress());
}
void connect_wifi() {
  const char* ssid = "My ASUS";
  const char* password= "450ef7a4dffe";
  Serial.println("Connecting Wifi...");
  WiFi.begin((char*)ssid, password) ;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Attempting to connect Wifi ...");
    delay(1000);
  }
  Serial.println("Connected to local Wifi");
  print_connection_status();
}

DHT dht(DHTPIN, DHTTYPE); //instance de l'interface du capteur
int PinLed = 13; //LED témoin sur pin 13
int seuil_alerte = 28; // valeur du seuil apartir duquel l'alerte sécheresse est donnée
WiFiClient client;
IPAddress server(192,168,43,64);
unsigned port=10000;

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
  connect_wifi();
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

  if (client.connect(server, port)) {
    while(true){
      client.write("coucou");
      Serial.print(client.read());
    }
  }

  //test de lecture
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT11 sensor!"));
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
