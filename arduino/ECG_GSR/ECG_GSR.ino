
// 
// Arduino - eHealth Platform
// Timer sketch that sample every 4 ms
// The serial output is: millis, ECG, GSR
//
// millis: Arduino millis() function
// ECG: ECG value from eHealth board (Analog 0)
// GSR: GSR value from eHealth board )(Analog 2)
//

#define set_bit(sfr, bit) (sfr |= (1 << bit))
#define clear_bit(sfr, bit) (sfr &= ~(1 << bit))

void setup() 
{
  // Setup the serial port
  Serial.begin(115200);  
  // Setup timer
  setup_timer();
}

void loop() 
{
  // Loop function (not used)  
}

void setup_timer() 
{
  // Set the prescaler to 1024 -> CSS2:0 = b110
  clear_bit (TCCR2B, CS20);
  set_bit (TCCR2B, CS21);
  set_bit (TCCR2B, CS22);
  
  // CTC timer operation
  // Compare Output Mode = Toggle OC2A on Compare Match for non-PWM mode
  // Set COM2A1:0 = b01 
  set_bit (TCCR2A, COM2A0);
  clear_bit (TCCR2A, COM2A1);
  clear_bit (TCCR2A, COM2B0);
  clear_bit (TCCR2A, COM2B1);
  
  // Waveform Generation Mode = CTC
  // Set WGM22:0 = 2 = b010
  clear_bit (TCCR2A, WGM20);  
  set_bit (TCCR2A, WGM21);
  clear_bit (TCCR2B, WGM22);

  // Set the counter limit
  OCR2A = 249;    
  
  // Turn on timer2
  set_bit (TIMSK2, OCIE2A);
}

ISR(TIMER2_COMPA_vect)
{
  Serial.print(millis());
  Serial.print(",");
  Serial.print(analogRead(A0));
  Serial.print(",");
  Serial.println(analogRead(A2));
}
    


