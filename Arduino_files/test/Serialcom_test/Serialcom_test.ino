//created for testing and thus is not failsafe

//asynchronous: arduinonun recieve buffer ını izleyip şişip şişmediğine bakacağız
const byte sb_ = 2;
const byte eb_ = 3; 
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  byte rgb[3];
  if(getFrame(rgb))
  {
      Serial.println(String(rgb[0]));
  }
}

bool getFrame(byte buf[]){
  if(Serial.available()){
    byte a = Serial.read();
    if(a == sb_){
      byte data[7];
      Serial.readBytes(data, 7);
      if(data[6] == eb_){
        buf[0]=data[1];
        buf[1]=data[2];
        buf[2]=data[3];
        return true;
      }
      else
      {
        return false;
      }
    }
    else
    {
      return false;
    }
  }
}

