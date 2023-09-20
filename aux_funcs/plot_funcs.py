#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib as mpl
mpl.rcParams[r'text.usetex']            = True
mpl.rcParams[r'text.latex.preamble']    = r'\usepackage{amsmath} \usepackage{amssymb} \usepackage[utf8]{inputenc} \usepackage{multirow}' #for \text{} command
mpl.rcParams['legend.framealpha']       = 1
mpl.rcParams['legend.facecolor']        = '#fcfcfc'
glob_alpha                              = .3
mpl.rcParams['grid.alpha']              = glob_alpha


""" Functions to create the plots.
"""


""" Function to create plot of S_j depending on bit-flip position j.
"""
def plot_S_j_by_j(lines, i2o_vals, i2o_avgs, sig_fig, leg1_pos=2, leg2_pos=6, feed_forwards=[], xlim=(), ylim=(), n_cols=3, font_size=14, quarter_yticks=False, bbox_leg_1_val=(), bbox_leg_2_val=(0,0.665), alpha=glob_alpha):
    
    n_bits      = len(lines[0])
    no_lines    = len(lines)    
    color       = cm.turbo(np.linspace(0, 1, no_lines))
    
    string_round    = r'{:.' + str(sig_fig) + r'f}'
    i2o_vals = [r'$' + string_round.format(round(ele, sig_fig)) + '$' for ele in i2o_vals]
    i2o_avgs  = string_round.format(round(i2o_avgs, sig_fig))
    
    fig, ax = plt.subplots()
    
    if xlim != ():
        ax.set_xlim(xlim)
    
    if ylim != ():
        ax.set_ylim(ylim)
    
    ylim = ax.get_ylim()
    
    plot_lines = []
    # Add the r line plots
    for i, c in zip(range(no_lines), color):
        line, = ax.plot(range(1,n_bits+1), lines[i], c=c)    
        plot_lines.append([line])
    
    # Add the vertical lines at the start of the FF Arb loops
    for i, vline in enumerate(feed_forwards):
        lines_arr   = np.array(lines)
        if i<=1:
            y_max       = np.min(lines_arr[:, vline[0]-1])
            ax.vlines(x=(vline[0]),     ymax=y_max, ymin=ylim[0], linestyle='dashed', colors='slategrey', lw=1.5)
        else:
            y_max       = np.min(lines_arr[:, vline[0]-i+1-1])
            ax.vlines(x=(vline[0]-i+1), ymax=y_max, ymin=ylim[0], linestyle='dashed', colors='slategrey', lw=1.5)
        
    if bbox_leg_1_val != ():
        legend_1 = ax.legend([l[0] for l in plot_lines], i2o_vals, loc=leg1_pos, ncol=n_cols, title=r'${\sf I2O}_{1} \, \mathrm{Scores}$', title_fontsize=font_size, prop={'size': font_size}, columnspacing=.75, handletextpad=.5, handlelength=.7, bbox_to_anchor=bbox_leg_1_val)
    else:
        legend_1 = ax.legend([l[0] for l in plot_lines], i2o_vals, loc=leg1_pos, ncol=n_cols, title=r'${\sf I2O}_{1} \, \mathrm{Scores}$', title_fontsize=font_size, prop={'size': font_size}, columnspacing=.75, handletextpad=.5, handlelength=.7)
    
    rect        = mpl.patches.Rectangle((0,0), .001, .001, fill=False, edgecolor='none', visible=False)
    legend_2    = plt.legend([rect], [r'$\overline{\sf I2O}_{1} = ' + i2o_avgs + '$'], loc=leg2_pos, prop={'size': font_size}, borderpad=.4, handletextpad=0, handlelength=0, fancybox=True, bbox_to_anchor=bbox_leg_2_val)
    
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=13)
    
    ax.set_xlabel(r'$\mathrm{Bit \; Flip \; Position} \; j$', fontsize=font_size+1)
    ax.set_ylabel(r'$\mathrm{Response \; Flip \; Probability} \; S_j$', fontsize=font_size+1)
    
    ax.grid(True, alpha=alpha)
        
    ax.add_artist(legend_1)
    ax.add_artist(legend_2)
    
    if quarter_yticks:
        yticks = ax.get_yticks()
        yticks = np.array([yticks[0], yticks[-1]])
        yticks = np.append(yticks, np.array([0, .25, .5, .75, 1]))
        yticks = np.sort(yticks)
        ax.set_yticks(yticks[1:-1], fontsize=13)    
    
    return fig


""" Function to create box-plot of S_j depending on bit-flip position j.
"""
def plot_S_j_by_j_box(S_js, i2o_avg, sig_fig, feed_forwards=[], leg2_pos=6, xlim=(-2.15, 67.15), ylim=(), font_size=14, quarter_yticks=False, bbox_val=(.0,.665), S_j_bars=None):
    
    n_bits      = S_js.shape[0]
    
    labels_all  = [str(i) for i in range(n_bits)]
    
    string_round    = '{:.' + str(sig_fig) + 'f}'
    i2o_avg  = string_round.format(round(i2o_avg, sig_fig))
    
    fig, ax = plt.subplots()
    
    medianprops = dict(linestyle='-', linewidth=0, color='white')
    ax.boxplot(np.transpose(S_js), whis=[10,90], labels=labels_all, flierprops={'marker': 'o', 'markersize': 1, 'markerfacecolor': 'black'}, medianprops=medianprops)
    
    if ylim == ():
        ylim = ax.get_ylim()
    
    # Add the vertical lines at the start of the FF Arb loops
    for i, vline in enumerate(feed_forwards):
        S_js_trans  = np.array(S_js.T)
        if i<=1:
            y_max       = np.min(S_js_trans[:, vline[0]-1])
            ax.vlines(x=(vline[0]),     ymax=y_max, ymin=ylim[0], linestyle='dashed', colors='slategrey', lw=1.5)
        else:
            y_max       = np.min(S_js_trans[:, vline[0]-i+1-1])
            ax.vlines(x=(vline[0]-i+1), ymax=y_max, ymin=ylim[0], linestyle='dashed', colors='slategrey', lw=1.5)
    
    ax.set_ylim(ylim)
    
    if quarter_yticks:
        yticks = ax.get_yticks()
        yticks = np.array([yticks[0], yticks[-1]])
        yticks = np.append(yticks, np.array([0, .25, .5, .75, 1]))
        yticks = np.sort(yticks)
        ax.set_yticks(yticks[1:-1], fontsize=13)
    
    xticks_10 = [i for i in range(0,n_bits,10)]
    ax.set_xticks(xticks_10)
    ax.set_xticklabels(['$\\mathdefault{' + str(ele) + '}$' for ele in xticks_10])
    
    ax.set_xlim(xlim)
    
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=13)
    
    ax.set_xlabel(r'$\mathrm{Bit \; Flip \; Position} \; j$', fontsize=font_size+1)
    ax.set_ylabel(r'$\mathrm{Response \; Flip \; Probability} \; S_j$', fontsize=font_size+1)
    
    ax.grid(True)
    
    rect        = mpl.patches.Rectangle((0,0), .001, .001, fill=False, edgecolor='none', visible=False)
    legend_2    = ax.legend([rect], [r'$\overline{\sf I2O}_{1} = ' + i2o_avg + '$'], loc=leg2_pos, prop={'size': font_size}, borderpad=.4, handletextpad=0, handlelength=0, fancybox=True)
    
    ax.add_artist(legend_2)
    
    if not S_j_bars is None:
        color       = cm.turbo(np.linspace(0, 1, 16))
        color       = color[[2]]
        
        line, = ax.plot(range(1,n_bits+1), S_j_bars, c=color[0], linewidth=2.75)
        
        legend_3    = ax.legend([line], [r'$\overline{S}_j$'], loc=leg2_pos, prop={'size': font_size}, borderpad=.4, handletextpad=.5, handlelength=.7, fancybox=True, bbox_to_anchor=bbox_val)
        ax.add_artist(legend_3)        
    
    return fig


""" Function to create dot plot of multiple descending values of instance merit values.
"""
def plot_inst_merit_desc_mult(lines, lines_desc, annot_high=r'', annot_low=r'', pos_high=(0,0), pos_low=(0,0), con_style1='arc3,rad=0', con_style2='arc3,rad=0', leg1_pos="upper right", z_box='', font_size=14, ylim=(), box_back=['None'], alpha=glob_alpha, n_cols=1, bbox_val=(), ff_special_col=False, font_size_xy=14):
    
    n_inst  = len(lines[0])
    
    no_lines    = len(lines)    
    colors      = cm.turbo(np.linspace(0, 1, no_lines))
    color       = colors
    
    if ff_special_col:
        color       = cm.turbo(np.linspace(0, 1, 16))
        color       = color[[2,5,11,15]]
    
    fig, ax = plt.subplots()
    
    plot_lines = []
    # Add the r line scatter plots
    for i, c in zip(range(no_lines), color):
        line = ax.scatter(range(1,n_inst+1), lines[i], s=5.5, color=c)    
        plot_lines.append([line])
    
    fc = mpl.colors.to_rgba(box_back[0])[:-1] + (1.0,)
    ec = mpl.colors.to_rgba('None')[:-1] + (.3,)
    
    if annot_high != r'':
        ax.annotate(annot_high, fontsize=font_size, xy=(1, lines[0][0]),   xytext=pos_high, textcoords='offset points', ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc=fc, ec=ec), arrowprops=dict(arrowstyle='->', connectionstyle=con_style1, color='black'))
    if annot_low != r'':
        ax.annotate(annot_low,  fontsize=font_size, xy=(n_inst,lines[0][-1]), xytext=pos_low,  textcoords='offset points', ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.3', fc=fc, ec=ec), arrowprops=dict(arrowstyle='->', connectionstyle=con_style2, color='black'))
    
    if bbox_val != ():
        legend_1 = ax.legend([l[0] for l in plot_lines], lines_desc, loc=leg1_pos, ncol=n_cols, prop={'size': font_size}, columnspacing=.75, handletextpad=.5, handlelength=.7, bbox_to_anchor=bbox_val, markerscale=2)
    else:
        legend_1 = ax.legend([l[0] for l in plot_lines], lines_desc, loc=leg1_pos, ncol=n_cols, prop={'size': font_size}, columnspacing=.75, handletextpad=.5, handlelength=.7, markerscale=2)
    
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=13)
    
    ax.set_xlabel(r'$\mathrm{PUF \; Instance}$', fontsize=font_size_xy)
    ax.set_ylabel(r'${\sf I2O}_{1} \; \mathrm{Score}$', fontsize=font_size_xy)
    
    ax.grid(True, alpha=alpha)
    
    if ylim != ():
        ax.set_ylim(ylim)
    
    ax.add_artist(legend_1)
    
    return fig

