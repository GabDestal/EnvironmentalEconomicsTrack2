# 2. Data

Our data come from the Copernicus Interactive Climate Atlas
(https://atlas.climate.copernicus.eu/, version v2.5), produced by the
Copernicus Climate Change Service (C3S). We downloaded the series through
the Atlas's regional-information export on 29 October 2026. All series
come from ERA5-Land, a land-surface reanalysis that ECMWF produces for C3S
by re-running the land component of the ERA5 model on a 0.1° regular
grid; the Atlas retains this native resolution. We study four European countries along
a south-north gradient: Spain, France, Germany and Sweden. Every series is
annual and covers 1950 to 2025, giving 76 observations per series. A
validation script (`scripts/check_raw.py`) confirms that all 16 files share
the same Atlas version and dataset, that each year from 1950 to 2025
appears exactly once, and that no observation is missing. We therefore
carry out no imputation or interpolation. The label "1961-1990" in the
file headers refers to the period the Atlas highlights in its charts; it
does not restrict the data.

We use two indices. The first, TXx, is the monthly maximum of daily
maximum near-surface air temperature, in degrees Celsius. In each grid
cell, the daily maximum is the highest of the hourly 2 m temperatures of
that day, and the Atlas takes the highest of these daily maxima in a
given month. It then averages these cell values over the country's territory,
weighting each cell of the regular latitude-longitude grid by the cosine
of its latitude; since ERA5-Land covers land only, sea cells do not enter
the average (C3S Atlas User Guide). Our country-level TXx is
therefore the average across the country of each location's hottest day of
the month, not the single hottest value recorded anywhere in the country.
We use TXx for June, July and August. Pooling the three summer months gives
90 observations per 30-year period instead of the 30 that a single month
would provide. This matters because our question concerns the tails of
the distribution, which are poorly estimated in small samples. The cost is
that the three months are not independent draws from one distribution, as
August is typically hotter than June. Any pooled comparison must allow for
this seasonal difference.

The second index is the Standardised Precipitation-Evapotranspiration
Index over a six-month window (SPEI-6). For each grid cell, the balance
between precipitation and potential evapotranspiration (PET) is
accumulated over the preceding six months. It is then transformed, by
fitting a probability distribution, into standard deviations from the
mean of a reference period of 1971-2005. The Atlas documentation is inconsistent on
this point: the dataset documentation gives 1971-2010, while the v2.5
changelog gives 1971-2005 in the context of projections; we report the
period shown in the Atlas information panel for SPEI-6 computed from
ERA5-Land. Potential evapotranspiration is computed with the Hargreaves
formulation, which the Atlas has used since version 2.0, implemented with
the xclim library (C3S Atlas User Guide and dataset documentation). The
index has no units; negative values indicate conditions drier than the reference
climate and positive values wetter ones. As with TXx, the Atlas averages
the grid-cell values over each country. We keep only the September value
in each year. Because the window is six months long, the September value
summarises the water balance from April to September, that is, the whole
growing and warm season. Taking one month per year also avoids the strong
autocorrelation that consecutive monthly SPEI-6 values would introduce, as
they share five of their six months. Each year then contributes one
non-overlapping observation of warm-season dryness.

These data have several limitations. First, ERA5-Land is a reanalysis,
not a set of station observations. It combines a numerical model with
assimilated observations, and its representation of extremes depends on
the model's physics as well as on the observations. A specific concern
affects the start of our sample: the Atlas disables ERA5-Land trends before 1978
because of a potential inconsistency in the ERA5 forcing used for that
period. Our early period overlaps these years, so part of any difference
between the early and recent distributions could be a data artefact
rather than a change in climate. Second, averaging over a country
smooths local extremes. A heatwave or drought that affects only part of
the territory is diluted in the national mean, so our series understate
the severity of the most extreme local events, and the smoothing is
likely to be stronger for large or climatically diverse countries such as
France and Spain. In addition, the Atlas documentation does not state how
grid cells that straddle a national border are treated, so the exact
spatial footprint of each country average is not known. Third, SPEI depends on modelling choices: the reference
period sets the zero of the scale, and the PET formulation determines how
strongly rising temperatures translate into apparent drying. A different
reference period or PET method could shift the series or change their
trends. Fourth, standardisation is done per grid cell, and averaging
standardised values across cells reduces their variance. The country-level
SPEI-6 series have standard deviations between 0.754 and 0.902, all below
the unit variance of a cell-level index, and their 1950-2025 means are
negative, between -0.285 and -0.037. As a result, the Atlas's fixed
threshold of -1.5 for "severe" drought is rarely crossed at the country
level, and a count of exceedances of that threshold would carry little
information. We therefore define extremes with percentile thresholds taken
from each country's own distribution. Finally, the tails contain few
observations by construction. With 76 years per series, or 90 observations
per 30-year period for pooled TXx, the 90th or 95th percentile within a
period is estimated from only a handful of values. Estimates of tail
shape are thus imprecise, and the inference in Section 3 accounts for
this [VERIFY: align with the methods section].
