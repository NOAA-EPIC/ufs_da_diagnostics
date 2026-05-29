#!/bin/bash

set -x

path2yaml=/work2/noaa/epic/weihuang/cadre/ufs_da_diagnostics/diagnostic/yamls
day1output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_day1.8909339
day3output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_Day3_exp_obs_error.8912363
expname=day3_atms_err

rm *.yaml

for yamlfile in increment_maps.yaml  obs_diag.yaml  spectra_ana_inc.yaml
do
   sed -e "s?Day1EXPDIR?${day1output}?g" \
       -e "s?Day3EXPDIR?${day3output}?g" \
	   ${path2yaml}/${expname}/${yamlfile} > ${yamlfile}
done

export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg

ufsda-spectra-ana-inc --yaml spectra_ana_inc.yaml
ufsda-inc-maps --yaml increment_maps.yaml
ufsda-obs-diag --yaml obs_diag.yaml
ufsda-jedi-log ${day3output}/OUTPUT.fv3jedi --output log_report_${expname}.txt

