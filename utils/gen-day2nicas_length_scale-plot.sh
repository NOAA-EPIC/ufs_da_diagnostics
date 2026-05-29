#!/bin/bash

set -x

path2yaml=/work2/noaa/epic/weihuang/cadre/ufs_da_diagnostics/diagnostic/yamls
day1output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_Day1.8988876
day2_nicas_length_scale_output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_Day2_exp_nicas_scale.8989381

rm -f tmp/*
for yamlfile in increment_maps.yaml  obs_diag.yaml  spectra_ana_inc.yaml
do
   sed -e "s?Day1EXPDIR?${day1output}?g" \
       -e "s?Day2nicas_length_scaleEXPDIR?${day2_nicas_length_scale_output}?g" \
	   ${path2yaml}/day2_nicas_length_scale/${yamlfile} > tmp/${yamlfile}
done

export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg

ufsda-spectra-ana-inc --yaml tmp/spectra_ana_inc.yaml
ufsda-inc-maps --yaml tmp/increment_maps.yaml
ufsda-obs-diag --yaml tmp/obs_diag.yaml
ufsda-jedi-log ${day2_nicas_length_scale_output}/OUTPUT.fv3jedi --output tmp/log_report_day2_nicas_length_scale.txt

