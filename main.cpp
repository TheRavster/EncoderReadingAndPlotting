#include <SPI.h>  // include the new SPI library:

#define MAGNETIC
// #define CAPACITIVE

#if defined(MAGNETIC) + defined(CAPACITIVE) != 1
#error "Please only define one encoder type"
#endif

#ifdef CAPACITIVE
    #define cmd 0x00
    #define read_pos 0x00
    #define set_zero 0x70
    #define reset 0x60
    #define SPI_MODE SPI_MODE0

    uint8_t data1, data2;
    uint16_t pos, pos_temp;
#endif

#ifdef MAGNETIC
    #define NOP 0x0000
    #define ERRFL 0x0001
    #define PROG 0x0003
    #define DIAAGC 0x3FFC
    #define MAG 0X3FFD
    #define ANGLEUNC 0x3FFE
    #define ANGLECOM 0x3FFF
    #define SPI_MODE SPI_MODE1

    uint16_t nop, pos_temp, error, cmd, pos, diag;
#endif

const int cs = 10;
// set up the speed, mode and endianness of each device
SPISettings settings(500000, MSBFIRST, SPI_MODE);

void setup() {
  // set the Slave Select Pins as outputs:
  pinMode (cs, OUTPUT);
  // initialize SPI:
  SPI.begin(); 
}

void loop(){
  SPI.beginTransaction(settings);
  #ifdef CAPACITIVE
    digitalWrite (cs, LOW);
    // reading only, so data sent does not matter
    data1 = SPI.transfer(cmd);
    delayMicroseconds(3);
    data2 = SPI.transfer(read_pos);
    delayMicroseconds(3);
    digitalWrite (cs, HIGH);
    SPI.endTransaction();
    pos_temp = (data1<<8)|data2;
    pos = (pos_temp & 0b0011111111111100) >> 2;
    Serial.print("Reading: ");
    Serial.println(pos);
  #endif
  #ifdef MAGNETIC
  cmd = (0b11<<14) | ANGLECOM;
  digitalWrite (cs, LOW);
  nop = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  delayNanoseconds(400);
  cmd = (0b01<<14) | ERRFL;
  digitalWrite(cs, LOW);
  pos_temp = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  delayNanoseconds(400);
  cmd = (0b11<<14) | DIAAGC;
  digitalWrite(cs, LOW);
  error = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  delayNanoseconds(400);
  cmd = (0b11<<14) | NOP;
  digitalWrite(cs, LOW);
  diag = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  SPI.endTransaction();
  Serial.print("Reading: ");
  Serial.println(pos_temp&0b11111111111111);
  #endif
  delay(10);
}
 