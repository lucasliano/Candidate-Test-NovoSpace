from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from random import randrange

from bitstring import BitArray

def toCA2(arg, K):      # TODO
    '''
    Function Description
    ------------------
    It takes an N-bit uint as an input and outputs the (K)-bit int.

    Parameters
    ----------
    arg : int
        Target number.

    K : int
        K = N - 1.

    '''

    return BitArray(int=arg, length=K).int



if __name__ == '__main__':
    N = 4   # Numero de bits
    a = -8   # Valor a Evaluar
    b = toCA2(a,N+1)

    print(b)
