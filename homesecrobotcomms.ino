int lmt1 = 5;
int lmt2 = 3;
int rmt1 = 6;
int rmt2 = 11;

void stp() {
analogWrite(lmt1,0);
analogWrite(lmt2,0);
analogWrite(rmt1,0);
analogWrite(rmt2,0); 
  } 


void forward(){
analogWrite(lmt1,250);
analogWrite(lmt2,0);
analogWrite(rmt1,250);
analogWrite(rmt2,0);
delay(1000);
stp();
  }


void reverse(){
analogWrite(lmt1,0);
analogWrite(lmt2,250);
analogWrite(rmt1,0);
analogWrite(rmt2,250);
delay(1000);
stp();
  }


void stpleft() {
analogWrite(lmt1,0);
analogWrite(lmt2,0);
analogWrite(rmt1,250);
analogWrite(rmt2,0); 
delay(1000);
stp();
  }

void stpright() {
analogWrite(lmt1,250);
analogWrite(lmt2,0);
analogWrite(rmt1,0);
analogWrite(rmt2,0);
delay(1000);
stp(); 
  } 


void setup() {
Serial.begin(9600);
pinMode(lmt1,OUTPUT);
pinMode(lmt2,OUTPUT);
pinMode(rmt1,OUTPUT);
pinMode(rmt2,OUTPUT);
}


void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'F') forward();
    else if (cmd == 'B') reverse();
    else if (cmd == 'L') stpleft();
    else if (cmd == 'R') stpright();
    else if (cmd == 'S') stp();
  }
}
