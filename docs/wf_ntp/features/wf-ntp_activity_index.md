WF-NTP Activity index implementation
====================================

The activity index is calculated similarly to [CeleST (2014)](https://doi.org/10.1371/journal.pcbi.1003702):

First, the brush stroke is computed comparing, for each bend $b$, the ratio between the residual area painted by the worm and the average area occupied by its body.

Assuming that over one bend $b$ the worm paints a total of $\mathrm{TotalArea}_b$ pixels over all the frames, and the average area occupied by its body is $\mathrm{AverageBodyArea}_b$, the brush stroke is:

$$
\mathrm{BrushStroke}_b = \frac{\mathrm{TotalArea}_b - \mathrm{AverageBodyArea}_b}{\mathrm{AverageBodyArea}_b} 
$$

The activity index corresponds to the value of the brush stroke, normalized by the time that the worm has taken to complete one bend:

$$
\mathrm{ActivityIndex}_b = \frac{\mathrm{BrushStroke}_b}{\Delta t_b}
$$

Note: In the current version, the activity index is still not normalized and therefore equal to the brush stroke.

Properties
----------
The brush stroke is therefore a number greater then zero:
- the value $0$ (zero) corresponds to a worm that doesn't move at all during the bend: $\mathrm{TotalArea}_b =\mathrm{AverageBodyArea}_b$;
- the value $n$ corresponds to a worm that occupied in total an amount of $(n+1) \mathrm{AverageBodyArea}_b$ pixels during the bend.

Differences with CeleST
-----------------------
The formulas for the brush stroke and activity index are slightly different from the formula at page 6 of the aformentioned paper.
The only significant difference is that CeleST's value should be always negative and WF_NTP's always positive, the two values being exact opposites:
- BrushStoke(CeleST) = -BrushStoke(WF-NTP)
- ActivityIndex(CeleST) = -ActivityIndex(WF-NTP)

> **N

Output format
-------------

The activity index is computed over a normal execution of WF_NTP as one of the several features supported by the program.

Statistical properties of the activity index are presented in the results file (mean, standard deviation, etc.).
