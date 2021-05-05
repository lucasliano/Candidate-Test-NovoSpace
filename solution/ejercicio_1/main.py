from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from random import getrandbits



class Stream(Record):
    def __init__(self, width, **kwargs):
        Record.__init__(self, [('data', width), ('valid', 1), ('ready', 1)], **kwargs)

    def accepted(self):
        return self.valid & self.ready

    class Driver:
        def __init__(self, clk, dut, prefix):
            self.clk = clk
            self.data = getattr(dut, prefix + 'data')
            self.valid = getattr(dut, prefix + 'valid')
            self.ready = getattr(dut, prefix + 'ready')

        async def send(self, data):
            self.valid <= 1
            for d in data:
                self.data <= d
                await RisingEdge(self.clk)
                while self.ready.value == 0:
                    await RisingEdge(self.clk)
            self.valid <= 0

        async def recv(self, count):
            self.ready <= 1
            data = []
            for _ in range(count):
                await RisingEdge(self.clk)
                while self.valid.value == 0:
                    await RisingEdge(self.clk)
                data.append(self.data.value.integer)
            self.ready <= 0
            return data


class InvalidArgument(RuntimeError):
    def __init__(self, arg):
           super().__init__()
           self.arg = arg


class Adder(Elaboratable):
    '''
    Module Description
    ------------------
    A sync N-bit adder with an async reset. The output port have N+1 bits to store the sum.


    Module Diagram
    --------------

                       |--------------|
             a_data -->|              |
            a_valid -->|              |
            a_ready <--|              |
                       |              |-->  r_data
                       |    Adder     |--> r_valid
                       |              |<--  r_ready
             b_data -->|              |
            b_valid -->|              |
            b_ready <--|              |
                       |--------------|
                           ^       ^
                           |       |
                          rst     clk

    Parameters
    ----------
    N : int
        Number of bits of a_data/b_data.

    Attributes
    ----------
    rst : Signal, in
        The result of the sum will be '0' if 'rst = 1'.

    a_valid, b_valid : Signal, in
        Input 'X_valid' signals are used to check the availability of data in the input ports.

    a_ready, b_ready : Signal, out
        Output 'X_ready' signals are indicate whether the module is listening to the input port.

    a_data, b_data : Singal(N), in
        N-bit input ports. Both summands should be load here.

    r_valid: Signal, out
        Signal used to inticate whether the result of the sum is ready to be read.

    r_ready: Signal, in
        Input signal used to check if the result was read.

    r_data: Signal(N+1), out
        (N+1)-bit output port. The result of the sum will be load here one clock cycle after both summands were read.
    '''
    def __init__(self, N):
        # Arguments Validation
        if N < 1:   # If the input argument type is not an integer it should raise a TypeError
            raise InvalidArgument("The argument 'N' should be a natural value greater than 1.")


        # Ports Definition
        self.a = Stream(N, name='a')
        self.b = Stream(N, name='b')
        self.r = Stream(N+1, name='r')

        # Rst Definition
        self.rst = Signal()

    def elaborate(self, platform):
        # Definitions
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        # Combinational logic
        # ===================

        comb += self.r.data.eq(signed(self.a.data) + signed(self.a.data))
        # nMigen generates a signal(N+1) if we need so add two signal(N)
        # More info: https://nmigen.info/nmigen/latest/lang.html#arithmetic-operators


        # Result
        with m.If(self.rst):
            comb += self.r.data.eq(Const(0,signed(N)))              # Async reset
        with m.Else():
            sync += self.r.valid.eq(~self.a.ready & ~self.b.ready)  # r_valid <- !a_ready & !b_ready


        # Sequential logic
        # ===================

        # RX
        with m.If(self.a.accepted()):           # if a_valid & a_ready
            sync += [
                self.a.ready.eq(0)              # a_data recieved, a_ready <- 0
            ]
        with m.If(self.b.accepted()):           # if b_valid & b_ready
            sync += [
                self.b.ready.eq(0)              # b_data recieved, b_ready <- 0
            ]


        # TX
        with m.If(self.r.accepted()):           # if r_valid & r_ready => Data sent! Waiting for incoming a_data & b_data
            sync += self.r.valid.eq(0)          # r_data was read => r_valid = 0
            sync += self.a.ready.eq(0)          # r_data was read => a_ready = 1
            sync += self.b.ready.eq(0)          # r_data was read => b_ready = 1

        return m

if __name__ == '__main__':
    print ("Initializing...")
    myAdder = Adder(3)
    # myAdder = Adder(-3)
    # myAdder = Adder("3")
