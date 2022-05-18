import smbus
import time
import pigpio

pi = pigpio.pi()
PUMPE_GPIO = 4

bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x49 # default address

TØR = 679
VÅD = 300

def JORDFUGTIGHED():
# Reads word (2 bytes) as int - 0 is comm byte
    rd = bus.read_word_data(i2c_address, 0)
# Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
# Ignores two least significiant bits
    data = data >> 2
    print("Data: ", data)
    time.sleep(1)
    
    ADC = data
    MÅLING = (TØR-ADC)*100/(TØR-VÅD)
    if MÅLING < 0:
        MÅLING = 0
    if MÅLING > 100:
        MÅLING = 100
    
    #print(int(MÅLING), "%")
    return MÅLING

print(int(JORDFUGTIGHED()), "%")

while True:
    fugtprocent = JORDFUGTIGHED()
    if fugtprocent < 10:
        pi.write(PUMPE_GPIO, 1)
    else:
        print("Fugtigheden er ikke under 10%")
    if fugtprocent > 60:
        pi.write(PUMPE_GPIO, 0)
    else:
        print("Fugtigheden er ikke over 60%")
        
    
    
    #PERCENT = (data*100)/1024
    #if PERCENT > 50:
     #   print(int(PERCENT), "% tør")
    #else:
     #   print(int(PERCENT), "% våd")
    #print(int(PERCENT), "%")
    # tør = 67, våd 29