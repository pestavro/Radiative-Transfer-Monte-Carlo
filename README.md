*************************************************************************************
 Radiative Transfer Monte Carlo Simulation Project - Petros Stavroulakis, April 2021 
*************************************************************************************

The program was written in Python and requires the matplotlib library to run. The only inputs requested from the user on execute are the number of photons and the maximum number of scatterings in the medium. On completion, two figures should be produced: an interactive (zoom + rotate) 3d line plot depicting all the scattered photons' positions and a graph with the total distance travelled per photon.

The simulation runs in the high-density regime by default. In order to switch between the high and low-density regimes, it is necessary to change what the density() function returns. Simply comment the current return line and un-comment the line that returns a constant value for the density (8.96e16) to switch to the low-density regime.

Absorption is also turned off by default. To turn it on, simply change the value of the absorption flag at the top from 0 to 1.

There are various prints scattered throughout the code, in order to test its functionality. I have left some of them in, but they are all commented by default. If you would like to see some useful information printed in the terminal after the simulation has finished executing, you are welcome to un-comment them.
