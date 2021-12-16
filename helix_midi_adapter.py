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
# You can get away without setting CC control of Glide or Shape on the HX
# device. 
# Note, Octave, and Volume/Level are necessary, though.
#
# It might be possible that the Helix port name differs. In my Windows 10
# the port name is 'Line 6 Helix 1'. 
# Check carefully beforehand whether your ports are named right!
#
# You can find the ports with md.get_input_names() and md.get_output_names()
#
# If no port is specified in the function call 
# (e.g. helix_polysynth(gui_inport =""))
# Then all ports available are used. This can work sometimes, but in my case
# under Raspberry OS, the Devices were shown twice in each port-list. 
# That lead to unforeseen consequences. I really suggest to use the GUI.


# Use the adapter with a graphic user interface (GUI)
# This one takes no arguments, as everything is set in the GUI.
helix_midi_adapter_GUI()

# Start the Polysynth adapter:
# helix_polysynth()

# Start the Monosynth adapter:
# THIS ONE HAS FIXED INTERVALS FOR OSC2 AND OSC3
#helix_monosynth(0,7)
