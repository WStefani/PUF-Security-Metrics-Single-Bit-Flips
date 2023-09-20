#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import numpy as np

from collections import Counter
from joblib import Parallel, delayed


""" Functions to implement Tests 1 and 2
"""


def det_no_resp_flips(puf_instance, responses, challenges, flip_pos):
    """ Function to determine how many response bits are flipped when the challenge
        bits at the positions in flip_pos are flipped
        
        puf_instance:   puf object      - from pypuf
        responses:      numpy.ndarray   - initial evaluation results
        challenges:     numpy.ndarray   - all initial challenges (e.g. generated with pypuf.io.random_inputs)
        flip_pos:       list of int     - positions of bits to be flipped (may include mulitples of the same position)
        
        no_resp_flips:  int             - number of flipped responses obtained with flipped challenges
    """

    challenges_flipped = copy.copy(challenges)
    
    """ Account for the possibility of multiple flips at the same position """
    if len(flip_pos) == len(np.unique(flip_pos)):
        challenges_flipped[:,flip_pos] = challenges_flipped[:,flip_pos] * (-1)
    else:
        """ Remove even number of flips from the flip_pos list, retain uneven ones. """
        flip_pos_counts = Counter(flip_pos)
        flip_pos_rem    = [flip for flip, count in flip_pos_counts.items() if count%2 != 0]
        
        challenges_flipped[:,flip_pos_rem] = challenges_flipped[:,flip_pos_rem] * (-1)
    
    responses_flipped = puf_instance.eval(challenges_flipped)
    
    """ Compare responses and responses_flipped elementwise:
        1 * 1 = (-1) * (-1) = 1, i.e. no flip results in 1,
        while 1 * (-1) = (-1) * 1 = -1, i.e. flips are -1.
        Subtract 1, then divide by -2, hence the resulting array has
        entries 0 for no flips and 1 if there is a flip in the response.
    """    
    resp_diffs = responses * responses_flipped
    resp_diffs = (resp_diffs - 1) / (-2)
    
    no_resp_flips = np.sum(resp_diffs)
    
    return no_resp_flips


def T1_1_bflip_1_inst(puf_instance, challenges):
    """ Function to implement Test 1

        puf_instance:   puf object      - from pypuf
        challenges:     numpy.ndarray   - all initial challenges (e.g. generated with pypuf.io.random_inputs)
        
        S_i_arr:        numpy.ndarray   - estimated n S_j(P)s from Test 1
        I2O_1:          float           - estimated I2O_1(P) from Test 1
    """

    no_bits = puf_instance.challenge_length
    no_Cs   = challenges.shape[0]
    
    responses = puf_instance.eval(challenges)
    
    S_i     = [det_no_resp_flips(puf_instance, responses, challenges, [i]) for i in range(no_bits)]
    S_i_arr = np.asarray(S_i) / no_Cs
    
    I2O_1   = np.average(np.abs(S_i_arr - 0.5))
    
    return S_i_arr, I2O_1


def T2_1_bflip_r_inst(instances, challenges, n_jobs=1):
    """ Function to implement Test 2

        instances:      list of puf objects - from pypuf
        challenges:     numpy.ndarray       - all initial challenges (e.g. generated with pypuf.io.random_inputs)
        n_jobs:         int                 - no. of cores used (parallel evaluation of instances)
        
        S_i_r:          list of arrays      - estimated r*n S_j(P_k)s from Test 1 for P_ks (list pos. 1 <= k <= r, array pos 1 <= j <= n)
        S_i_avg:        numpy.ndarray       - estimated n \overline{S}_js from Test 2
        I2O_1_r:        list of float       - estimated r I2O_1(P_k) from Test 1 for P_ks
        I2O_1_avg:      float               - estimated \overline{I2O}_1 from Test 2
        A2O_1:          float               - estimated A2O_1 from Test 2
    """
    
    r = len(instances)
    
    instances_T1 = Parallel(n_jobs=n_jobs)(delayed(T1_1_bflip_1_inst)(instance, challenges) for instance in instances)
    
    S_i_r   = [S_i_arr for S_i_arr, I2O_1 in instances_T1]
    S_i_avg = np.sum(S_i_r, axis=0) / r
    
    I2O_1_r     = [I2O_1 for S_i_arr, I2O_1 in instances_T1]
    I2O_1_avg   = np.sum(I2O_1_r) / r
    
    A2O_1 = np.average(np.abs(S_i_avg - 0.5))
    
    return S_i_r, S_i_avg, I2O_1_r, I2O_1_avg, A2O_1


def sort_T2_return_by_I2O(S_i_r, S_i_avg, I2O_1_r, I2O_1_avg, A2O_1, order='decreasing'):
    """ Function to sort return of Test 2 by I2O scores

        Test_2_on_r_inst:   tuple of T2_1_bflip_r_inst return - only [0, 2] relevant for sorting
                            [0 - flips of PUF instances, 2 - I2O_1 scores, cf. T2_1_bflip_r_inst above]
        order:              string - either 'increasing' or 'decreasing' determining the sort order
        
        Test_2_on_r_inst:   reordered return of T2_1_bflip_r_inst
    """
    
    if order == 'increasing':
        I2O_order = [i for i, i2o in sorted(enumerate(I2O_1_r), key=lambda x:x[1])]
    elif order == 'decreasing':
        I2O_order = [i for i, i2o in sorted(enumerate(I2O_1_r), key=lambda x:x[1])]
        I2O_order = list(reversed(I2O_order))
        
    S_i_r   = [S_i_r[i] for i in I2O_order]
    I2O_1_r = [I2O_1_r[i] for i in I2O_order]
    
    return S_i_r, S_i_avg, I2O_1_r, I2O_1_avg, A2O_1


def T2_sel_from_T2_bflip_r_inst(n, Test_2_m_insts):
    """ Function to reduce the elements in the list iterating over k or l for 
        k-XORArbiter/k-XORBistableRing PUFs or l Loop FF Arbiter PUFs from their total
        number of instances to n instances.
        
        n:                  int             - Number of instances (must be <= #instances for each k/l parameter)
        Test_2_m_insts:     list of tuples  - list in k/l of tuples from Test 2 results - Return from T2_1_bflip_r_inst
        
        sel_Test_2_m_insts: list of tuples  - list in k/l of tuples from Test 2 results - Return from T2_1_bflip_r_inst
    """
    
    sel_Test_2_m_insts = []
    for k, Test_2_insts in enumerate(Test_2_m_insts):
        S_i_r = Test_2_insts[0][:n]
        S_i_avg = np.sum(S_i_r, axis=0) / n
        
        I2O_1_r     = Test_2_insts[2][:n]
        I2O_1_avg   = np.sum(I2O_1_r) / n
        
        A2O_1 = np.average(np.abs(S_i_avg - 0.5))
        
        sel_Test_2_m_insts.append(tuple([S_i_r, S_i_avg, I2O_1_r, I2O_1_avg, A2O_1]))
    
    return sel_Test_2_m_insts


def produce_loop_structure(last_loop_no_tup):
    """ Function to produce a list respresenting the FF Arbiter PUF loop structure
        
        last_loop_no_tup:   tuple           - of type ((a,b), n) with (a,b) the loop and n number of loops
        
        loops:              list of tuples  - list to represent the loop structure
    """

    loops       = []
    last_loop   = last_loop_no_tup[0]
    
    loops.append(last_loop)
    
    dist        = last_loop[1]-last_loop[0]
    
    prev_loop   = last_loop
    for i in range(last_loop_no_tup[1]-1):
        prev_loop = (prev_loop[0]-dist+1, prev_loop[0]+1)
        loops.append(prev_loop)
    
    loops.reverse()
    
    return loops

