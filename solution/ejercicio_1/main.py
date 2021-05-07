from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from random import randrange



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

        self.N = N

        # Ports Definition
        self.a = Stream(N, name='a')
        self.b = Stream(N, name='b')
        self.r = Stream(N+1, name='r')

        # Reset Values Definition
        # self.r.data.reset = 0     # Default reset value = 0x0
        #self.r.valid.reset = 0
        self.a.ready.reset = 0
        self.b.ready.reset = 0


    def elaborate(self, platform):
        # Definitions
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        # Combinational logic
        # ===================

        # comb += self.a.ready.eq((~self.r.valid) | (self.r.accepted())) # Si no tengo disponible la salida es porque se reseteo o a.valid o b.valid estan en 0
        # comb += self.b.ready.eq((~self.r.valid) | (self.r.accepted())) # Cuando no tengo disponible la salida o cuando acepte

        with m.If(self.a.valid & self.b.valid):
            comb += [
                self.a.ready.eq(1),                     # Indicate that i'm working with the registers
                self.b.ready.eq(1)
                ]
        with m.Else():
            comb += [
                self.a.ready.eq(0),                     # Indicate that i'm not able to read cause im waiting both registers
                self.b.ready.eq(0)
                ]


        # Sequential logic
        # ===================
        with m.If(self.a.valid & self.b.valid):         # Wait until both a_data and b_data ara vailable
            sync += self.r.valid.eq(1)                  # Cuando estan las dos entradas para ser leidas

            sync += self.r.data.eq(self.a.data.as_signed() + self.b.data.as_signed())
            # nMigen generates a signal(N+1FallingEdge) if we need so add two signal(N)
            # More info: https://nmigen.info/nmigen/latest/lang.html#arithmetic-operators
        with m.Else():
            with m.If(self.r.accepted()):               # If r_ready & r_valid
                sync += self.r.valid.eq(0)              # The output was read and it is not longer available.


        return m



async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


def toCA2(arg, N):      # TODO
    '''
    Function Description
    ------------------
    Converts an int to the N-bit 2's complement representation

    Parameters
    ----------
    arg : int
        Target number.

    N : int
        Number of bits of arg.

    '''
    raise RuntimeError("This function is not finished")
    return arg


@cocotb.test()
async def reset_test(dut):
    '''
    Test Description
    ------------------
    Checks if the values after the reset are correct.

    '''
    # Definitions
    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    width = len(dut.a__data)

    # Test Data
    data_a = [1, 2, 3]
    data_b = [4, 5, 6]
    expected = [0, 0, 0, 0]
    recved =   [0, 0, 0, 0]     # Initial recieved values

    # Test Execution
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    await RisingEdge(dut.clk)
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0
    cocotb.fork(stream_input_a.send(data_a))
    cocotb.fork(stream_input_b.send(data_b))
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 1
    await RisingEdge(dut.clk)
    dut.rst <= 0

    await FallingEdge(dut.clk)                          # Reads when FallingEdge(clk)
    recved[0] = stream_output.data.value.integer
    recved[1] = stream_output.valid.value.integer
    recved[2] = stream_input_a.ready.value.integer
    recved[3] = stream_input_b.ready.value.integer
    await RisingEdge(dut.clk)

    assert recved == expected

@cocotb.test()
async def basic_add_subs(dut):
    '''
    Test Description
    ------------------
    Checks if the adder is working. We check all the posible combinations (+)(+), (+)(-), (-)(+) and (-)(-).
    '''
    # Definitions
    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    width = len(dut.a__data)

    # Test Data
    data_a =   [3, -2,  3, -2]
    data_b =   [2,  3, -4, -2]
    expected = [5,  1, -1, -4]                 # The expected result is the sum of the data_a + data_b values

    # Test Execution
    await init_test(dut)
    cocotb.fork(stream_input_a.send(data_a))        # Port A input
    cocotb.fork(stream_input_b.send(data_b))        # Port B input
    recved = await stream_output.recv(len(data_a))  # Save the N values recieved


    recved_processed = [toCA2(recved[_],width) for _ in range(len(recved))]         # Convert the int to a string containing the N-bit ca2 binary equivalent
    expected_processed = [toCA2(expected[_],width) for _ in range(len(expected))]

    assert recved_processed == expected_processed

@cocotb.test()
async def overflow(dut):
    '''
    Test Description
    ------------------
    Checks what happen if we want to add two numbers that are thought to overflow.
    '''
    # Definitions
    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    width = len(dut.a__data)
    mask = 1 + int('1' * (width-1), 2)  # max value with (width-1) bits = (2^(width-1))

    # Test Data
    data_a =   [mask - 1  , -1*mask]
    data_b =   [mask - 1  , -1*mask]
    expected = [2*mask - 2, -2*mask]         # This should cause an overflow exception in width-1 bits.

    # Test Execution
    await init_test(dut)
    cocotb.fork(stream_input_a.send(data_a))        # Port A input
    cocotb.fork(stream_input_b.send(data_b))        # Port B input
    recved = await stream_output.recv(len(data_a))  # Save the N values recieved

    recved_processed = [toCA2(recved[_],width) for _ in range(len(recved))]         # Convert the int to a string containing the N-bit ca2 binary equivalent
    expected_processed = [toCA2(expected[_],width) for _ in range(len(expected))]

    assert recved_processed == expected_processed

@cocotb.test()
async def burst(dut):
    '''
    Test Description
    ------------------
    Stress test with random numbers.
    '''
    # Definitions
    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    N = 100
    width = len(dut.a__data)
    mask = 1 + int('1' * (width-1), 2)  # max value with (width-1) bits = (2^(width-1))

    # Test Data
    data_a = [randrange(-1*mask, mask-1) for _ in range(N)]   # This generates random numbres between -2^(width-1) and 2^(width-1)+1
    data_b = [randrange(-1*mask, mask-1) for _ in range(N)]
    expected = [(data_a[_] + data_b[_]) for _ in range(N)]    # Computes the expected result

    # Test Execution
    await init_test(dut)
    cocotb.fork(stream_input_a.send(data_a))        # Port A input
    cocotb.fork(stream_input_b.send(data_b))        # Port B input
    recved = await stream_output.recv(N)            # Save the N values recieved

    recved_processed = [toCA2(recved[_],width) for _ in range(len(recved))]         # Convert the int to a string containing the N-bit ca2 binary equivalent
    expected_processed = [toCA2(expected[_],width) for _ in range(len(expected))]

    assert recved_processed == expected_processed



if __name__ == '__main__':
    print ("Running Tests...")
    myAdder = Adder(4)
    # myAdder = Adder(-3)
    # myAdder = Adder("3")
    run(
        myAdder, 'main',
        ports=
        [
            *list(myAdder.a.fields.values()),
            *list(myAdder.b.fields.values()),
            *list(myAdder.r.fields.values())
        ],
        vcd_file='adder.vcd'
    )
