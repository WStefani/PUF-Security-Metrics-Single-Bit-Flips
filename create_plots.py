#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Python Version: 3.8.13
    pypuf Version:  3.2.1
    Also cf. requirements_full.txt
"""

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from aux_funcs.plot_funcs import plot_S_j_by_j, plot_S_j_by_j_box, plot_inst_merit_desc_mult
from aux_funcs.simulation_funcs import sort_T2_return_by_I2O, T2_sel_from_T2_bflip_r_inst

import pickle
import numpy as np
from pathlib import Path
from tabulate import tabulate

import matplotlib.pyplot as plt


sub_dir_simulation  = './simulations/'
sub_dir_plots       = './plots/'
Path(sub_dir_plots).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    
    """ Load simulations from the simulation folder
    """
    
    with open(sub_dir_simulation + 'Test_2_on_0008_ArbiterPUF_inst', 'rb') as source_file:
        Test_2_on_0008_ArbiterPUF_inst = pickle.load(source_file)
    with open(sub_dir_simulation + 'Test_2_on_0008_FFArbiterPUF_inst', 'rb') as source_file:
        Test_2_on_0008_FFArbiterPUF_inst = pickle.load(source_file)
    with open(sub_dir_simulation + 'Test_2_on_0006_BistableRingPUF_inst', 'rb') as source_file:
        Test_2_on_0006_BistableRingPUF_inst = pickle.load(source_file)
    
    with open(sub_dir_simulation + 'Test_2_on_20_1000_XORArbiterPUF_inst', 'rb') as source_file:
        Test_2_on_20_1000_XORArbiterPUF_inst = pickle.load(source_file)
    with open(sub_dir_simulation + 'Test_2_on_10_1000_FFArbiterPUF_inst', 'rb') as source_file:
        Test_2_on_10_1000_FFArbiterPUF_inst = pickle.load(source_file)
    with open(sub_dir_simulation + 'Test_2_on_20_1000_XORBistableRingPUF_inst', 'rb') as source_file:
        Test_2_on_20_1000_XORBistableRingPUF_inst = pickle.load(source_file)
    
    
    """ Create sub selections from the extensive simulations
    """
    
    Test_2_on_20_10_XORArbiterPUF_inst  = T2_sel_from_T2_bflip_r_inst(10, Test_2_on_20_1000_XORArbiterPUF_inst)
    Test_2_on_20_100_XORArbiterPUF_inst = T2_sel_from_T2_bflip_r_inst(100, Test_2_on_20_1000_XORArbiterPUF_inst)

    Test_2_on_10_10_FFArbiterPUF_inst  = T2_sel_from_T2_bflip_r_inst(10, Test_2_on_10_1000_FFArbiterPUF_inst)
    Test_2_on_10_100_FFArbiterPUF_inst = T2_sel_from_T2_bflip_r_inst(100, Test_2_on_10_1000_FFArbiterPUF_inst)

    Test_2_on_20_10_XORBistableRingPUF_inst  = T2_sel_from_T2_bflip_r_inst(10, Test_2_on_20_1000_XORBistableRingPUF_inst)
    Test_2_on_20_100_XORBistableRingPUF_inst = T2_sel_from_T2_bflip_r_inst(100, Test_2_on_20_1000_XORBistableRingPUF_inst)

    
    """ Set the parameters for the plots
        img_counter    : track order of plots
        sig_fig        : number of significant figures shown
        glob_font_size : standard font size
    """
    
    img_counter     = 1
    sig_fig         = 3
    glob_font_size  = 14
    
    
    
    """ Arbiter PUF """    
    
    """ Plot S_j dependent on j for 8 instances from file Test_2_on_0008_ArbiterPUF_inst.
        Add legend with I2O scores for the corresponding colours.
        Add \overline{I2O} score for the 8 instances.
    """
    
    """ Sort according to I2O scores """
    Test_2_on_0008_ArbiterPUF_inst_sorted = sort_T2_return_by_I2O(*Test_2_on_0008_ArbiterPUF_inst)
    
    """ Now select plot items and round \overline{I2O} to sig_fig. """
    lines    = Test_2_on_0008_ArbiterPUF_inst_sorted[0]
    i2o_vals = Test_2_on_0008_ArbiterPUF_inst_sorted[2]
    i2o_avgs = Test_2_on_0008_ArbiterPUF_inst_sorted[3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    """ Create the plot """
    fig_plot    = plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, ylim=ylim, n_cols=4, font_size=glob_font_size, quarter_yticks=True)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0008_ArbiterPUF_inst.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Plot box-plot of S_j for 100 Arbiter PUF instances dependent on j.
        Add \overline{I2O} score for the 100 instances.
    """
    # k=1, i.e. first subselection [0]
    S_j_bars    = Test_2_on_20_100_XORArbiterPUF_inst[0][1]
    S_js        = np.transpose(np.concatenate([Test_2_on_20_100_XORArbiterPUF_inst[0][0]], axis=1))
    i2o_avg     = Test_2_on_20_100_XORArbiterPUF_inst[0][3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    fig_plot    = plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, leg2_pos="upper left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True, bbox_val=(.0,.88), S_j_bars=S_j_bars)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_ArbiterPUF_inst_box.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ 2-XOR Arbiter PUF """
    
    """ Select 8 suitable 2-XOR Arbiter PUF instances to plot """
    # k=2, i.e. first subselection [1]
    Test_2_on_0008_2XORArbiterPUF_inst = Test_2_on_20_100_XORArbiterPUF_inst[1]
    
    lines    = Test_2_on_0008_2XORArbiterPUF_inst[0][:8]
    i2o_vals = Test_2_on_0008_2XORArbiterPUF_inst[2][:8]
    i2o_avgs = np.average(i2o_vals) 
    
    """ Order the selection according to descending I2O_1 scores """
    sorted_list_vals = sorted(zip(lines, i2o_vals), key = lambda x: x[1], reverse=True)
    lines            = [line for line, _   in sorted_list_vals]
    i2o_vals         = [val  for _,    val in sorted_list_vals]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    """ Create the plot """
    fig_plot    = plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, leg1_pos="upper left", leg2_pos="center left", ylim=ylim, n_cols=4, font_size=glob_font_size, quarter_yticks=True)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0008_2XORArbiterPUF_inst.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1


    """ Plot box-plot of S_j for 100 2-XOR Arbiter PUF instances dependent on j. """
    # k=2, i.e. first subselection [1]
    S_j_bars    = Test_2_on_20_100_XORArbiterPUF_inst[1][1]
    S_js        = np.transpose(np.concatenate([Test_2_on_20_100_XORArbiterPUF_inst[1][0]], axis=1))
    i2o_avg     = Test_2_on_20_100_XORArbiterPUF_inst[1][3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    fig_plot    = plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, leg2_pos="upper left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True, bbox_val=(.0,.88), S_j_bars=S_j_bars)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_2XORArbiterPUF_inst_box.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ 3-XOR Arbiter PUF """
    
    """ Select 8 suitable 3-XOR Arbiter PUF instances to plot """
    # k=3, i.e. first subselection [2]
    Test_2_on_0008_3XORArbiterPUF_inst = Test_2_on_20_100_XORArbiterPUF_inst[2]
    
    lines    = Test_2_on_0008_3XORArbiterPUF_inst[0][:8]
    i2o_vals = Test_2_on_0008_3XORArbiterPUF_inst[2][:8]
    i2o_avgs = np.average(i2o_vals) 
    
    """ Order the selection according to descending I2O_1 scores """
    sorted_list_vals = sorted(zip(lines, i2o_vals), key = lambda x: x[1], reverse=True)
    lines            = [line for line, _   in sorted_list_vals]
    i2o_vals         = [val  for _,    val in sorted_list_vals]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    """ Create the plot """
    fig_plot    = plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, leg1_pos="upper left", leg2_pos="center left", ylim=ylim, n_cols=4, font_size=glob_font_size, quarter_yticks=True)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0008_3XORArbiterPUF_inst.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Plot box-plot of S_j for 100 3-XOR Arbiter PUF instances dependent on j. """
    # k=3, i.e. first subselection [2]
    S_j_bars    = Test_2_on_20_100_XORArbiterPUF_inst[2][1]
    S_js        = np.transpose(np.concatenate([Test_2_on_20_100_XORArbiterPUF_inst[2][0]], axis=1))
    i2o_avg     = Test_2_on_20_100_XORArbiterPUF_inst[2][3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    fig_plot    = plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, leg2_pos="upper left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True, bbox_val=(.0,.88), S_j_bars=S_j_bars)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_3XORArbiterPUF_inst_box.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Plot of descending I2O_1 scores of 100 k-XOR Arbiter PUF instances for selected values of k
    """
    
    """ Order by descending I2O_1 socres and select ks """
    Test_2_on_20_100_XORArbiterPUF_inst_sorted = [sort_T2_return_by_I2O(*ele, order='decreasing') for ele in Test_2_on_20_100_XORArbiterPUF_inst]
    # selection for k = 1, 2, 3, 5, 8, 12
    selection = [0, 1, 2, 4, 7, 11]
    
    lines = []
    for i in selection:
        lines.append(Test_2_on_20_100_XORArbiterPUF_inst_sorted[i][2])
    
    lines_desc = []
    for i, val in enumerate(selection):
        if 3 < i < 5:
            lines_desc.append(r'$k = \phantom{0}$' + r'${}$'.format(val+1))
        else:
            lines_desc.append(r'$k = {}$'.format(val+1))
    
    pos_high = (64,70)
    pos_low  = (-64,75)
    annot_high = r'\begin{tabular}{l} $\mathrm{Largest} \; {\sf  I2O_{1}} \: \mathrm{Score}$ \\ $\mathrm{of} \; \mathrm{all} \; 100 \; \mathrm{instances} $  \end{tabular}'
    annot_low  = r'\begin{tabular}{l} $\mathrm{Smallest} \; {\sf  I2O_{1}} \: \mathrm{Score}$ \\ $\mathrm{of} \; \mathrm{all} \; 100 \; \mathrm{instances} $  \end{tabular}'
    
    ylim = (-0.02, .522680407)
    
    fig_plot    = plot_inst_merit_desc_mult(lines, lines_desc, annot_high, annot_low, pos_high, pos_low, leg1_pos='upper right', ylim=ylim, n_cols=3, box_back=['#fcfcfc'])
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_kXORArbiterPUF_inst_I2O_dot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ FF Arbiter PUF """    
    
    """ Define the loop structure used for the simulation """
    feed_forwards = [(6, 15), (14, 23), (22, 31), (30, 39), (38,47), (46, 55), (54, 63), (62, 71)]
    
    """ Plot S_j dependent on j for 8 instances from file Test_2_on_0008_FFArbiterPUF_inst.
        Add legend with I2O scores for the corresponding colours.
        Add \overline{I2O} score for the 8 instances.
        Add vertical lines at the starting positions of the loops
            (in challenge bit representation - NOT stage representation!)
    """
    
    """ Sort according to I2O scores """
    Test_2_on_0008_FFArbiterPUF_inst = sort_T2_return_by_I2O(*Test_2_on_0008_FFArbiterPUF_inst)
    
    """ Now select plot items and round \overline{I2O} to 5 sig_fig. """
    lines    = Test_2_on_0008_FFArbiterPUF_inst[0]
    i2o_vals = Test_2_on_0008_FFArbiterPUF_inst[2]
    i2o_avgs = Test_2_on_0008_FFArbiterPUF_inst[3]
    
    ylim = (-0.04809600000000001, 1.120396)
    
    """ Create the plot """
    fig_plot    = plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, leg2_pos=6, feed_forwards=feed_forwards, ylim=ylim, n_cols=4, font_size=glob_font_size, quarter_yticks=True, bbox_leg_1_val=(-0.00,1), bbox_leg_2_val=(-0.00,.665), alpha=.3)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0008_FFArbiterPUF_inst.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    
    img_counter += 1
    
    
    """ Plot box-plot of S_j for 100 FF Arbiter PUF instances with l=8 dependent on j.
    """
    Test_2_on_10_100_FFArbiterPUF_inst[7][0]
    # l=8, i.e. first subselection [7]
    S_j_bars    = Test_2_on_10_100_FFArbiterPUF_inst[7][1]
    S_js        = np.transpose(np.concatenate([Test_2_on_10_100_FFArbiterPUF_inst[7][0]], axis=1))
    i2o_avg     = Test_2_on_10_100_FFArbiterPUF_inst[7][3]
    
    ylim = (-0.04809600000000001, 1.120396)
    
    fig_plot    = plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, feed_forwards=feed_forwards, leg2_pos="upper left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True, bbox_val=(.0,.88), S_j_bars=S_j_bars)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_FFArbiterPUF_inst_box.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Plot of descending I2O_1 scores of 100 l-loop FF Arbiter PUF instances for selected values of l
    """
    
    """ Order by descending I2O_1 socres and select ls """
    Test_2_on_12_100_FFArbiterPUF_inst_sorted = [sort_T2_return_by_I2O(*ele, order='decreasing') for ele in Test_2_on_10_100_FFArbiterPUF_inst]
    # selection for l = 3, 4, 5, 8
    selection = [2, 3, 4, 7]
    
    lines = []
    for i in selection:
        lines.append(Test_2_on_12_100_FFArbiterPUF_inst_sorted[i][2])
    
    lines_desc = []
    for _, val in enumerate(selection):
        lines_desc.append(r'$l = {}$'.format(val+1))
    
    pos_high = (64,57)
    pos_low  = (-64,-48)
    annot_high = r'\begin{tabular}{l} $\mathrm{Largest} \; {\sf  I2O_{1}} \: \mathrm{Score}$ \\ $\mathrm{of} \; \mathrm{all} \; 100 \; \mathrm{instances} $  \end{tabular}'
    annot_low  = r'\begin{tabular}{l} $\mathrm{Smallest} \; {\sf  I2O_{1}} \: \mathrm{Score}$ \\ $\mathrm{of} \; \mathrm{all} \; 100 \; \mathrm{instances} $  \end{tabular}'
    
    ylim = (-0.02, .522680407)
    
    fig_plot    = plot_inst_merit_desc_mult(lines, lines_desc, annot_high, annot_low, pos_high, pos_low, leg1_pos='upper right', ylim=ylim, n_cols=2, box_back=['#fcfcfc'], ff_special_col=True)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_lLoopFFArbiterPUFs_inst_dot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Bistable Ring PUF """    
    
    """ Plot S_j dependent on j for 8 instances from file Test_2_on_0006_BistableRingPUF_inst.
        Add legend with I2O scores for the corresponding colours.
        Add \overline{I2O} score for the 8 instances.
    """
    
    """ Sort according to I2O scores """
    Test_2_on_0006_BistableRingPUF_inst = sort_T2_return_by_I2O(*Test_2_on_0006_BistableRingPUF_inst)
    
    """ Now select plot items and round \overline{I2O} to sig_fig. """
    lines    = Test_2_on_0006_BistableRingPUF_inst[0]
    i2o_vals = Test_2_on_0006_BistableRingPUF_inst[2]
    i2o_avgs = Test_2_on_0006_BistableRingPUF_inst[3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    """ Create the plot """
    fig_plot    = plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, leg1_pos="upper left", leg2_pos="center left", ylim=ylim, n_cols=3, font_size=glob_font_size, quarter_yticks=True)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0006_BistableRingPUF_inst.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Plot box-plot of S_j for 100 Bistable Ring PUF instances dependent on j.
        Add \overline{I2O} score for the 100 instances.
    """
    # k=1, i.e. first subselection [0]
    S_j_bars    = Test_2_on_20_100_XORBistableRingPUF_inst[0][1]
    S_js        = np.transpose(np.concatenate([Test_2_on_20_100_XORBistableRingPUF_inst[0][0]], axis=1))
    i2o_avg     = Test_2_on_20_100_XORBistableRingPUF_inst[0][3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    fig_plot    = plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, leg2_pos="upper left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True, bbox_val=(.0,.88), S_j_bars=S_j_bars)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_BistableRingPUF_inst_box.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ 4-XOR Bistable Ring PUF """
    
    """ Select 6 suitable 4-XOR Bistable Ring instances to plot """
    # k=4, i.e. first subselection [3]
    Test_2_on_0006_4XORBistableRingPUF_inst = Test_2_on_20_100_XORBistableRingPUF_inst[3]
    
    lines    = Test_2_on_0006_4XORBistableRingPUF_inst[0][:6]
    i2o_vals = Test_2_on_0006_4XORBistableRingPUF_inst[2][:6]
    i2o_avgs = np.average(i2o_vals) 
    
    """ Order the selection according to descending I2O_1 scores """
    sorted_list_vals = sorted(zip(lines, i2o_vals), key = lambda x: x[1], reverse=True)
    lines            = [line for line, _   in sorted_list_vals]
    i2o_vals         = [val  for _,    val in sorted_list_vals]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    """ Create the plot """
    fig_plot    = plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, leg1_pos="upper left", leg2_pos="center left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0006_4XORBistableRingPUF_inst.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Plot box-plot of S_j for 100 4-XOR Bistable Ring PUF instances dependent on j. """
    # k=4, i.e. first subselection [3]
    S_j_bars    = Test_2_on_20_100_XORBistableRingPUF_inst[3][1]
    S_js        = np.transpose(np.concatenate([Test_2_on_20_100_XORBistableRingPUF_inst[3][0]], axis=1))
    i2o_avg     = Test_2_on_20_100_XORBistableRingPUF_inst[3][3]
    
    ylim = (-0.04809600000000001, 1.049396)
    
    fig_plot    = plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, leg2_pos="upper left", ylim=ylim, font_size=glob_font_size, quarter_yticks=True, bbox_val=(.0,.88), S_j_bars=S_j_bars)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_4XORBistableRingPUF_inst_box.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    """ Plot of descending I2O_1 scores of 100 k-XOR Bistable Ring PUF instances for selected values of k
    """
    
    """ Order by descending I2O_1 socres and select ks """
    Test_2_on_20_100_XORBistableRingPUF_inst_sorted = [sort_T2_return_by_I2O(*ele, order='decreasing') for ele in Test_2_on_20_100_XORBistableRingPUF_inst]
    # selection for k = 1, 2, 3, 5, 8, 12
    selection = [0, 1, 2, 4, 7, 11]
    
    lines = []
    for i in selection:
        lines.append(Test_2_on_20_100_XORBistableRingPUF_inst_sorted[i][2])
    
    lines_desc = []
    for i, val in enumerate(selection):
        if 3 < i < 5:
            lines_desc.append(r'$k = \phantom{0}$' + r'${}$'.format(val+1))
        else:
            lines_desc.append(r'$k = {}$'.format(val+1))
    
    pos_high = (64,21)
    pos_low  = (-64,-187)
    annot_high = r'\begin{tabular}{l} $\mathrm{Largest} \; {\sf  I2O_{1}} \: \mathrm{Score}$ \\ $\mathrm{of} \; \mathrm{all} \; 100 \; \mathrm{instances} $  \end{tabular}'
    annot_low  = r'\begin{tabular}{l} $\mathrm{Smallest} \; {\sf  I2O_{1}} \: \mathrm{Score}$ \\ $\mathrm{of} \; \mathrm{all} \; 100 \; \mathrm{instances} $  \end{tabular}'
    
    ylim = (-0.07, .578180407)
    
    fig_plot    = plot_inst_merit_desc_mult(lines, lines_desc, annot_high, annot_low, pos_high, pos_low, leg1_pos='upper right', ylim=ylim, n_cols=3, box_back=['#fcfcfc'], font_size=13)
    fig_plot.savefig(sub_dir_plots + '{:02d}'.format(img_counter) + '_Test_2_on_0100_kXORBistableRingPUF_inst_I2O_dot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    img_counter += 1
    
    
    """ Produce \overline{I2O}_1 values used in the tables and write them to .txt files in the plot folder """

    
    """ k-XOR Arbiter PUF """
    
    kXORArbiterPUF_I2O_List = []
    for k in range(20):
        kXORArbiterPUF_I2O_List.append([f'{k+1:2d}', f'{Test_2_on_20_10_XORArbiterPUF_inst[k][3]:.5f}', 
                                        f'{Test_2_on_20_100_XORArbiterPUF_inst[k][3]:.5f}', 
                                        f'{Test_2_on_20_1000_XORArbiterPUF_inst[k][3]:.5f}']
                                       )
    kXORArbiter_I2O_table = tabulate(kXORArbiterPUF_I2O_List, headers=['k', '10_inst_I2O', '100_inst_I2O', '1000_inst_I2O'], tablefmt='psql', floatfmt=".5f")
    
    with open(sub_dir_plots + '{:02d}'.format(img_counter) + '_I2O_Values_kXORArbiterPUF.txt', 'wb') as target_file:
        target_file.write(kXORArbiter_I2O_table.encode('utf-8'))
    
    img_counter += 1

    
    """ l Loop FF Arbiter PUF """

    lLoopFFARbiterPUF_I2O_List = []
    for k in range(10):
        lLoopFFARbiterPUF_I2O_List.append([f'{k+1:2d}', f'{Test_2_on_10_10_FFArbiterPUF_inst[k][3]:.5f}', 
                                           f'{Test_2_on_10_100_FFArbiterPUF_inst[k][3]:.5f}', 
                                           f'{Test_2_on_10_1000_FFArbiterPUF_inst[k][3]:.5f}']
                                          )
    lLoopFFArbiter_I2O_table = tabulate(lLoopFFARbiterPUF_I2O_List, headers=['k', '10_inst_I2O', '100_inst_I2O', '1000_inst_I2O'], tablefmt='psql', floatfmt=".5f")
    
    with open(sub_dir_plots + '{:02d}'.format(img_counter) + '_I2O_Values_lLoopFFArbiterPUF.txt', 'wb') as target_file:
        target_file.write(lLoopFFArbiter_I2O_table.encode('utf-8'))
    
    img_counter += 1
    
    
    """ k-XOR Bistable Ring PUF """

    kXORBistableRingPUF_I2O_List = []
    for k in range(20):
        kXORBistableRingPUF_I2O_List.append([f'{k+1:2d}', f'{Test_2_on_20_10_XORBistableRingPUF_inst[k][3]:.5f}', 
                                             f'{Test_2_on_20_100_XORBistableRingPUF_inst[k][3]:.5f}', 
                                             f'{Test_2_on_20_1000_XORBistableRingPUF_inst[k][3]:.5f}']
                                            )
    kXORArbiter_I2O_table = tabulate(kXORBistableRingPUF_I2O_List, headers=['k', '10_inst_I2O', '100_inst_I2O', '1000_inst_I2O'], tablefmt='psql', floatfmt=".5f")
    
    with open(sub_dir_plots + '{:02d}'.format(img_counter) + '_I2O_Values_kXORBistableRingPUF.txt', 'wb') as target_file:
        target_file.write(kXORArbiter_I2O_table.encode('utf-8'))
    
    img_counter += 1

