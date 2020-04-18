 Walking Pattern Comparision with Walking Sensor
=============================================
# Project Name: Walking Pattern Comparision
  This is to compute the sensor position according .h5 file
  This tool could remove noise signal in walking track sensor and then using accelerometer and gyroscope to compute x,y,z coordinate position

# Oscillatory motion tracking
## Data Source:  Accelerometer and Gyroscope measurements from sensors
## Data Processing:
* Process data through AHRS algorithm (calculate orientation) -> R
* Calculate 'tilt-compensated' accelerometer -> tcAcc
* Calculate linear acceleration in Earth frame (subtracting gravity) -> linAcc
* Calculate linear velocity (integrate acceleration) -> linVel
* High-pass filter linear velocity to remove drift -> linVelHP
* Calculate linear position (integrate velocity) -> linPos
* High-pass filter linear position to remove drift -> linPosHP

# Reference:
For more information see:
   https://x-io.co.uk/oscillatory-motion-tracking-with-x-imu/

<div align="center">
<img src="https://raw.github.com/xioTechnologies/Oscillatory-Motion-Tracking-With-x-IMU/master/Video%20Screenshot.png"/>
</div>


