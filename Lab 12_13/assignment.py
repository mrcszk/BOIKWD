from __future__ import annotations
import ahp
from dataclasses import dataclass
import numpy as np
from typing import Tuple


@dataclass
class RankingSolution:
    rankings: Tuple[np.Array]
    preference_ranking: np.Array
    global_ranking: np.Array
    choice: int

@dataclass
class ConsistencySolution:
    saaty: float 
    koczkodaj: float

def ranking_assignment():
    Cs = (
        ahp.read_comparison_matrix("1/7,1/5;3"),
        ahp.read_comparison_matrix("5,9;4"),
        ahp.read_comparison_matrix("4,1/5;1/9"),
        ahp.read_comparison_matrix("9,4;1/4"),
        ahp.read_comparison_matrix("1,1;1"),
        ahp.read_comparison_matrix("6,4;1/3"),
        ahp.read_comparison_matrix("9,6;1/3"),
        ahp.read_comparison_matrix("1/2,1/2;1")
    )
    c_p = ahp.read_comparison_matrix("4,7,5,8,6,6,2;5,3,7,6,6,1/3;1/3,5,3,3,1/5;6,3,4,1/2;1/3,1/4,1/7;1/2,1/5;1/5")

    evm_rankings = []
    for c in Cs:
        evm_rankings.append(ahp.evm(c))
    evm_p_ranking = ahp.evm(c_p)
    evm_global_ranking = [0, 0, 0]
    for h in range(len(evm_global_ranking)):
        for i in range(0, len(evm_rankings)):
            evm_global_ranking[h] += evm_rankings[i][h] * evm_p_ranking[i]
    evm_choice = int(np.argmax(evm_global_ranking))
    evm_solution = RankingSolution(evm_rankings, evm_p_ranking, evm_global_ranking, evm_choice)
    
    gmm_rankings = []
    for c in Cs:
        gmm_rankings.append(ahp.gmm(c))
    gmm_p_ranking = ahp.gmm(c_p)
    gmm_global_ranking  = [0, 0, 0]
    for h in range(len(gmm_global_ranking)):
        for i in range(0, len(gmm_rankings)):
            gmm_global_ranking[h] += gmm_rankings[i][h] * gmm_p_ranking[i]
    gmm_choice = int(np.argmax(gmm_global_ranking))
    gmm_solution = RankingSolution(gmm_rankings, gmm_p_ranking, gmm_global_ranking, gmm_choice)

    return evm_solution, gmm_solution

def consistency_assignment():
    Cs = (
       ahp.read_comparison_matrix("7,3;2"),
       ahp.read_comparison_matrix("1/5,7,1;1/2,2;3"),
       ahp.read_comparison_matrix("2,5,1,7;3,1/2,5;1/5,2;7") 
    )

    saaty_indexes = []
    for c in Cs:
        saaty_indexes.append(ahp.saaty_index(c))

    koczkodaj_indexes = []
    for c in Cs:
        koczkodaj_indexes.append(ahp.koczkodaj_index(c))

    return (ConsistencySolution(s, k) for s,k in zip(saaty_indexes, koczkodaj_indexes))
