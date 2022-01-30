int led = LED_BUILTIN;
int state = 0;

void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
}

void loop(){
//  if (Serial.available() > 0){
//    Serial.print("STATE: ");
//    Serial.print(state);
    
    if (state == 0) {
      digitalWrite(led, HIGH);
      state = 1;
    } else {
      digitalWrite(led, LOW);
      state = 0;
    }

    if (Serial.available() > 0){
      byte data = Serial.read();

      if (data == 0x00){
        Serial.println("GOT EXPECTED!");
      } else {
        Serial.write(data); 
      }
    }

    delay(1000);
    
//    byte data = Serial.readStringUntil('\n');
//    Serial.print("You sent me: ");
//    Serial.println(data);
//  }
}
