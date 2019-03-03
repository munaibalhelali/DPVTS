#include <SoftwareSerial.h>
SoftwareSerial mySerial(D6, D7); // RX, TX
int incomingByte;
boolean barricadeState=false;
int irStatus=1;


const int oneCycle= 200;
const int cw= 0;
const int ccw= 1;


// defines pins numbers
const int stepPin = D1; 
const int dirPin = D0; 
const int irSensor=D2;

void setup() {
Serial.begin(115200);
mySerial.begin(115200);
// Sets the two pins as Outputs/INPUTS
pinMode(stepPin,OUTPUT); 
pinMode(dirPin,OUTPUT);
pinMode(irSensor,INPUT);
delay(20);
}

String getPayload(String data){
  int lastCommaIndex = data.lastIndexOf(',');
  data.remove(lastCommaIndex );
  lastCommaIndex = data.lastIndexOf(',');
  data.remove(lastCommaIndex );
  lastCommaIndex = data.lastIndexOf(',');
  String payload = data.substring(lastCommaIndex+1); 
  return payload ;
}

void loop() 
{
  //Serial.println(digitalRead(irSensor));
 
  if(mySerial.available()>0)
  {
    irStatus=digitalRead(irSensor);
    String incomingByte = mySerial.readString();
    
    if(incomingByte.startsWith("+RCV"))
    {
      String payload = getPayload(incomingByte);
      if (payload.equals("open"))
      {
        if (barricadeState == false )
        {
          motorControl(0.5*oneCycle,cw);
        }
      }else if (payload.equals("close"))
      { 
        if(barricadeState == true && irStatus)
        {
          motorControl(0.5*oneCycle,ccw); 
        }else if(!irStatus){
          payload="ERROR0";
        }
      }
      Serial.println(payload);
      mySerial.print("AT+SEND=2," + String(payload.length()) + "," + payload + "\r\n");
    }
  }
}

void motorControl(int steps, int dir){ // dir=0 turn CW
                                       // dir=1 turn CCW
  if(dir == 0){
    digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
    barricadeState=true;
  }else if(dir==1){
    digitalWrite(dirPin,LOW); // Enables the motor to move in a particular direction
    barricadeState=false;
  }
  

  for(int x = 0; x < steps; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(500); 
  }
}

