#Below is a small macro I wrote to get the pretilt zero for the lamellae, to be used in setting up of tilt-series. In SerialEM, you can go to Scripts> Edit 4 or 7 or whatever and then copy-paste this script, to be saved into your Settings file. The macro takes a series of Trial images at different tilt angles and output their mean counts in the log. The angle at which you get the highest mean count is the Pre-Tilt zero. It takes roughly 30 seconds to run & dose is expended on a sacrificial Trial area. This pre-tilt zero, as you know, depends on the angle of milling, any possible surface deformations, the angular offset of the milling direction to the tilt-axis, etc.
#In this repository is a screenshot (pretilt_zero.png) of an example log, from which the PreTilt zero angle would be 3 degrees, quite different from the milling angle.

start_angle = -1 * 15
end_angle = 15
step = 3
n_tilts = $end_angle - $start_angle
n_tilts = $n_tilts / $step
echo $n_tilts
tilt_angle = $start_angle
Loop $n_tilts
 TiltTo $tilt_angle
 Trial
 echo $tilt_angle
 ElectronStats
 tilt_angle = $tilt_angle + $step
EndLoop