# PWM-Compare
Compares two different computer fan PWM duty cycles and outputs the highest duty cycle

N.B. Dependent on the statistics micropython library found at https://github.com/rcolistete/MicroPython_Statistics

The aim of this is to compare fan speeds for case fans as determined by CPU and GPU temperature and still allow for monitoring of each fan via their tach pin (IE not using a PWM splitter).

This would also be ideal for a (especially single-loop) watercooling system with both CPU and GPU in the loop.

This has been designed for a dual core microcontroller like the Raspberry Pi Pico, but with minimal tweaking it could be adjusted to a single core microcontroller.

Designed-for scenario:
* I have 6 fan headers on my motherboard, and 6 on my Corsair Commander Pro.
* I have 6 case fans and a mid-case mounted radiator for my CPU with 4 attached fans.

Corsair iCUE allows me to set a fan curve based on GPU temperature.
My motherboard's BIOS/UEFI allows me to set a fan curve based on CPU temperature.

I have Noctua iPPC 3000 RPM fans, as I wanted black Noctua fans and the Chromax ones hadn't yet been released. I never want to run them at 100%, so if 100% duty cycle is detected it assumes there is no control yet so defaults to 37.5%; enough to have plenty of airflow and also be relatively quiet - when my computer starts up it won't sound like a jet taking off anymore as they default to 100%.

Further info of the reason why I did this can be found at https://forum.level1techs.com/t/gpu-and-cpu-dependent-case-fan-control-with-kvm-using-linux-and-windows-software/191877


Stripboard layout I used:

![FanPWM_2 1_Pico](https://user-images.githubusercontent.com/5290059/213879008-fce5c49d-b606-46e9-b850-fb750a245e39.png)


Due to issues with getting a reliable PWM value when the pulse was either high or low for over 50% duty cycle, I experimented with using the ADC (GP26/GP27) as a voltmeter which required using a potential divider to step the voltage down from 5V, but that ended up being completely unreliable, so the risistors are ignorable. Update: a capacitor would probably smooth the voltage and make it more reliable, but it works as it is so I'm not going to further experiment at least for now. Same goes for the wire soldered between the PWM output and GP12 as I thought I needed to wait for the PWM duty cycle to finish before updating the duty cycle as iCUE scales the RPM monitor graph to the lowest and highest in the stated timeframe, rather than setting the bottom of the graph to 0, so I didn't initially realise that the spiky graph was a fluctuation of a couple RPM rather than what it looked like, which was a couple hundred.

![PXL_20230121_153830263 MP](https://user-images.githubusercontent.com/5290059/213879670-424c8fed-93a7-4e2c-ab74-2d2fadaf49bb.jpg)

![PXL_20230121_153856360 MP](https://user-images.githubusercontent.com/5290059/213879679-2624436d-10ff-4c20-bf16-e1afd128f96f.jpg)
