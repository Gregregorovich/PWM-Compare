from machine import *
import time, _thread, statistics

#Define CPU PWM Pin
cpu_pin = Pin(0)
#Define GPU PWM Pin
gpu_pin = Pin(4)
#Define PWM Output
fan = machine.PWM(machine.Pin(8))
#Wait for PWM Output to finish before changing duty cycle
#output_pin = Pin(12)

#Computer fan PWM frequency = 25kHz = 25000Hz
fan.freq(25000)

#Define Maximum PWM pulse length in microseconds (1/25k)
#pwm_pulse = 100000
pwm_pulse = 40

n = 40

#Define global CPU arguments; set to 0
#CPU PWM time in microseconds
cpu = 0
cpu_off = 0
cpu_output = 0
cpu_av=[0] * n
cpu_av_off=[0] * n
#Time at start of CPU PWM pulse in microseconds
cpu_t_off = 0
#Time at end of CPU PWM pulse in microseconds
cpu_t = 0

#Define global GPU arguments; set to 0
#GPU PWM time in microseconds
gpu = 0
gpu_off = 0
gpu_output = 0
gpu_av=[0] * n
gpu_av_off=[0] * n
#Time at start of GPU PWM pulse in microseconds
gpu_t_off = 0
#Time at end of GPU PWM pulse in microseconds
gpu_t = 0

def CPU_PWM_TIMER(cpu_pin,pwm_pulse):
    global cpu
    global cpu_off
    global cpu_av
    global cpu_av_off
    global cpu_output
    #global cpu_t_off
    #global cpu_t
    global wait_for_CPU
    i=0
    #Wait for CPU PWM pulse to be off
    machine.time_pulse_us(cpu_pin, 0, pwm_pulse)
    machine.time_pulse_us(cpu_pin, 1, pwm_pulse)
    
    #Measure Time PWM Pulse is on and take a median
    for x in cpu_av:
        #Record time at start of PWM pulse
        #cpu_t_off = time.ticks_us()
        
        #Time CPU PWM pulse on (else could start part-way through pulse)
        cpu_av[i] = machine.time_pulse_us(cpu_pin, 1, pwm_pulse)
        
        #Record time at end of PWM pulse
        #cpu_t = time.ticks_us()
        i += 1
    
    cpu = (statistics.median(cpu_av))
    
    i=0
    #Measure Time PWM Pulse is off and take a median
    for x in cpu_av_off:
        cpu_av_off[i] = machine.time_pulse_us(cpu_pin, 0, pwm_pulse)
        i += 1
    
    cpu_off = (statistics.median(cpu_av_off))
    
    #Anything over 50% either on or off doesn't seem to measure reliably;
    #Take the smallest value, and if it's the time the pulse is off, invert it,
    # unless it is always on, which would give "off" a value of "-2", whilst
    # "on" would give "-1"
    if cpu_off<cpu:
        if cpu_off > 0:
            cpu_output = 40-cpu_off
        else:
            cpu_output = cpu
    else:
        cpu_output = cpu
    
    #Set CPU PWM analysis as done
    wait_for_CPU = 0
    #Wait for GPU PWM analysis
    while wait_for_GPU == 1:
        time.sleep_us(1)
    
    return

def GPU_PWM_TIMER(gpu_pin,pwm_pulse):
    global gpu
    global gpu_off
    global gpu_av
    global gpu_av_off
    global gpu_output
    #global gpu_t_off
    #global gpu_t
    global wait_for_GPU
    i=0
    #Wait for GPU PWM pulse to be off
    machine.time_pulse_us(gpu_pin, 0, pwm_pulse)
    machine.time_pulse_us(gpu_pin, 1, pwm_pulse)
    
    for x in gpu_av:
        #Record time at start of PWM pulse
        #gpu_t_off = time.ticks_us()
        
        #Time GPU PWM pulse on
        gpu_av[i] = machine.time_pulse_us(gpu_pin, 1, pwm_pulse)
        
        #Record time at end of PWM pulse
        #gpu_t = time.ticks_us()
        i += 1
    
    gpu = (statistics.median(gpu_av))
    
    i=0
    #Measure Time PWM Pulse is on and take a median
    for x in gpu_av_off:
        gpu_av_off[i] = machine.time_pulse_us(gpu_pin, 0, pwm_pulse)
        i += 1
    
    gpu_off = (statistics.median(gpu_av_off))
    
    if gpu_off<gpu:
        if gpu_off > 0:
            gpu_output = 40-gpu_off
        else:
            gpu_output = gpu
    else:
        gpu_output = gpu
    
    #Set GPU PWM analysis as done
    wait_for_GPU=0
    #Wait for CPU PWM analysis
    while wait_for_CPU == 1:
        time.sleep_us(1)
    
    return

#Loop forever
while True:
#Loop once for testing
#i=0
#while i<1:

    #Wait for CPU PWM pulse to finish: Reset variables
    wait_for_CPU = 1
    wait_for_GPU = 1
    
    #Assign core1 to PWM analysis
    #_thread.start_new_thread(CPU_PWM_TIMER, (cpu_pin,pwm_pulse))
    _thread.start_new_thread(GPU_PWM_TIMER, (gpu_pin,pwm_pulse))
    
    #Use core0 for PWM analysis
    CPU_PWM_TIMER(cpu_pin,pwm_pulse)
    #GPU_PWM_TIMER(gpu_pin,pwm_pulse)
    
    #Debug
    #print("Time for PWM pulse","PWM Duty","Wait for code to finish?")
    #print(cpu_t-cpu_t_off,cpu,wait_for_CPU)
    #print(gpu_t-gpu_t_off,gpu,wait_for_CPU)
    #print("Difference between end of CPU and end of GPU code in us")
    #print(cpu_t_off-gpu_t_off,cpu_t-gpu_t)
    
    #print(cpu_av)
    #print(cpu_av_off)
    #print(cpu,cpu_off,cpu_output)
    
    #print(gpu_av)
    #print(gpu_av_off)
    #print(gpu,gpu_off,gpu_output)
    
    #print("thread exit")
    #_thread.exit()
    #return
    
    if cpu_output > gpu_output:
        fanDuty = cpu_output *1000
        #print("CPU")
    else:
        fanDuty = gpu_output *1000
        #print("GPU")
    
    if fanDuty == -2000:
        #Set PWM Duty to 10% if both CPU and GPU fan are off
        fanDuty = 4000
        #print("10%")
    elif fanDuty == -1000:
        #Set PWM Duty to 37.5% if both CPU and GPU fan are at 100%
        fanDuty = 15000
        #print("100%")
    
    #Wait for PWM duty cycle to finish pulse on and off to prevent spiky output
    #machine.time_pulse_us(output_pin, 0, pwm_pulse)
    #Set PWM Duty to the higher of CPU / GPU
    fan.duty_ns(int(fanDuty))
    #print(fanDuty,fanDuty/400)
    
    #i+=1

