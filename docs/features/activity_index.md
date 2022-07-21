# Documentation: How to implement celest's activity index measure into wfntp

## Definition of Activity Index in CeleST paper
The activity index : 
> sums up the number of pixels that are painted by the body during the time that it takes an animal to do two stroke  

The Activity Index measure is calculated with the help of another measure : brush strokes which is the area that the body would “paint” (= number of pixels covered) in a single complete stroke. 

The brush stroke : 
> reports on the area that the body of the animal would ‘‘paint’’ (the number of pixels covered) in a single complete stroke, giving an indication of the depth of the movement and the extent to which the animal has flexed in a given stroke.

## Measures in wf_ntp script relevant to calculate activity index
Two variables can be used in wfntp : `area` and `BPM`.  
`area` is the total area covered by the worm (particle) in mm.  
`BPM` is the number of bends per minutes.  
Bends and strokes are considered to be equivalent.     
We use `BPM` to determine the time it takes a worm to do two bends.  

## Calculation of the Activity Index in WF_NTP (first iteration)

The following calculation could be implemented in the function `extract_data` in the file `WF_NTP_script.py`: 
$$ activity\_index = \frac{area}{\frac{2 * 60}{BPM}}$$