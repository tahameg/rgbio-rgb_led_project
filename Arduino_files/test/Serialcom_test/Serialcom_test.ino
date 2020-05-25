//created for testing and thus is not failsafe
//--->mode
//      66 -> turn on
//      117-> fire
//      83-> get status
//      69-> turn off   
//[s_Byte][length][mode][config][data(max 8 bytes)][CRC-A][CRC-B][e_Byte]


//asynchronous: arduinonun recieve buffer ını izleyip şişip şişmediğine bakacağız
const uint8_t max_f_len = 15; //maks Frame length
const uint8_t min_f_len = 8; //min Frame length
const byte sb_ = 2;
const byte eb_ = 3; 

const uint8_t r_pin = 3;
const uint8_t g_pin = 5;
const uint8_t b_pin = 10;
bool isReady;


void setup() {
  isReady = false;
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(r_pin, OUTPUT);
  pinMode(g_pin, OUTPUT);
  pinMode(b_pin, OUTPUT);
}

void loop() {
  byte data[max_f_len];

  /*
  if(Serial.available()){
    Serial.readBytes(data, 11);
    Serial.write(data, 11);  
  }*/
  
  int data_len = getFrame(data);
  if(data_len > 0){
     setmode(data, data_len);
  }    
}

int getFrame(byte *buf){
  int returnVal = -1;
  if(Serial.available()>= min_f_len){ // wait for multiple bytes to arrive 
    byte a = Serial.read();
    if(a == sb_ && Serial.available()){
        byte msg_len_l = Serial.read();
        uint8_t data_len = getEndBytePos(msg_len_l);
        if(data_len <= (max_f_len - 2)){ //check if the end frame can be on that position
          byte data[data_len];
          Serial.readBytes(data, data_len);
          if(data[data_len-1] == eb_){
            for(int i=0;i<data_len;i++){
              buf[i] = data[i];
            }
            returnVal = int(data_len);
          }//Frame is succesfully recieved
        }
      }
    }
    return returnVal;
}


//How many bytes must be readed to get the end byte after reading message length which is the second byte
uint8_t getEndBytePos(uint8_t msg_len){//also length of the obtained array    
      return 5+msg_len;
}

void setmode(byte *data, int data_len){
  switch(int(data[0])){
    case 66:
      isReady = true;
      setvalue(200, 200, 200);
    break;
    case 69:
      isReady = false;
      setvalue(0, 0, 0);
    break;
    case 117:
      if(isReady){
        setvalue( uint8_t(data[2]), uint8_t(data[3]), uint8_t(data[4]));
      }else{
        Serial.println("ups!");
      }
    break;
  }
}

void setvalue(uint8_t r, uint8_t g, uint8_t b){
      analogWrite(r_pin, r);
      analogWrite(g_pin, g);
      analogWrite(b_pin, b);
}

  
