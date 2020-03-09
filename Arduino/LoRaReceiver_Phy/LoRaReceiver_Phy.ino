#include <SPI.h>
#include <LoRa.h>
#include <ArduinoJson.h>
#include <Servo.h>

#define SS 10
#define RST 8
#define DI0 2
#define BAND 865E6  // Here you define the frequency carrier
#define PUMPPIN 5    //peristaltic pump control pin

// Parameters you can play with :
int txPower = 14; // from 0 to 20, default is 14
int spreadingFactor = 12; // from 7 to 12, default is 12
long signalBandwidth = 125E3; // 7.8E3, 10.4E3, 15.6E3, 20.8E3, 31.25E3,41.7E3,62.5E3,125E3,250E3,500e3, default is 125E3
int codingRateDenominator=5; // Numerator is 4, and denominator from 5 to 8, default is 5
int preambleLength=8; // from 2 to 20, default is 8
int seuil_alerte = 25; // valeur du seuil apartir duquel l'alerte sécheresse est donnée
Servo myservo;

void moteur_stop(){
  myservo.write(90);
}

void moteur_avancer(){
  myservo.write(0);
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  myservo.attach(PUMPPIN);
  moteur_stop();
/*
  Serial.println("LoRa Receiver");
  Serial.print("SetFrequency : ");
  Serial.print(BAND);
  Serial.println("Hz");
  Serial.print("SetSpreadingFactor : SF");
  Serial.println(spreadingFactor);
  */
  SPI.begin();
  LoRa.setPins(SS,RST,DI0);
  if (!LoRa.begin(BAND)) {
    //Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setTxPower(txPower,1);
  LoRa.setSpreadingFactor(spreadingFactor);
  LoRa.setSignalBandwidth(signalBandwidth);
  LoRa.setCodingRate4(codingRateDenominator);
  LoRa.setPreambleLength(preambleLength);
}

void loop() {
   // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    //Serial.print("Received packet: '");
    // read packet
    String s="";
    while (LoRa.available()) {
      s+=(char)LoRa.read();
    }/*
    Serial.print(s);
    // print RSSI of packet
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());*/

    // JSON
    int h,t,hic;
    char donnees[10];
    s.toCharArray(donnees, 10);
    const size_t capacity = JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(3);
    DynamicJsonDocument doc(capacity);
    JsonObject data = doc.createNestedObject("data");
    sscanf(donnees, "%03d;%02d;%02d", &h, &t, &hic);
    data["humidité"] = h;
    data["temp"] = t;
    data["index"] = hic;
    serializeJson(doc, Serial);
    Serial.println();
    if(t>=seuil_alerte){
      /*Serial.print("ALERTE TEMPERATURE ");
      Serial.print(t);
      Serial.println(F("°C"));*/
      moteur_avancer();
    }else{
      moteur_stop();
    }
    delay(5000);
  }
}
