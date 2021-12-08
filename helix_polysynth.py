import mido as md

#############################################################################
############### - CLASSES - #################################################
#############################################################################

class HelixOscillator:
    def __init__(self, cc_shape, cc_oct, cc_note, cc_level, cc_glide, 
                 note=0, octave=0, volume=0, glide=0, shape=0, midi_note=0,
                 channel=0):
        self.cc_note    = cc_note
        self.cc_oct     = cc_oct
        self.cc_shape   = cc_shape
        self.cc_level   = cc_level
        self.cc_glide   = cc_glide
        self.note       = note
        self.octave     = octave
        self.volume     = volume
        self.glide      = glide
        self.shape      = shape
        self.midi_note  = midi_note
        self.channel    = channel

        
    def set_note(self, input_note):
        """
        Sets the note and octave of the oscillator.

        Parameters
        ----------
        midi_note : int
            MIDI note VALUE (0,...,127).

        Returns
        -------
        None.

        """
        self.octave   = input_note//12
        self.note     = input_note - self.octave*12
        
    def update_oscillator(self, msg):
        """
        Updates the Oscillator object with the content of a message.

        Parameters
        ----------
        msg : midi MIDI message
            (Preferably) a MIDI NOTE ON message.

        Returns
        -------
        None.

        """
        if msg.type == 'note_on':
            self.octave     = msg.note // 12
            self.note       = msg.note - self.octave * 12
            self.volume     = max(20, msg.velocity)
            self.midi_note  = msg.note
        else:
            print("Message is not NOTE ON. Doing nothing.")
              
    def gen_message(self):
        """
        Generate a list of MIDI messages that represent the status of the
        oscillator

        Returns
        -------
        list
            MIDO MIDI messages that are to be sent to the Helix.

        """
        olist = [0,16,32,48,64,80,96,112,127]
        nlist = [0,12,24,35,47,59,70,81,93,104,116,127]
        
        
        msg_shp = md.Message('control_change', 
                                   channel = self.channel, 
                                   control = self.cc_shape,
                                   value   = self.shape
                                   )
        msg_oct = md.Message('control_change', 
                                   channel = self.channel, 
                                   control = self.cc_oct,
                                   value   = olist[self.octave]
                                   )    
        msg_note = md.Message('control_change', 
                                   channel = self.channel, 
                                   control = self.cc_note,
                                   value   = nlist[self.note]
                                   )
        msg_lev = md.Message('control_change', 
                                   channel = self.channel, 
                                   control = self.cc_level,
                                   value   = self.volume
                                   )
        msg_glide = md.Message('control_change', 
                                   channel = self.channel, 
                                   control = self.cc_glide,
                                   value   = self.glide
                                   )                       
        return [msg_shp, msg_oct, msg_note, msg_lev, msg_glide]
      
    def off(self):
        """
        Turns the oscillator off.

        Returns
        -------
        None.

        """
        self.volume = 0
        
    def set_wave(self, shape="saw_up"):
        """
        Set the wave shape of oscillator.

        Parameters
        ----------
        shape : STRING, optional
            Keyword of the desired waveform. The default is "sine".

        Returns
        -------
        None.

        """
        if shape == "saw_up":
            self.shape = 0

        elif shape == "saw_down":
            self.shape = 60
        elif shape == "triangle":
            self.shape = 90
        elif shape == "sine":
            self.shape = 126
        elif shape == "square":
            self.shape = 127
        else:
            self.shape = 0
            print("Shape: "+shape+" is not a valid shape. Revert to sine...\n")


#############################################################################
############### - FUNCTIONS - ###############################################
#############################################################################

def turn_3ng_on(chn=0, cc=77):
    """
    Turns the 3NG on, i.e. a message is generated that can be send to the
    Helix to un-bypass the corresponding 3NG block.

    Parameters
    ----------
    chn : int, optional
        MIDI channel that the Helix responds to.
    cc : int, optional
        The control change (CC) parameter the CC bypass of the 3NG is set to. 
        The default is 77.

    Returns
    -------
    msg : mido MIDI message
        Message object to be send via outport.send(msg)

    """
    msg = md.Message('control_change', channel=chn, control=cc, value=127)
    return msg

def turn_3ng_off(chn=0, cc=77):
    """
    Turns the 3NG off, i.e. a message is generated that can be send to the
    Helix to bypass the corresponding 3NG block.

    Parameters
    ----------
    chn : int, optional
        MIDI channel that the Helix responds to.
    cc : int, optional
        The control change (CC) parameter the CC bypass of the 3NG is set to. 
        The default is 77.

    Returns
    -------
    msg : mido MIDI message
        Message object to be send via outport.send(msg)

    """
    msg = md.Message('control_change', channel=chn, control=cc, value=0)
    return msg

def helix_midi_adapter(midi_channel = 0,
                    ccshapes        = [80,85,90],
                    ccocts          = [81,86,91],
                    ccnotes         = [82,87,92],
                    cclevels        = [83,88,93],
                    ccglides        = [84,89,94],
                    cc_bypass       = 77,
                    keyboard        = 'MPK mini 1',
                    helix           = 'Line 6 Helix 1',
                    cc_off          = 18,
                    shape           = "saw_up"
                    ):
    """
    This function provides the main loop of the Helix-MIDI adapter.
    Running this function couples the MIDI-NOTE input of the keyboard.
    These CC values are sent to the Helix to control the
    3-Note-Generator block which then acts as polyphonic synth.

    Parameters
    ----------
    midi_channel : int, optional
        Input MIDI channel of the Helix. Can be set in the global settings
        of the Helix Floor / LT / Stomp / Stomp XL / Effects device. 
        The default is 0.
    ccshapes : list of int, optional
        Control Change (CC) parameter assigned to the three oscillator values
        for "OSC shape". The default is [80,85,90].
    ccocts : list of int, optional
        Control Change (CC) parameter assigned to the three oscillator values
        for "OSC octave". The default is [81,86,91].
    ccnotes : list of int, optional
        Control Change (CC) parameter assigned to the three oscillator values
        for "OSC note". The default is [82,87,92].
    cclevels : list of int, optional
        Control Change (CC) parameter assigned to the three oscillator values
        for "OSC volume". The default is [83,88,93].
    ccglides : list of int, optional
        Control Change (CC) parameter assigned to the three oscillator values
        for "OSC glide". The default is [84,89,94].
    cc_bypass : int, optional
        Control Change (CC) parameter set for the MIDI bypass of the
        3-Note-Generator block. The default is 77.
    keyboard : string, optional
        Internal name of the MIDI keyboard device as read from mido input 
        device list.. The default is 'MPK mini 1'.
    helix : string, optional
        Internal name of the Helix device as read from mido input device list.
        The default is 'Line 6 Helix 1'.
    cc_off : int, optional
        Control Change (CC) value that ends the synthesizer script.
        The default is '18'.


    Returns
    -------
    None.

    """
    
    
    print(" Starting the adapter... \n Opening ports...")
    inport      = md.open_input(keyboard)
    outport     = md.open_output(helix)
    print(" DONE.")
      
    # Initialize the oscillator objects
    oscillators = []
    for o in [0,1,2]:
        oscillators.append(HelixOscillator(ccshapes[o], 
                                      ccocts[o], 
                                      ccnotes[o], 
                                      cclevels[o], 
                                      ccglides[o],
                                      channel = midi_channel
                                      )
                           )
    # Send the initial status of the oscillators to the Helix device.
    # This way, basically all sliders on the 3NG are set to zero.    
    for o in oscillators:
        for m in o.gen_message():
            outport.send(m)
    
    # Turn on the 3NG    
    outport.send(turn_3ng_on())
    
    # Initialze the main loop.
    print(" Starting main loop of the adapter. Fingers crossed!")
    rotation = -1
    loop = True
    while loop: 
        # Wait for MIDI input through the inport
        msg = inport.receive()
        if msg.type=="note_on":
            # Update the oscillator's state with the information from the
            # message that was received.
            oscillators[rotation].update_oscillator(msg)
            # Update the rotation parameter to choose the next oscillator
            # to simulate a polyphonic synth.
            rotation = (rotation + 1)%3

        elif msg.type=="note_off":
            # Switch the oscillator off if a note is released.
            for i in [0,1,2]:
                if msg.note == oscillators[i].midi_note:
                    oscillators[i].off()
            
        elif msg.type=="control_change":
            # Use a CC value as an "emergency exit" out of the main loop.
            if msg.control == cc_off: 
                loop = False
                print(" CC value {} received. Stopping the adapter.".format(cc_off))
                outport.send(turn_3ng_off())
                
        # Send the information for ALL oscillators to the Helix device.
        for o in oscillators:
            for m in o.gen_message():
                outport.send(m)
                
                
    print("... Shutting adapter down. Goodbye.")
    inport.close()
    outport.close()
    
    return None

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
# You can get away without setting CC control of Glide or Shape. Note, Octave,
# and Volume/Level are necessity, though.
#
# It might be possible that the Helix port name differs. In my Windows 10
# the port name is 'Line 6 Helix 1'. 
# My MIDI keyboard is listed as 'MPK mini 1'.
# Check carefully beforehand whether your ports are named right!
#
# You can find the ports with md.get_input_names() and md.get_output_names()
#
#


 'MPK mini 1',
helix           = 'Line 6 Helix 1'



# Start the Adapter.
helix_midi_adapter()
