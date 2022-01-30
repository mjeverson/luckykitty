int led = 13;

void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
}

void loop(){
  Serial.println("HELLO FROM ARDUINO!");
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(led, LOW);
  delay(1000);
}
