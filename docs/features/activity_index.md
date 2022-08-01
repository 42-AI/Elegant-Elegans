# Documentation: How to implement celest's activity index measure into wfntp

## Activity Index
> **Definition**\
> in CeleST paper, the activity index is defined as the sums over the number of pixels that are painted by the body during the time that it takes an animal to do two strokes.


The Activity Index is calculated based on the **brush strokes**.

> **The brush stroke**\
> Reports on the area that the body of the animal would *"paint"* (the number of pixels covered) in a single complete stroke, giving an indication of the depth of the movement and the extent to which the animal has flexed in a given stroke.

## Measures in wf_ntp script relevant to calculate activity index
In WF NTP, two variables might be used to calculate the activity index:
* `area` corresponding to the total area covered by the worm (particle) in mm.
* `BPM` corresponding to the number of bends per minutes.

As first approximation, we consider that **bends** and **strokes** are somehow equivalent.


Thus `BPM` to determine the time it takes a worm to do two bends.

## Calculation of the Activity Index in WF_NTP (first iteration)

The following calculation could be implemented in the function `extract_data` in the file `WF_NTP_script.py`:

$$
activity\_index = \frac{area}{\frac{2 \times 60}{BPM}} = \frac{area \times BPM}{120}
$$
