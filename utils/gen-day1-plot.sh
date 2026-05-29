#!/bin/bash

set -x

path2yaml=/work2/noaa/epic/weihuang/cadre/ufs_da_diagnostics/diagnostic/yamls
path2output=/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/year2_cases/exp_case/cadre26_Day1.8988876

for yamlfile in increment_maps.yaml  obs_diag.yaml  spectra_bkg_inc.yaml
do
   sed -e "s?Day1EXPDIR?${path2output}?g" ${path2yaml}/day1/${yamlfile} > tmp/${yamlfile}
done

export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg

ufsda-spectra-bkg-inc --yaml tmp/spectra_bkg_inc.yaml
ufsda-inc-maps --yaml tmp/increment_maps.yaml
ufsda-obs-diag --yaml tmp/obs_diag.yaml
ufsda-jedi-log ${path2output}/OUTPUT.fv3jedi --output tmp/log_report_day1.txt

