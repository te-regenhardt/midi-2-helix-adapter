import mido as md
import tkinter as tk
from tkinter import ttk
import threading
from PIL import ImageTk, Image



#############################################################################
############### - CLASSES - #################################################
#############################################################################

class HelixOscillator:
    def __init__(self, cc_shape, cc_oct, cc_note, cc_level, cc_glide, 
                 note=0, octave=0, volume=0, glide=0, shape=0, midi_note=0,
                 channel=0, monopoly="poly"):
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
        self.monopoly   = monopoly

        
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
              
    def gen_message(self, monopoly="poly"):
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
        

        # msg_shp = md.Message('control_change', 
        #                                channel = self.channel, 
        #                                control = self.cc_shape,
        #                                value   = self.shape
        #                                )
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

        # msg_glide = md.Message('control_change', 
        #                                channel = self.channel, 
        #                                control = self.cc_glide,
        #                                value   = self.glide
        #                                )    
        if monopoly == "poly":       
            return [msg_oct, msg_note, msg_lev]            
            #return [msg_shp, msg_oct, msg_note, msg_lev, msg_glide]
        if monopoly == "mono":
            return [msg_oct, msg_note, msg_lev]
      
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


def activate_adapter(inport, outport, mode, chn, 
                     shp, i1, i2, 
                     ccbyp, ccoff,
                     ccshp, cco, ccnot, cclev, ccgli, gli):
    if mode == "poly":
        helix_polysynth(    midi_channel    = chn,
                            ccshapes        = ccshp,
                            ccocts          = cco,
                            ccnotes         = ccnot,
                            cclevels        = cclev,
                            ccglides        = ccgli,
                            cc_bypass       = ccbyp,
                            cc_off          = ccoff,
                            shape           = shp,
                            GUI             = True,
                            gui_inport      = inport,
                            gui_outport     = outport
                        )
    elif mode == "mono":
        helix_monosynth(    interval1       = i1,
                            interval2       = i2,
                            midi_channel    = chn,
                            ccshapes        = ccshp,
                            ccocts          = cco,
                            ccnotes         = ccnot,
                            cclevels        = cclev,
                            ccglides        = ccgli,
                            cc_bypass       = ccbyp,
                            cc_off          = ccoff,
                            shape           = shp,
                            GUI             = True,
                            gui_inport      = inport,
                            gui_outport     = outport,
                            glide           = gli
                        )
    else:
        print("ERROR: No synth mode set. Doing nothing.")
    
# def deactivate_adapter():
#     return


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

def send_all(msg, portlist):
    """
    This function sends a midi message to all ports in a portlist.

    Parameters
    ----------
    msg : mido MIDI message.
        A MIDI message of any kind (CC, NOTE ON, etc.).
    portlist : List of MIDI ports.
        List of opened (out-) ports.

    Returns
    -------
    None.

    """
    for p in portlist:
        p.send(msg)
        
def wave_to_cc(shape):
    """
    Translates a waveshape string into the CC parameter VALUE that corresponds
    to the waveshape on the Helix device.

    Parameters
    ----------
    shape : string
        Name of the waveshape.

    Returns
    -------
    wave : int
        CC parameter VALUE that corresponds to shape. Defaults to "saw_up".

    """
    if shape == "saw_up":
        wave = 0  
    elif shape == "saw_down":
        wave = 60
    elif shape == "triangle":
        wave = 90
    elif shape == "sine":
        wave = 126
    elif shape == "square":
        wave = 127
    else:
        wave = 0      
    return wave

def helix_polysynth(midi_channel = 0,
                    ccshapes        = [80,85,90],
                    ccocts          = [81,86,91],
                    ccnotes         = [82,87,92],
                    cclevels        = [83,88,93],
                    ccglides        = [84,89,94],
                    cc_bypass       = 77,
                    cc_off          = 18,
                    shape           = "saw_up",
                    GUI             = False,
                    gui_inport      = "",
                    gui_outport     = ""
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
    cc_off : int, optional
        Control Change (CC) value that ends the synthesizer script.
        The default is '18'.
    shape : TYPE, optional
        DESCRIPTION. The default is "saw_up".
    GUI : bool, optional
        Whether the GUI was used to call the adapter. The default is False.
    gui_inport : string, optional
        Name of the inport to be used. The default is "".
    gui_outport : string, optional
        Name of the outport to be used. The default is "".

    Returns
    -------
    None.

    """
      
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
        
    # Opening the ports.
    if GUI == True:
        print(" Starting the polysynth adapter... \n Opening selected ports...")
        inportlist  = [gui_inport]
        outportlist = [gui_outport]
        print(" Opening the following ports:")
        print([gui_inport, gui_outport])
    else:
        print(" Starting the polysynth adapter...")
        if gui_inport == "":
            print(" No inport set. Opening ALL inports.")
            inportlist = md.get_input_names()
        else:
            print(" Opening inport {}.".format(gui_inport))
            inportlist = [gui_inport]
        if gui_outport == "":
            print(" No outport set. Opening ALL outports.")
            outportlist = md.get_output_names()
        else:
            print(" Opening outport {}".format(gui_outport))
            outportlist = [gui_outport]
            
    open_iports = []
    open_oports = []
    for i in inportlist:
        open_iports.append(md.open_input(i))
    for o in outportlist:
        open_oports.append(md.open_output(o))
    print(" DONE.")   
    
    
    # Send the initial status of the oscillators to the Helix device.
    # This way, basically all sliders on the 3NG are set to zero.    
    for o in oscillators:
        for m in o.gen_message():
            send_all(m, open_oports)
            
    # Send the waveshape info from the GUI to the Helix device. 
    for i in [0,1,2]:
        if GUI == True:
            msg_w = md.Message('control_change', 
                                            channel = midi_channel, 
                                            control = ccshapes[i],
                                            value   = wave_to_cc(shape)
                                            )  
            send_all(msg_w, open_oports)
    
    # Turn on the 3NG    
    send_all(turn_3ng_on(midi_channel, cc_bypass), open_oports)


    # Initialze the main loop.
    print(" Starting main loop of the adapter. Fingers crossed!")
    keycounter = 0
    rotation = -1
    loop = True
    while loop: 
        if keycounter > 7:
            loop = False
            send_all(turn_3ng_off(midi_channel, cc_bypass), open_oports)
            print("More than 7 Keys pressed. Aborting adapter main loop.")
        for port in open_iports:
            msg = port.poll()
            if msg is not None:
                # Wait for MIDI input through the inport
                if msg.type=="note_on":
                    # Update the oscillator's state with the information from the
                    # message that was received.
                    print("NOTE ON received for note {}.".format(msg.note))
                    oscillators[rotation].update_oscillator(msg)
                    # Update the rotation parameter to choose the next oscillator
                    # to simulate a polyphonic synth.
                    rotation = (rotation + 1)%3
                    # Increase the key counter by one.
                    keycounter +=1
        
                elif msg.type=="note_off":
                    # Switch the oscillator off if a note is released.
                    print("NOTE OFF received for note {}.".format(msg.note))
                    # Decrease the key counter by one.
                    keycounter -=1
                    for i in [0,1,2]:
                        if msg.note == oscillators[i].midi_note:
                            oscillators[i].off()
                    
                elif msg.type=="control_change":
                    # Use a CC value as an "emergency exit" out of the main loop.
                    if msg.control == cc_off: 
                        loop = False
                        send_all(turn_3ng_off(midi_channel, cc_bypass), open_oports)
                        
                # Send the information for ALL oscillators to the Helix device.
                for o in oscillators:
                    for m in o.gen_message():
                        send_all(m, open_oports)
                        
                
    print("... Shutting adapter down. Goodbye.")
    for i in open_iports:
        i.close()
    for o in open_oports:
        o.close()
    print(" ..::: Ports are closed. :::..")
    
    
def helix_monosynth(interval1 = 0,
                    interval2 = 0,
                    midi_channel = 0,
                    ccshapes        = [80,85,90],
                    ccocts          = [81,86,91],
                    ccnotes         = [82,87,92],
                    cclevels        = [83,88,93],
                    ccglides        = [84,89,94],
                    cc_bypass       = 77,
                    cc_off          = 18,
                    shape           = "saw_up",
                    GUI             = False,
                    gui_inport      = "",
                    gui_outport     = "",
                    glide           = 0
                    ):
    """
    

    Parameters
    ----------
    interval1 : int, optional
        Interval for OSC2. The default is 0.
    interval2 : int, optional
        Interval for OSC3. The default is 0.
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
    cc_off : int, optional
        Control Change (CC) value that ends the synthesizer script.
        The default is '18'.
    shape : TYPE, optional
        DESCRIPTION. The default is "saw_up".
    GUI : bool, optional
        Whether the GUI was used to call the adapter. The default is False.
    gui_inport : string, optional
        Name of the inport to be used. The default is "".
    gui_outport : string, optional
        Name of the outport to be used. The default is "".
    glide : int, optional
        Glide value to be used. The default is 0.

    Returns
    -------
    None.

    """
    
    # Initialize the oscillator objects
    oscillators = []
    for o in [0,1,2]:
        oscillators.append(HelixOscillator(ccshapes[o], 
                                      ccocts[o], 
                                      ccnotes[o], 
                                      cclevels[o], 
                                      ccglides[o],
                                      channel  = midi_channel,
                                      monopoly = "mono"
                                      )
                           )
        
    # Opening the ports.
    if GUI == True:
        print(" Starting the monosynth adapter... \n Opening selected ports...")
        inportlist  = [gui_inport]
        outportlist = [gui_outport]
        print([gui_inport, gui_outport])
    else:
        print(" Starting the polysynth adapter...")
        if gui_inport == "":
            print("No inport set. Opening ALL inports.")
            inportlist = md.get_input_names()
        else:
            print("Opening inport {}.".format(gui_inport))
            inportlist = [gui_inport]
        if gui_outport == "":
            print("No outport set. Opening ALL outports.")
            outportlist = md.get_output_names()
        else:
            print("Opening outprt {}".format(gui_outport))
            outportlist = [gui_outport]
            
    open_iports = []
    open_oports = []
    for i in inportlist:
        open_iports.append(md.open_input(i))
    for o in outportlist:
        open_oports.append(md.open_output(o))
    print(" DONE.")   
    

    # Turn off the 3NG  to be sure   
    send_all(turn_3ng_off(midi_channel, cc_bypass), open_oports)
    
    # Send the glide and waveshape info from the GUI to the Helix device. 
    for i in [0,1,2]:
        if GUI == True:
            msg_w = md.Message('control_change', 
                                            channel = midi_channel, 
                                            control = ccshapes[i],
                                            value   = wave_to_cc(shape)
                                            )  
            msg_g = md.Message('control_change', 
                                            channel = midi_channel, 
                                            control = ccglides[i],
                                            value   = glide
                                            )  
            send_all(msg_w, open_oports)
            send_all(msg_g, open_oports)
    
    
    # Initialze the main loop.
    print(" Starting main loop of the adapter. Fingers crossed!")
    
    keycounter  = 0
    last_note   = 0
    loop        = True
    TNGstate    = False
    while loop: 
        for port in open_iports:
            msg = port.poll()
            if msg is not None:
                # Wait for MIDI input through the inport
                if msg.type=="note_on":
                    TNGstate = True
                    
                    # Increase the key counter by one.
                    keycounter +=1
                    
                    # Remember the last key pressed
                    last_note = msg.note
                    
                    # Update all three oscillators
                    # And check that the interval notes are in range of (0,...,127)
                    intvl_notes  = [msg.note, 
                                     msg.note + interval1,
                                     msg.note + interval2]
                    
                    for i in [0,1,2]:
                        if intvl_notes[i] < 0:
                            intvl_notes[i] = msg.note
                        elif intvl_notes[i] > 127:
                            intvl_notes[i] = msg.note
                        oscillators[i].set_note(intvl_notes[i])
                        oscillators[i].volume = msg.velocity

        
        
                elif msg.type=="note_off":
                    # Decrease the key counter by one.
                    keycounter -= 1
                    # If the key of the note playing right now is released, stop the
                    # synth.
                    if msg.note == last_note:
                        TNGstate = False
            
                elif msg.type=="control_change":
                    # Use a CC value as an "emergency exit" out of the main loop.
                    if msg.control == cc_off: 
                        print(" CC value {} received. Stopping the adapter.".format(cc_off))
                        loop        = False
                        TNGstate    = False
                        
                # Send the information for aLL oscillators to the Helix device.
                for o in oscillators:
                    for m in o.gen_message(monopoly="mono"):
                        send_all(m, open_oports)
                        
                # This conditional is just to be sure the synth stops if nothing is
                # pressed anymore.           
                if keycounter < 1:
                    TNGstate = False
                    
                if TNGstate == True:
                    send_all(turn_3ng_on(midi_channel, cc_bypass), open_oports)
                else:
                    send_all(turn_3ng_off(midi_channel, cc_bypass), open_oports)
                
    print(" ... Shutting adapter down. Goodbye.")
    for i in open_iports:
        i.close()
    for o in open_oports:
        o.close()
    print(" ..::: Ports are closed. :::..")
    
    
    
    
def helix_midi_adapter_GUI():
    """
    This function is a GUI, wrapping the adapter functions for monosynth and
    polysynth in a handy interface. 

    Returns
    -------
    None.

    """
    # Data for Settings
    #####################################################################
    synth_types         = ["mono", "poly"]
    available_channels  = [x for x in range(0,16)]
    available_dev       = ["Helix", "Helix Rack", "Helix LT", 
                           "HX Stomp", "HX Stomp XL", "HX Effects"]
    default_cc          = [[80,81,82,83,84],[85,86,87,88,89],[90,91,92,93,94]]
    default_bypass      = 77
    available_cc        = {
                            available_dev[0]: [x for x in range(1,129) if x not in 
                                               [1,2,3,49,50,51,52,52,53,54,55,56,
                                                57,58,59,60,61,62,63,65,66,67,0,32,
                                                64,68,69,70,71,72,73,74,75,76,128]
                                               ],
                            available_dev[1]: [x for x in range(1,129) if x not in 
                                               [1,2,3,49,50,51,52,52,53,54,55,56,
                                                57,58,59,60,61,62,63,65,66,67,0,32,
                                                64,68,69,70,71,72,73,74,75,76,128]
                                               ],
                            available_dev[2]: [x for x in range(1,129) if x not in 
                                               [1,2,49,50,51,52,52,53,54,55,56,
                                                57,58,59,60,61,62,63,65,66,67,0,32,
                                                64,68,69,70,71,72,73,74,75,76,128]
                                               ],
                            available_dev[3]: [x for x in range(1,129) if x not in 
                                               [1,2,3,49,50,51,52,52,53,54,55,56,
                                                57,58,59,60,61,62,63,65,66,67,0,32,
                                                64,68,69,70,71,72,73,74,75,76,128]
                                               ],
                            available_dev[4]: [x for x in range(1,129) if x not in 
                                               [1,2,3,49,50,51,52,52,53,54,55,56,
                                                57,58,59,60,61,62,63,65,66,67,0,32,
                                                64,68,69,70,71,72,73,74,75,76,128]
                                               ],
                            available_dev[5]: [x for x in range(1,129) if x not in 
                                               [1,2,49,50,51,52,53,54,60,61,62,63,
                                                64,65,66,67,68,69,70,71,72,73,74,
                                                75,76,128]
                                               ]
                            }
    available_shapes    = ["saw_up", "saw_down", "triangle", "sine", "square"]
    
    
    # Setting up Tkinter and window geometry
    #####################################################################
    version     = 1.0
    root        = tk.Tk()
    root.title("MIDI to HX Adapter {}".format(version))
    root.iconbitmap('./assets/favicon.ico')
    
    dim_window      = [830,700]
    dim_screen      = [root.winfo_screenwidth(),root.winfo_screenheight()]
    dim_center      = [int(dim_screen[0]/2 - dim_window[0]/2), 
                       int(dim_screen[1]/2 - dim_window[1]/2)]
    
    root.geometry(f'{dim_window[0]}x{dim_window[1]}+{dim_center[0]}+{dim_center[1]}')
    
    ipx = 20
    ipy = 30
    px = 10
    py = 10
    
    
    # Setting up the main grid
    #####################################################################
    root.columnconfigure((0,1,2), weight=100)
    
    ## Label Frame for HX base info (Device, MIDI channel, Bypass-CC)
    lf_dev          = ttk.LabelFrame(root, text="HX device info: ")
    lf_dev.grid(column=0, row=1, padx=px, pady=py, sticky=tk.NSEW)
    lf_dev.rowconfigure((0,1,2), weight=100)
    lf_dev.columnconfigure((0,1), weight=100)
    
    ## Label Frame for MIDI devices
    lf_midi     = ttk.LabelFrame(root, text="MIDI devices: ")
    lf_midi.grid(column=1, row=1, padx=px, pady=py, sticky=tk.NSEW, ipady=ipy, ipadx=ipx)
    lf_midi.rowconfigure((0,1,2), weight=100)
    lf_midi.columnconfigure((0,1), weight=100)
    
    
    ## Label Frames for oscillator CC settings (interactive)
    lf_o_cc     = ttk.LabelFrame(root, text="CC parameters for 3NG: ")
    lf_o_cc.grid(column=1, row=2, padx=px, pady=py, sticky=tk.NSEW)
    lf_o_cc.rowconfigure((0,1), weight=100)
    lf_o_cc.columnconfigure((0,1,2), weight=100)
    
    ## Additional info
    lf_info     = ttk.LabelFrame(root, text="Additional information: ")
    lf_info.grid(column=1, row=3, padx=px, pady=py, sticky=tk.NSEW)
    
    ## Label Frames for each of the oscillators:
    lf_osc_cc_i = []
    # lf_osc_i    = []
    for i in [0,1,2]:
        lf_osc_cc_i.append(ttk.LabelFrame(lf_o_cc, text="Oscillator {}: ".format(i+1)))
        lf_osc_cc_i[i].grid(column=i, row=1)
    
    
    # Label Frame for MonoSynth settings
    lf_ms_set = ttk.Labelframe(root, text="Synth adapter settings: ")
    lf_ms_set.grid(column=0, row=2, padx=px, pady=py, sticky=tk.NSEW)
    lf_ms_set.rowconfigure((0,1,2), weight=100)
    lf_ms_set.columnconfigure((0,1), weight=100)
    
    lf_control = ttk.LabelFrame(root, text="Adapter controls: ")
    lf_control.grid(column=0, row=3, padx=px, pady=py, sticky=tk.NSEW)
    
    
    # Variables that can be set or seen in the GUI
    #####################################################################
    ## MIDI base channel
    cc_channel      = tk.IntVar(root, value = 0, name="MIDI Channel")
    ## MIDI base channel
    cc_bypass       = tk.IntVar(root, value = default_bypass, name="Bypass CC")
    ## MIDI CC parameters that the adapter adresses in the HX device
    cc_osc          = [[tk.IntVar(root, value=default_cc[0][x]) for x in range(0,5)]]
    cc_osc.append([tk.IntVar(root, value=default_cc[1][x]) for x in range(0,5)])
    cc_osc.append([tk.IntVar(root, value=default_cc[2][x]) for x in range(0,5)])
    # Shapes of the oscillators (should be identical in poly)
    shape          = tk.StringVar(root, value=available_shapes[0])
    # Which HX device is connected?
    device          = tk.StringVar(root, value=available_dev[2])
    # Mode of the adapter
    adapter_mode    = tk.StringVar(root, value='poly')
    # Intervals for the MonoSynth
    intvl1 = tk.IntVar(root, value = 0 )
    intvl2 =tk.IntVar(root, value = 0)
    # Glide property
    glide_entry = tk.IntVar(root, value = 0 )
    # Input and output MIDI device
    midi_in = tk.StringVar(root, value="")
    midi_out= tk.StringVar(root, value="")
    
    
    # Widgets for the variables
    #####################################################################
    ## Device section
    combo_dev   = ttk.Combobox(lf_dev, 
                               textvariable = device, 
                               values=available_dev, 
                               state="readonly", 
                               width=10
                               )
    
    spin_chl    = ttk.Spinbox(lf_dev, 
                              textvariable = cc_channel,
                              values=available_channels,
                              width=3
                              )
    
    ## Oscillator CC section
    l_cc_widgets = [[],[],[]]
    for i in [0,1,2]:
        for j in [0,1,2,3,4]:
            l_cc_widgets[i].append( ttk.Combobox(lf_osc_cc_i[i], 
                                                 textvariable=cc_osc[i][j], 
                                                 values=available_cc[device.get()],
                                                 width=3
                                                 )
                                   )
    combo_byp   = ttk.Combobox(lf_o_cc,
                               textvariable = cc_bypass,
                               values=available_cc[device.get()],
                               width=3
                               )
    
    ## MIDI device section
    combo_input     = ttk.Combobox(lf_midi,
                                   textvariable=midi_in,
                                   values=md.get_input_names(),
                                   width=30)
    combo_output    = ttk.Combobox(lf_midi,
                                   textvariable=midi_out,
                                   values=md.get_output_names(),
                                   width=30)
    
    ## Adapter Settings
    combo_mode = ttk.Combobox(lf_ms_set, 
                              textvariable = adapter_mode, 
                              values=synth_types,
                              state="readonly",
                              width=7
                              )
    combo_shape= ttk.Combobox(lf_ms_set,
                              textvariable = shape, 
                              values=available_shapes, 
                              state="readonly", 
                              width=7
                              )
    spin_i1    = ttk.Spinbox(lf_ms_set, 
                             textvariable = intvl1, 
                             values=[x for x in range(-127,128)], 
                             width=3
                             )
    spin_i2    = ttk.Spinbox(lf_ms_set, 
                             textvariable = intvl2, 
                             values=[x for x in range(-127,128)], 
                             width=3
                             )
    spin_gli    = ttk.Spinbox(lf_ms_set, 
                             textvariable = glide_entry, 
                             values=[x for x in range(0,128)], 
                             width=3
                             )
    
    ## Adapter Controls
    button_start = ttk.Button(lf_control, 
                              text = "Start adapter!",
                              command = lambda: threading.Thread(
                                  target = activate_adapter(
                                      inport    = midi_in.get(), 
                                      outport   = midi_out.get(), 
                                      mode      = adapter_mode.get(), 
                                      chn       = cc_channel.get(), 
                                      shp       = shape.get(), 
                                      i1        = intvl1.get(), 
                                      i2        = intvl2.get(), 
                                      ccbyp     = cc_bypass.get(), 
                                      ccoff     = 18,
                                      ccshp     = [cc_osc[0][0].get(),cc_osc[1][0].get(),cc_osc[2][0].get()], 
                                      cco       = [cc_osc[0][1].get(),cc_osc[1][1].get(),cc_osc[2][1].get()], 
                                      ccnot     = [cc_osc[0][2].get(),cc_osc[1][2].get(),cc_osc[2][2].get()],  
                                      cclev     = [cc_osc[0][3].get(),cc_osc[1][3].get(),cc_osc[2][3].get()],  
                                      ccgli     = [cc_osc[0][4].get(),cc_osc[1][4].get(),cc_osc[2][4].get()],
                                      gli       = glide_entry.get()
                                      )
                                  ).start()
                              )
    
    # button_stop = ttk.Button(lf_control, 
    #                           text = "Stop adapter!",
    #                           command = lambda: deactivate_adapter()
    #                           )
    
    
    
    
    
    # Labels for the widgets
    #####################################################################
    ## Logo
    image   = Image.open("./assets/logo.gif")
    logo    = ImageTk.PhotoImage(image)
    l_logo  = tk.Label(image=logo)
    
    ## Additional info
    additional_info = "Set the bypass control of the 3-Note-Generator block to the value above. \n \nAdjust the parameters of the three oscillators to be controlled by the CC values above (80-94 is the default). \n\n It is advisable to turn Snapshot Control for the 3NG block off.  \n\n Send CC parameter 18 (any value) to stop the adapter in emergencies.\n Pressing more than 7 keys also stops the adapter."
    l_info = ttk.Label(lf_info, text=additional_info)
    
    ## Device section
    l_device = []
    l_device.append(ttk.Label(lf_dev, text="Device to control: "))
    l_device.append(ttk.Label(lf_dev, text="Base MIDI channel: "))
    
    
    ## Oscillator CC section
    l_cc_labels = [[],[],[]]
    for i in [0,1,2]:
        l_cc_labels[i].append(ttk.Label(lf_osc_cc_i[i], text="CC Shape: "))
        l_cc_labels[i].append(ttk.Label(lf_osc_cc_i[i], text="CC Octave: "))
        l_cc_labels[i].append(ttk.Label(lf_osc_cc_i[i], text="CC Note: "))
        l_cc_labels[i].append(ttk.Label(lf_osc_cc_i[i], text="CC Level: "))
        l_cc_labels[i].append(ttk.Label(lf_osc_cc_i[i], text="CC Glide: "))
    l_bypass = ttk.Label(lf_o_cc, text="CC bypass for 3NG: ")
    
    
    
    ## MIDI device section
    l_midi = []
    l_midi.append(ttk.Label(lf_midi, text="Input Device: "))
    l_midi.append(ttk.Label(lf_midi, text="Output Device: "))
    
    ## Adapter settings section
    l_adapter = []
    l_adapter.append(ttk.Label(lf_ms_set, text="Synth mode: "))
    l_adapter.append(ttk.Label(lf_ms_set, text="Waveform: "))
    l_adapter.append(ttk.Label(lf_ms_set, text="Interval 1: "))
    l_adapter.append(ttk.Label(lf_ms_set, text="Interval 2: "))
    l_adapter.append(ttk.Label(lf_ms_set, text="Glide: "))
    
    # Place the widgets and labels on the grid
    #####################################################################
    ## Logo GFX
    l_logo.grid(column=0, row=0, columnspan=3)
    
    
    ## Info text 
    l_info.grid(column=0, row=0)
    
    
    ## Device section
    ### Widgets
    combo_dev.grid(column=1, row=0, sticky=tk.W)
    spin_chl.grid(column=1, row=1, sticky=tk.W)
    ### Labels
    for i in [0,1]:
        l_device[i].grid(column=0, row=i)
    
    
    ## Oscillator CC section
    ### Widgets
    for i in [0,1,2]:
        for j in [0,1,2,3,4]:
            l_cc_widgets[i][j].grid(column=2, row=j, padx=px)
    combo_byp.grid(column=1, row=5, sticky=tk.W)
                     
    ### Labels
    for i in [0,1,2]:
        for j in [0,1,2,3,4]:
            l_cc_labels[i][j].grid(column=1, row=j, padx=px)
    l_bypass.grid(column=0, row=5, sticky=tk.W, padx=px, pady=py)
    
    
    ## MIDI device section
    ### Widgets
    combo_input.grid(column=2, row=0)
    combo_output.grid(column=2, row=1)
    
    ### Labels
    for i in [0,1]:
        l_midi[i].grid(column=1, row=i)
    
    
    ## Adapter settings section
    ### Widgets
    combo_mode.grid(    column=1, row=0, sticky=tk.W)
    combo_shape.grid(   column=1, row=1, sticky=tk.W)
    spin_i1.grid(       column=1, row=2, sticky=tk.W)
    spin_i2.grid(       column=1, row=3, sticky=tk.W)
    spin_gli.grid(      column=1, row=4, sticky=tk.W)
    ### Labels
    for i in [0,1,2,3,4]:
        l_adapter[i].grid(    column=0, row=i, padx=px, pady=py)
    
    ## Start button
    button_start.grid(column=0, row=1, padx=px, pady=py, sticky=tk.NSEW)
    
    
    
    
    root.mainloop()
       
    
