#!/bin/bash

set -x

path2yaml=/scratch/wei/cadre/cadre26_noaa_tutorial/ufs_da_diagnostics/diagnostic/yamls
day1output=/scratch/wei/cadre/cadre26_noaa_tutorial/exp_case/wei_cadre26.8
day3output=/scratch/wei/cadre/cadre26_noaa_tutorial/exp_case/Day3_exp_gaussian_thinning.11
griddir=/scratch/cadre26/input_data/grid
expname=day3_atms_thining

rm *.yaml

for yamlfile in increment_maps.yaml  obs_diag.yaml  spectra_ana_inc.yaml
do
   sed -e "s?Day1EXPDIR?${day1output}?g" \
       -e "s?Day3EXPDIR?${day3output}?g" \
       -e "s?GRIDDIR?${griddir}?g" \
	   ${path2yaml}/${expname}/${yamlfile} > ${yamlfile}
done

export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg

ufsda-spectra-ana-inc --yaml spectra_ana_inc.yaml
ufsda-inc-maps --yaml increment_maps.yaml
ufsda-obs-diag --yaml obs_diag.yaml
ufsda-jedi-log ${day3output}/OUTPUT.fv3jedi --output log_report_${expname}.txt

