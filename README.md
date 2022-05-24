# Envelope_Detection
The code of ED-SG filter on GEE and python code for simulated experiment, the DOI of the research paper is 10.1080/17538947.2022.2044397

We open sourced our code of ED-SG NDVI time-series method ( DOI: 10.1080/17538947.2022.2044397) for anayone who attempt to use the algorithm on their work.

The code is the script of the simulated experiment.

(1) Download NDVI time-series, cloud flags and QC flags from GEE (We've given the examples in scv files here)

(2) Ran "script_read_timeseries.py" to convert the csv files into excel files.

(3) Ran  "script_simulate_real.py" to generate the simulated true NDVI timeseries.

(4) Ran "script_probability_density.py" to generate the frequency distribution of the duration of the pixel state (clear or cloud-affected).

(5) Ran "script_landcover_ndvi.py" to generate the frequency distribution of the cloud covered NDVI value.

(6) Finally, conduct "script_simulation.py" to obtain the Agreement Coefficient array.

(7) Besides, through "script_artificial_factors.py", you can evaluate the algorithms on the simulated NDVI time-series with artifical "long-gap" and "high-value outliers"

We also open source the GEE code:

Extract and download timeseries:

https://code.earthengine.google.com/2fef7c6f6772e60f43034bebb72af8ef?noload=true

ED-SG on GEE:

https://code.earthengine.google.com/0018778b55d4d122cead07cf1cf0ead1?noload=true
