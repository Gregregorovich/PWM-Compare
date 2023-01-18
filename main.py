from machine import *
import time, _thread

#Define CPU PWM Pin
cpu_pin = Pin(0)
#Define GPU PWM Pin
gpu_pin = Pin(4)
#Define PWM Output
fan = machine.PWM(machine.Pin(8))
#Computer fan PWM frequency = 25kHz = 25000Hz
fan.freq(25000)

#Define Maximum PWM pulse length in microseconds (1/25k)
#pwm_pulse = 100000
pwm_pulse = 40


#Define global CPU arguments; set to 0
#CPU PWM time in microseconds
cpu = 0
#Time at start of CPU PWM pulse in microseconds
cpuoff = 0
#Time at end of CPU PWM pulse in microseconds
cpu_t = 0

#Define global GPU arguments; set to 0
#GPU PWM time in microseconds
gpu = 0
#Time at start of GPU PWM pulse in microseconds
gpuoff = 0
#Time at end of GPU PWM pulse in microseconds
gpu_t = 0

def CPU_PWM_TIMER(cpu_pin,pwm_pulse):
    global cpu
    #global cpuoff
    #global cpu_t
    global wait_for_CPU
    
    #Wait for CPU PWM pulse to be off
    machine.time_pulse_us(cpu_pin, 0, pwm_pulse)
    
    #Record time at start of PWM pulse
    #cpuoff = time.ticks_us()
    
    #Time CPU PWM pulse on (else could start part-way through pulse)
    cpu = machine.time_pulse_us(cpu_pin, 1, pwm_pulse)
    
    #Record time at end of PWM pulse
    #cpu_t = time.ticks_us()
    
    #Set CPU PWM analysis as done
    wait_for_CPU = 0
    #Wait for GPU PWM analysis
    while wait_for_GPU == 1:
        time.sleep_us(1)
    
    return

def GPU_PWM_TIMER(gpu_pin,pwm_pulse):
    global gpu
    #global gpuoff
    #global gpu_t
    global wait_for_GPU
    
    #Wait for GPU PWM pulse to be off
    machine.time_pulse_us(gpu_pin, 0, pwm_pulse)
    
    #Record time at start of PWM pulse
    #gpuoff = time.ticks_us()
    
    #Time GPU PWM pulse on
    gpu = machine.time_pulse_us(gpu_pin, 1, pwm_pulse)
    
    #Record time at end of PWM pulse
    gpu_t = time.ticks_us()
    #print(gpu_t,"GPU",gpu," ")
    
    #Set GPU PWM analysis as done
    wait_for_GPU=0
    #Wait for CPU PWM analysis
    while wait_for_CPU == 1:
        time.sleep_us(1)
    
    return

#Loop forever
while True:
    
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
    #print(cpu_t-cpuoff,cpu,wait_for_CPU)
    #print(gpu_t-gpuoff,gpu,wait_for_CPU)
    #print("Difference between end of CPU and end of GPU code in us"
    #print(cpu_t-gpu_t)
    
    #print("thread exit")
    #_thread.exit()
    #return
    
    if cpu > gpu:
        fanDuty = cpu *1000
        #print("CPU")
    else:
        fanDuty = gpu *1000
        #print("GPU")
    
    if fanDuty == -2000:
        #Set PWM Duty to 10% if both CPU and GPU fan are off
        fanDuty = 4000
        #print("10%")
    elif fanDuty == -1000:
        #Set PWM Duty to 100% if both CPU and GPU fan are at 100%
        fanDuty = 40000
        #print("100%")
    
    #Set PWM Duty to the higher of CPU / GPU
    fan.duty_ns(fanDuty)
    #print(fanDuty)
