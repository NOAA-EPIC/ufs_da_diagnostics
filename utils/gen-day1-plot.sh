#!/bin/bash

set -x

path2yaml=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/diagnostic/yamls
path2output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_day1.8909339

for yamlfile in increment_maps.yaml  obs_diag.yaml  spectra_bkg_inc.yaml
do
   sed -e "s?EXPDIR?${path2output}?g" ${path2yaml}/day1/${yamlfile} > ${yamlfile}
done

export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg

ufsda-spectra-bkg-inc --yaml spectra_bkg_inc.yaml
ufsda-inc-maps --yaml increment_maps.yaml
ufsda-obs-diag --yaml obs_diag.yaml
ufsda-jedi-log ${path2output}/OUTPUT.fv3jedi --output log_report_day1.txt

