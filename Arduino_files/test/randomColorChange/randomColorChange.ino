//this code is written for testing and thus, is not failsafe 
//by tahameg 193358
const uint8_t r = 3;
const uint8_t g = 5;
const uint8_t b = 6;

uint8_t r_val = 0;
uint8_t g_val = 0;
uint8_t b_val = 0;

uint8_t r_inc = 1;
uint8_t g_inc = 1;
uint8_t b_inc = 1;

unsigned long pTime1 = 0; //previous time
unsigned long pTime2 = 0; //previous time
unsigned long pTime3 = 0; //previous time
void setup() { 
  pinMode(r, OUTPUT);
  pinMode(g, OUTPUT);
  pinMode(b, OUTPUT);
}

void loop() {
  unsigned long cTime1 = millis();//current time
  unsigned long cTime2 = millis();//current time
  unsigned long cTime3 = millis();//current time
  if(cTime1 - pTime1 >= 33){
    pTime1 = cTime1;
    r_val += r_inc;
    if(r_val >= 255){
      r_inc = -1;
    }
    if(r_val <= 0){
      r_inc = 1;
    } 
   analogWrite(r, r_val); 
  }

  if(cTime2 - pTime2 >= 51){
    pTime2 = cTime2;
    g_val += g_inc;
    if(g_val >= 255){
      g_inc = -1;
    }
    if(g_val <= 0){
      g_inc = 1;
    } 
   analogWrite(g, g_val); 
  }

  if(cTime3 - pTime3 >= 69){
    pTime3 = cTime3;
    b_val += b_inc;
    if(b_val >= 255){
      b_inc = -1;
    }
    if(b_val <= 0){
      b_inc = 1;
    } 
   analogWrite(b, b_val); 
  }
}
