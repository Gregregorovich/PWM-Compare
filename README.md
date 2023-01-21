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

I have Noctua iPPC 3000 RPM fans, as I wanted black Noctua fans and the Chromax ones hadn't yet been released. I never want to run them at 100%, so if 100% duty cycle is detected it assumes there is no control yet so defaults to 10%; enough to have some airflow and also be relatively quiet - when my computer starts up it won't sound like a jet taking off anymore as they default to 100%.

Further info of the reason why I did this can be found at https://forum.level1techs.com/t/gpu-and-cpu-dependent-case-fan-control-with-kvm-using-linux-and-windows-software/191877
