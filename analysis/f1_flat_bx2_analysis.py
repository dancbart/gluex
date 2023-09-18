# script for making histograms from flat best chi2/ndf trees for any datatype

import ROOT
import time
import os
import my_library.common_analysis_tools as ct
import sys

"""
usage of this file is as follows:
python3 f1_flat_bx2_analysis.py <channel> <run_period> <data_type>
"""

os.nice(18)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
start_time = time.time()

channel = sys.argv[1]
run_period = sys.argv[2]
data_type = sys.argv[3]

ct.verify_args(channel, run_period, data_type)

file_and_tree = ct.get_flat_file_and_tree(channel, run_period, data_type, filtered=False)

# if run_period == '2019_unconstrained':
#     treename = 'pimkpks__T1_S2_M16'
# elif run_period == '2019_constrained':
#     treename = 'pimkpks__T1_S2'

histo_array = []

## LOAD IN DATA ##

df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

## DEFINE ALL NECESSARY COLUMNS ##

# print(df.GetColumnNames())

df = ct.define_columns(df, channel)


## FILTER DATAFRAME AFTER DATA IS DEFINED ##

df = ct.filter_dataframe(df, channel)
print('cuts done in {} seconds'.format(time.time() - start_time))


## MAKE HISTOGRAMS ##

ks_m = df.Histo1D(('ks_m', 'ks_m', 100, 0.3, 0.7), 'ks_m')

## SAVE FILTERED DATA FOR USE ELSEWHERE IF NEEDED ##
## COMMENT/UNCOMMENT AS NEEDED WHEN CHANGING THINGS ABOVE THIS LINE ##
output_path = ct.get_path_for_output_file(channel, data_type)
df.Snapshot(f'{channel}_filtered_{ct.RUN_DICT[run_period]}', f'{output_path}/{channel}_filtered_{ct.RUN_DICT[run_period]}.root')


# ## FILTER BEAM AND T RANGE TO FIT WITHIN THE INDEX SET EARLIER ##
df = df.Filter(ct.BEAM_RANGE).Filter(ct.T_RANGE)

print('cut file written in {} seconds'.format(time.time() - start_time))

## LOOP OVER K* CUTS AND EXECUTE HISTO FILLING FUNCTION ##

n_e_bins = len(ct.ALLOWED_E_BINS)
n_t_bins = len(ct.ALLOWED_T_BINS)

def fill_histos(cut_df, histo_array, cut, channel, beam_index=0, t_index=0):
    if channel == 'pipkmks':
        cut_name = ct.KSTAR_CUT_NAME_DICT_PIPKMKS[cut]
    elif channel == 'pimkpks':
        cut_name = ct.KSTAR_CUT_NAME_DICT_PIMKPKS[cut]
    hist_name = f'{channel}_kstar_{cut_name}_cut_'
    beam_name = 'beam_full_'
    t_name = 't_full'
    if beam_index > 0:
        beam_low = ct.BEAM_INDEX_DICT[beam_index][0]
        beam_high = ct.BEAM_INDEX_DICT[beam_index][1]
        beam_name = f'beam_{beam_low}_{beam_high}_'
    if t_index > 0:
        t_low = ct.T_CUT_DICT[t_index][0]
        t_high = ct.T_CUT_DICT[t_index][1]
        t_name = f't_{t_low}_{t_high}'
    hist_name += beam_name + t_name
    histo_array.append(cut_df.Histo1D((hist_name, hist_name, 150, 1.0, 2.5), f'{channel}_m'))

    
if channel == 'pipkmks':
    cut_list = ct.F1_CUT_LIST_PIPKMKS
elif channel == 'pimkpks':
    cut_list = ct.F1_CUT_LIST_PIMKPKS

for cut in cut_list:
    cut_df = df.Filter(cut)
    fill_histos(cut_df, histo_array, cut, channel)
        

    for energy_index in range(1, n_e_bins+1):
        e_cut_df = cut_df.Filter(f'e_bin == {energy_index}')
        fill_histos(e_cut_df, histo_array, cut, channel, beam_index=energy_index)

        for t_index in range(1, n_t_bins+1):
            e_t_cut_df = e_cut_df.Filter(f't_bin == {t_index}')
            fill_histos(e_t_cut_df, histo_array, cut, channel, beam_index=energy_index, t_index=t_index)
         
    for t_index in range(1, n_t_bins+1):
       t_cut_df = cut_df.Filter(f't_bin == {t_index}')
       fill_histos(t_cut_df, histo_array, cut, channel, t_index=t_index)

print("histos done in {} seconds".format(time.time() - start_time))

## WRITE HISTOGRAMS TO FILE ##

target_file = ROOT.TFile(f"{output_path}/{channel}_flat_result_{ct.RUN_DICT[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))


ks_m.Write()

for histo in histo_array:
    histo.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close()

ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/{channel}_{data_type}_graph_{ct.RUN_DICT[run_period]}.dot")