# AP4C-reading-Qualitative-to-Quantitative
with this program we are reading the values given by AP4C machine, and converting the Qualitative values to Quantitative values, before showing them on GUI interface


<img src="AP4C.PNG">

AP4C [ Apparatus 4 Channels ] is a chemical detection machine which takes a chemical sample as input and gives the concentration of 4 elements in the compound.
Which are mainly: 
<ul>
  <l>Phosphorus (P)</l> <br>
  <l>Sulfur (S)</l> <br>
  <l>Arsenic (As)</l> <br>
  <l>Hydrogen-Nitrogen-Oxygen (HNO)</l> <br>
  <l>Carbon-Hydrogen (CH)</l> <br>
</ul>

>The Carbon-Hydrogen are responsible for flame production in the machine to breake the sample compound into individual molecules.

>These molecules then release photons while dropping from higher octate [excited state] to lower octate [ground state] due to loss of enegry acuired by the flame produced.

>These photos are then collided to the metal plate to release electrons [Photo-Electric_Effect] , the density of these electrons manipulates the indication-light on the machine that give the idea about chemical concentration of particular molecule.

<img src="photo-electric-effect.png">

>The electron density is increased by a special method to turn the light on, as the raw electrons are significantly low in number to create a spark in the electric circuit and turn onn the LED.

<hr>

## GUI
<img src="gui.png">


## Development and tests

The CRC helper is implemented locally in `crc.py`; it does not require a third-party
`crc` package. Packet creation returns a `bytes` object suitable for
`pySerial.write()`.

Run the hardware-independent CRC regression tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The Streamlit application reads a 35-byte binary response, checks its CRC and
30-byte payload length before decoding it, and logs the seven 16-bit readings
as big-endian hexadecimal values. A connected AP4C device is still required
to verify the physical serial protocol end to end.
