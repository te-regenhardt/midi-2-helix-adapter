![Logo](assets/logo.gif?raw=true "Title")
# midi-2-helix-adapter
A software adapter to translate MIDI keyboard notes to a format that can be accepted from the Line6 Helix 3-Note-Generator as input.

## Connect your MIDI keyboard to the Helix Floor / LT / Rack / HX Stomp (XL) / HX Effects

Considering the versatile guitar effects and amp modeling devices from the Line 6 Helix family, two facts are quite apparent:

* The Line 6 Helix Family has a build in synthesizer/oscillators.
* The Helix devices can receive MIDI input.

The problem in this constellation is:
* The synths are not controllable by MIDI note values, so keyboards are not able to control them!

This adapter script connects MIDI keyboards (and the NOTE ON and NOTE OFF signals send by them) to the Helix's built-in oscillator.


### The oscillator situation:
Taking a look at the *3 Note Generator* (3NG) block in the Helix, the behaviour and controllability are as follows:
* The 3NG can be switched on as a whole, or be bypassed.
* The 3NG can be switched via a CC control change message
    * Control Change with value 0 switches the 3NG off.
    * Control Change with value 127 switches the 3NG on.
* Every parameter of the 3NG can be controlled with a CC command each. For each of the 3 oscillators of one 3NG-block the possibilities are:
    * Oscillator shape (Saw Up, Saw Down, Square, Sine, Triangle)
    * Oscillator note (C, C#, ..., A#, B)
    * Oscillator octave (0 to 8)
    * Oscillator glide (time to glide from one note value to another)
    * Oscillator volume
* None of the five parameters above are mapped as MIDI notes are (0 to 127) - except for volume and glide.


### The (usual) MIDI keyboard situation:
Usually, a MIDI keyboard sends a NOTE_ON message when hitting a key, together with velocity information. Upon release of the key, a NOTE_OFF message is sent, too.

### How the adapter fixes this (in a way):
The adapter maps the NOTE_ON and NOTE_OFF messages of the keyboard to the corresponding CC parameters on the HX device. This seems straightforward, but some extra code is needed to divide the NOTE_ON's note-value (0 to 127) into an "OSC1 Note" and "OSC1 Octave" signal. Additionally, the adapter translates "velocity" of the NOTE_ON to the synths "OSC Volume" parameter. 

The Mono functinality translates a single key into a note for OSC1. Note+interval1 and note+interval2 are used for OSC2 and OSC3. The Poly functionality of the adapter allows for three-voiced polyphony (using one of the three oscillators per key).

## How to use the adapter
Plug in the MIDI keyboard and the HX device into the computer. If you want to use the GUI (graphic user interface), just run the adapter script "helix_midi_adapter.py". 

You can run the adapter function without the GUI as described in the adapter script. Please note that you have to specify "gui_inport" and "gui_inport". If you do not tell the function what MIDI inport to use, it will try to send and receive on all ports. That might work, but there's no guarantee.

### Dependencies
You will need to have Tkinter, mido, threading and PIL (especially ImageTk and Image) for this script. You can install these via pip (or any other way you prefer). 

Additionally, mido requires the addition of rtaudio. Threading should already be installed together with python. The same goes for PIL.

Commonly you would need to run the following code:
pip install mido
pip install python-rtmidi
pip install tk
pip install Pillow

In my case, I used anaconda, that worked fine, too.

### The functions and their parameters
You can start the adapter with the following functions:
* helix_midi_adapter_GUI() will start a GUI to let you set all parameters you need. (Does not work in headless mode, as you have to start the whole thing with a button!)
* helix_polysynth() will start the adapter in poly mode. You probably have to provide the function arguments for this to work. 
* helix_monosynth() will start the adapter in mono mode. You probably have to provide the function arguments for this to work.

### Ports
If you use the non-GUI functions, you probably want to know your port names. You can set these as gui_inport and gui_outport in the function calls. You can find them via mido.get_input_names() and mido.get_output_names(). If you provide these functions no port names, then they will try to use all ports available. 

### Stopping the adapter
Due to threading I cannot provide a "stop" button on the GUI. At least not right now. 

The adapter can be stopped with two methods:
* Sending CC18 via a button on your keyboard
* Holding at least 7 keys simultaneously. 

### Known bugs
On Linux, I noticed that some of the MIDI devices were available twice. I do not know what the reason behind this is. This is not a problem on its own, but if you use the polysynth() and monosynth() functions without providing portnames, the adapter will open all duplicates and send weird duplicate information.

If MIDI Thru is activated on the Helix, the adapter is stuck for some reason. It is possible that some MIDI message queueing is going wrong here inside the adapter.

## Run the adapter on a rasperry pi (and possibly headless)
You can plug both HX and the keyboard into a raspberry and set upthe script to work without a monitor. This is very specific to your OS situation. But the main steps would be:
* put the script on the RPi
* install the dependencies (i.e. Tkintr, mido, PIL, threading) if not already present
* connect the USB keyboard and HX device
* find the port names of these two things
* call the adapter with gui_inport="Keyboard input port name" and gui_outport="Helix output port name"
* Let the python script start with the portnames automatically on boot, e.g. helix_polysynth(gui_inport='MPK Mini 1', gui_outport='Line 6 Helix 1')
