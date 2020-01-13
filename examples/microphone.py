import analogio, time
import pimoroni_physical_feather_pins

mic = analogio.AnalogIn(pimoroni_physical_feather_pins.pin8())
samples = list(range(20))
clap_time = 0
half_second = 500000000 # measured in nanoseconds

clap_threshold = 1000 # the higher the value the less sensitive

def double_clap_function(): # what you want to do when there is a double clap
    print("Double Clap!")

while True: # detection start
    for i in range(20): # take 20 samples of how loud it is
        samples[i] = abs(mic.value - 32768)
    
    if (sum(samples)/20) > clap_threshold: # if clap found

        if not clap_time + half_second >= time.monotonic_ns(): # if another clap hasn't happened in the last half second
            #print("Clap at {}".format(time.monotonic_ns()))
            clap_time = time.monotonic_ns() # update the last time a clap happened
            time.sleep(0.1)
        else: # if another clap has happened in the last half second
            double_clap_function()
            time.sleep(0.1)