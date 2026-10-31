# 2. Data

We use the Copernicus Interactive Climate Atlas v2.5, produced by the Copernicus
Climate Change Service (C3S), with regional-information exports downloaded on
29 October 2026. The underlying dataset is ERA5-Land, ECMWF's land-surface
reanalysis on a 0.1° grid (C3S, 2023; 2024b). The four countries, Spain, France,
Germany and Sweden, span southern to northern Europe. All 16 downloaded
series cover 1950-2025, with 76 annual observations each. The raw-data check
confirms common dataset and version labels, complete coverage, unique years
and no missing values. We perform no imputation or interpolation. The
1961-1990 label in the file headers identifies the Atlas chart baseline,
not the downloaded coverage.

TXx is the monthly maximum of daily maximum near-surface temperature, in °C.
Within each grid cell, the daily maximum is the highest hourly 2 m temperature;
the Atlas then takes the month's highest daily value (C3S, 2023). Country
averages weight land cells by cosine latitude (C3S, 2024a). TXx therefore
averages local monthly maxima, rather than identifying the hottest reading
anywhere in the country. We pool June-August, giving 90 values per 30-year
period. Each value is expressed relative to the 1961-1990 mean of the same
country and calendar month, removing differences in seasonal levels. The
three observations from a summer remain correlated; Section 5 keeps them
together in the bootstrap.

SPEI-6 is the Standardised Precipitation-Evapotranspiration Index over six
months. It accumulates precipitation minus potential evapotranspiration
(PET) at each grid cell, fits a probability distribution and standardises the
result. PET uses the Hargreaves formulation, implemented through xclim
(Hargreaves and Samani, 1985; C3S, 2023; 2024a). The country average is
dimensionless; negative values indicate drier conditions. We retain September
only, covering April-September water balance, with 30 observations per
comparison period. These annual windows do not overlap, unlike consecutive
monthly SPEI-6 values. We adopt the 1971-2005 reference period explicitly
stated in the Atlas information panel for observations, reanalysis and
projections (`data/atlas_info_spei6.txt`). The dataset documentation instead
reports 1971-2010, while the v2.5 changelog gives 1971-2005 for projections;
this inconsistency remains a documentation limitation.

These data have several limitations. ERA5-Land is a model-based reanalysis,
not a collection of station measurements. The Atlas disables trends before
1978 because of potential inconsistency in the ERA5 forcing (C3S, 2024a).
Our early comparison period overlaps those years, so early-recent changes
may partly reflect data artefacts. The post-1978 check in Section 5 covers
mean trends only.

National averaging smooths local extremes, especially in large or diverse
countries, and the guide does not specify treatment of cells crossing
national borders. SPEI-6 also depends on the PET method and reference period.
Its standardisation occurs before spatial averaging: country-level SDs are
0.754-0.902 and full-record means range from -0.285 to -0.037. A country
average therefore need not have unit variance or zero mean. We use each
country's early-period percentiles rather than the rarely crossed fixed
threshold of -1.5. Finally, extreme percentiles rest on few observations.
Section 5 reports whole-year bootstrap intervals, which preserve dependence
within summers but not across years.

## References

Copernicus Climate Change Service (2023). *Gridded data underpinning the
Copernicus Interactive Climate Atlas: Description of the datasets and
variables*. Copernicus Knowledge Base, ECMWF Confluence Wiki. Dated
15 December 2023, updated 15 April 2025, last modified 28 May 2026.
https://confluence.ecmwf.int/x/UZZ-Fw (accessed 29 October 2026).

Copernicus Climate Change Service (2024a). *Copernicus Interactive Climate
Atlas: User Guide*. Copernicus Knowledge Base, ECMWF Confluence Wiki.
Dated 29 May 2024, last updated 29 May 2026.
https://confluence.ecmwf.int/x/aZZ-Fw (accessed 29 October 2026).

Copernicus Climate Change Service (2024b). *Gridded dataset underpinning
the Copernicus Interactive Climate Atlas* [Dataset]. European Centre for
Medium-Range Weather Forecasts. https://doi.org/10.24381/cds.h35hb680

Hargreaves, G. H. and Samani, Z. A. (1985). Reference crop
evapotranspiration from temperature. *Applied Engineering in Agriculture*,
1(2), 96-99. https://doi.org/10.13031/2013.26773
