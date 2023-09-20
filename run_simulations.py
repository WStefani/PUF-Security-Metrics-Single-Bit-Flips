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

from aux_funcs.simulation_funcs import T2_1_bflip_r_inst, produce_loop_structure

import argparse
import pickle
import joblib
from pathlib import Path
from functools import partial

from numpy.random import default_rng

from pypuf.simulation import XORArbiterPUF, FeedForwardArbiterPUF, XORBistableRingPUF
from pypuf.io import random_inputs

sub_dir_simulation  = './simulations/'
Path(sub_dir_simulation).mkdir(parents=True, exist_ok=True)

# Get no. of cores available:
no_cpu = joblib.cpu_count()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Default: Use all cores for simulation
    parser.add_argument('--cpus', default=max(1,no_cpu), type=int, choices=range(1, no_cpu+1))
    # Default: Use 10^5 challenges
    parser.add_argument('--challenges', default=100000, type=int)

    args = parser.parse_args()
    parallel_jobs = args.cpus
    no_challenges = args.challenges

    """ Choose challenge length 64 and create the challenges. """
    n_bits = 64
    # Use seed for challenge creation
    Challenges_C = random_inputs(n=n_bits, N=no_challenges, seed=1)
    
    """ The first three simulations are expected to be fast, while the
        last three are rather extensive - they will be used to create
        smaller subsets of simulations for the graphics shown in the paper.
    """
    
    
    """ #01 Test 2 on 8 ArbiterPUF instances """
    r = 8
    # Use Partial to later only adapt ArbiterPUF
    Puf_Func = partial(XORArbiterPUF, n=n_bits, k=1, noisiness=0)
    
    # Use seed to allow for reproducibility
    instances = [Puf_Func(seed=i) for i in range(r)]
    
    Test_2_on_0008_ArbiterPUF_inst = T2_1_bflip_r_inst(instances, Challenges_C, parallel_jobs)
    
    with open(sub_dir_simulation + 'Test_2_on_0008_ArbiterPUF_inst', 'wb') as target_file:
        pickle.dump(Test_2_on_0008_ArbiterPUF_inst, target_file)


    """ #02 Test 2 on 8 FFArbiterPUF instances """
    r = 8
    # Use Partial to later only adapt FFArbiterPUF
    feed_forwards = [(6, 15), (14, 23), (22, 31), (30, 39), (38,47), (46, 55), (54, 63), (62, 71)]
    Puf_Func = partial(FeedForwardArbiterPUF, n=n_bits, ff=feed_forwards, noisiness=0)
    
    # Use seed to allow for reproducibility
    instances = [Puf_Func(seed=i) for i in range(r)]
    
    Test_2_on_0008_FFArbiterPUF_inst = T2_1_bflip_r_inst(instances, Challenges_C, parallel_jobs)
    
    with open(sub_dir_simulation + 'Test_2_on_0008_FFArbiterPUF_inst', 'wb') as target_file:
        pickle.dump(Test_2_on_0008_FFArbiterPUF_inst, target_file)


    """ #03 Test 2 on 6 BistableRingPUF instances """
    r = 6
    # Use Partial to later only adapt BistableRingPUF
    Puf_Func = partial(XORBistableRingPUF, n=n_bits, k=1)
    
    # Use seed to allow for reproducibility
    instances = [Puf_Func(weights=default_rng(i).normal(size=(1, n_bits+1))) for i in range(r)]

    Test_2_on_0006_BistableRingPUF_inst = T2_1_bflip_r_inst(instances, Challenges_C, parallel_jobs)
    
    with open(sub_dir_simulation + 'Test_2_on_0006_BistableRingPUF_inst', 'wb') as target_file:
        pickle.dump(Test_2_on_0006_BistableRingPUF_inst, target_file)
    
    
    """ #04 Test 2 on 20*1000 k-XORArbiterPUF instances """
    r = 1000
    # Use Partial to later only adapt further properties
    Puf_Func = partial(XORArbiterPUF, n=n_bits, noisiness=0)
    
    """ Create a list of lists of instances. Outer list indexed by k,
        inner contains the results for the r=1000 instances.
    """
    instances_in_k = [[Puf_Func(k=k, seed=i) for i in range(r)] for k in range(1,20+1)]

    Test_2_on_20_1000_XORArbiterPUF_inst = []
    for _, instances in enumerate(instances_in_k):
        Test_2_on_20_1000_XORArbiterPUF_inst.append(T2_1_bflip_r_inst(instances, Challenges_C, parallel_jobs))
    
    with open(sub_dir_simulation + 'Test_2_on_20_1000_XORArbiterPUF_inst', 'wb') as target_file:
        pickle.dump(Test_2_on_20_1000_XORArbiterPUF_inst, target_file)
    
    
    """ #05 Test 2 on 12*1000 FFArbiterPUF instances with different loop_structure"""
    r = 1000
    """ For the above example with loop structure
        feed_forwards = [(6, 15), (14, 23), (22, 31), (30, 39), (38,47), (46, 55), (54, 63), (62, 71)]
        the last loop determines stage 72, hence it ends after 71.
        
        Since all loops are required to have the same length, the length of the last loop determines the length.
        
        All previous loops are required to overlap with their respective next loop by 1.
        
        Hence we provide a tuple comprising of the last loop and the number of loops in total in last_loops_no below.
        
        From these we construct the individual loop structures examined using the produce_loop_structure function.
    """
    last_loops_no = [((65,73),10), ((64,72),9), ((62,71),8), ((60,70),7), ((57,69),6), ((54,68),5), ((50,67),4), ((44,66),3), ((33,65),2), ((2,64),1)]
    last_loops_no.reverse()
    
    loops_in_l = [produce_loop_structure(ele) for ele in last_loops_no]
    
    """ Create a list of lists of instances. Outer list indexed by l, starting with 1,
        inner contains the r=1000 instances.
    """
    instances_in_l = []
    for l in range(len(loops_in_l)):
        feed_forwards   = loops_in_l[l]
        # Use Partial to later only adapt further properties
        Puf_Func        = partial(FeedForwardArbiterPUF, n=n_bits, ff=feed_forwards, noisiness=0)
        instances       = [Puf_Func(seed=i) for i in range(r)]
        
        instances_in_l.append(instances)

    Test_2_on_10_1000_FFArbiterPUF_inst = []
    for _, instances in enumerate(instances_in_l):
        Test_2_on_10_1000_FFArbiterPUF_inst.append(T2_1_bflip_r_inst(instances, Challenges_C, parallel_jobs))
    
    with open(sub_dir_simulation + 'Test_2_on_10_1000_FFArbiterPUF_inst', 'wb') as target_file:
        pickle.dump(Test_2_on_10_1000_FFArbiterPUF_inst, target_file)
    
    
    """ #06 Test 2 on 20*1000 k-XORBistableRingPUF instances """
    r = 1000
    # Use Partial to later only adapt further properties
    Puf_Func = partial(XORBistableRingPUF, n=n_bits)

    """ Create a list of lists of instances. Outer list indexes by k,
        inner contains the r=1000 instances.
    """
    instances_in_k = [[Puf_Func(k=k, weights=default_rng(i).normal(size=(k, n_bits+1))) for i in range((k-1)*r,k*r)] for k in range(1,20+1)]

    Test_2_on_20_1000_XORBistableRingPUF_inst = []
    for _, instances in enumerate(instances_in_k):
        Test_2_on_20_1000_XORBistableRingPUF_inst.append(T2_1_bflip_r_inst(instances, Challenges_C, parallel_jobs))
    
    with open(sub_dir_simulation + 'Test_2_on_20_1000_XORBistableRingPUF_inst', 'wb') as target_file:
        pickle.dump(Test_2_on_20_1000_XORBistableRingPUF_inst, target_file)

