import mido as md

from functions import *

#############################################################################
############### - MAIN SCRIPT - #############################################
#############################################################################

# These are the parameters that need to be set on the Helix device
# to control the synth with this adapter:
    
# MIDI bypass for the 3-Note-Generator (Standard: CC 77)
# CC control for the 3NG parameters:
# - Shape  (Standard are CC80, CC85, and CC90 )
# - Octave (Standard are CC81, CC86, and CC91 )
# - Note   (Standard are CC82, CC87, and CC92 )
# - Level  (Standard are CC83, CC88, and CC93 )
# - Glide  (Standard are CC84, CC89, and CC94 )
# for each of the three Oscillators.
# 
# You can get away without setting CC control of Glide or Shape in the HX
# device. 
# Note, Octave, and Volume/Level are necessary, though.
#
# It might be possible that the Helix port name differs. In my Windows 10
# the port name is 'Line 6 Helix 1'. 
# My MIDI keyboard is listed as 'MPK mini 1'.
# Check carefully beforehand whether your ports are named right!
#
# You can find the ports with md.get_input_names() and md.get_output_names()
#
#





# Start the Polysynth adapter:
# THIS ONE ALSO CONTROLS VOLUME THROUGH VELOCITY
# THIS ONE ALSO SETS SHAPE AND GLIDE
helix_polysynth()

# Start the Monosynth adapter:
# THIS ONE HAS FIXED INTERVALS FOR OSC2 AND OSC3
# THIS ONE DOES NOT CONTROL VOLUME OR GLIDE
# helix_monosynth(0,7)
