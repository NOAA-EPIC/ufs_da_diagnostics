#!/bin/bash

set -x

path2yaml=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/diagnostic/yamls
day1output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_day1.8909339
day2_nicas_length_scale_output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_Day2_exp_nicas_scale.8910150

for yamlfile in increment_maps.yaml  obs_diag.yaml  spectra_ana_inc.yaml
do
   sed -e "s?Day1EXPDIR?${day1output}?g" \
       -e "s?Day2nicas_length_scaleEXPDIR?${day2_nicas_length_scale_output}?g" \
	   ${path2yaml}/day2_nicas_length_scale/${yamlfile} > ${yamlfile}
done

export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg

ufsda-spectra-ana-inc --yaml spectra_ana_inc.yaml
ufsda-inc-maps --yaml increment_maps.yaml
ufsda-obs-diag --yaml obs_diag.yaml
ufsda-jedi-log ${day2_nicas_length_scale_output}/OUTPUT.fv3jedi --output log_report_day2_nicas_length_scale.txt

