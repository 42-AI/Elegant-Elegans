# References
- CeleST: Computer Vision Software for Quantitative Analysis of C. elegans Swim Behavior Reveals Novel Features of Locomotion doi:10.1371/journal.pcbi.1003702
- (WF-NTP) Assessing motor-related phenotypes of Caenorhabditis elegans with the wide field-of-view nematode tracking platform doi:10.1038/s41596-020-0321-9

# Data pipelines
## CeleST pipeline
1. Detect the outlines of the animals (maximisation of gradient flow)
2. Compute the curvilinear center line of the body, and the half-with of the body along the length
3. Track the animals in successive frames
4. Reject the overlaps between animals
5. Compute 13 body points from head to tail along the center line, and the curvature of the body at each point
6. Select a short time interval and compute the bidimentional Fourier transform of the curvature (on curvature and time)

## WF-NTP pipeline
1. Detect the regions occupied by the animals at each frame
2. Compute the centroid of the animal
3. At each frame and for each animal, fit with an ellipse
4. Compute the frequency of worm bendings using the changes in eccentricity of the ellipse

# List of CeleST features

## Wave initiation rate
The frequency of body wawes initiated from the head or the tail (# of bends/minutes)

Prerequisite: Celest pipeline #6 (Fourier transform)

Possible alternative in WF-NTP: not straightforward

## Body wave number
The number of waves traveling through the body (# of bends)

Prerequisite: Celest pipeline #6 (Fourier transform)

Possible alternative in WF-NTP: not straightforward without a Fourier transform

## Asymmetry
The global curvature of the body (positive value: clockwise curvature, negative value: counterclockwise)

Prerequisite: Celest pipeline #6 (Fourier transform)

Possible alternative in WF-NTP: Ratio of surface covered by the body on the left side of the ellipse, compared to the right side)

## Stretch
Range between the point of maximum and minimun curvature

Prerequisite: Celest pipeline #6 (Fourier transform)

Possible alternative in WF-NTP: not straightforward (computation of curvature along the body is required)

## Attenuation
Ratio between the amplitudes of the waves on the head and the tail

Prerequisite: Celest pipeline #6 (Fourier transform)

Possible alternative in WF-NTP: not straightforward without the computation of the Fourier transform

## Reverse swimming
Fraction of time of reverse swimming (global measure)

Prerequisite: Celest pipeline #6 (Fourier transform)

Possible alternative in WF-NTP: Fraction of the time of negative speed

## Curling
Fraction of time of maximal bending, defined as an self-overlap (global measure)

Prerequisite: Celest pipeline #3 (identification of head and tail, and tracking of the animal across time)

Possible alternative in WF-NTP: threshold on the eccentricity of the fitted ellipse


## Travel speed
Longitudinal distance travelled by the body center over a two-stroke interval

Prerequisite: Celest pipeline #3 (identification of body center, and tracking of the animal across time)

Possible alternative in WF-NTP: similar implementation, tracking the center of the ellipse

## Brush stroke
Area "painted" by the animal over a two-stroke interval, normalized by body size

Prerequisite: Celest pipeline #1

Possible alternative in WF-NTP: similar implementation (can also be normalised on the surface of the ellipse)

## Activity index
Brush stroke, normalized by the two-strokes interval

Prerequisite: Celest pipeline #6 

Possible alternative in WF-NTP: similar implementation (can also be normalised on the surface of the ellipse)
