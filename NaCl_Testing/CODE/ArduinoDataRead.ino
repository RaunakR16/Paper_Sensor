#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;

void setup(void)
{
  Serial.begin(9600);
  //---------------------------------------------------------------------------------------Gain Selector
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  if (!ads.begin()) {
    Serial.println("Failed to initialize ADS.");
    while (1);
  }
}

void loop(void)
{
  int16_t adc0;
  float volts0;
  float mv0;
//--------------------------------------------------- ADC Value Read
  adc0 = ads.readADC_SingleEnded(0);

//---------------------------------------------------Voltage Calculator
  volts0 = ads.computeVolts(adc0);

//---------------------------------------------------Millivolt Calculation
  mv0 = volts0 * 1000;

//---------------------------------------------------Print Statement
  // Serial.print("AIN0: "); 
  Serial.print(adc0); 
  Serial.print(",  "); 
  // Serial.print(volts0);
  // Serial.print("V");
  // Serial.print ("  ");
  Serial.println(mv0);
  // Serial.println("mV");

  delay(1);
}
