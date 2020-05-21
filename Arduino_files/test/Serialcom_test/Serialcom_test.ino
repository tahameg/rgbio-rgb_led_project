//created for testing and thus is not failsafe
//--->mode
//      66 -> turn on
//      117-> fire
//      83-> get status
//      69-> turn off   
//[s_Byte][length][mode][config][data(max 8 bytes)][CRC-A][CRC-B][e_Byte]


//asynchronous: arduinonun recieve buffer ını izleyip şişip şişmediğine bakacağız
const uint8_t m_f_len = 15; //maks Frame length
const byte sb_ = 2;
const byte eb_ = 3; 

const uint8_t r_pin = 3;
const uint8_t g_pin = 5;
const uint8_t b_pin = 6;
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
  byte data[m_f_len];
  uint8_t msg_len;

  /*
  if(Serial.available()){
    Serial.readBytes(data, 11);
    Serial.write(data, 11);  
  }*/
  
  
  if(getFrame(data, msg_len)){
                Serial.println("ok!");
  }
      
}

bool getFrame(byte buf[], uint8_t &msg_len){
  bool returnVal = false;
  if(Serial.available()>1){
    byte a = Serial.read();
    if(a == sb_){
        byte msg_len = Serial.read();
        uint8_t data_len = getEndBytePos(msg_len);
        if(data_len <= (m_f_len - 2)){ //check if the end frame can be on that position
          byte data[data_len];
          Serial.readBytes(data, data_len);
          if(data[data_len-1] == eb_){

            buf = data;
            returnVal = true;
          }//Frame is succesfully recieved
        }
      }
    }
    return returnVal;
}


//How many bytes must be readed to get the end byte after reading message length which is the second byte
uint8_t getEndBytePos(uint8_t msg_len){    
      return 5+msg_len;
}
  
