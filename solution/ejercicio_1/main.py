from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
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

        # Rst Definition
        self.rst = Signal()

    def elaborate(self, platform):
        # Definitions
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        # Combinational logic
        # ===================

        # comb += self.a.ready.eq((~self.r.valid) | (self.r.accepted())) # Si no tengo disponible la salida es porque se reseteo o a.valid o b.valid estan en 0
        # comb += self.b.ready.eq((~self.r.valid) | (self.r.accepted())) # Cuando no tengo disponible la salida o cuando acepte







        # Sequential logic
        # ===================
        with m.If(self.rst):
            sync += self.r.data.eq(Const(0,signed(self.N)))      # Async reset
            sync += self.r.valid.eq(1)
            sync += [
                self.a.ready.eq(1),                         # Indicate that i "read" the registers, but the result will be zero
                self.b.ready.eq(1)
                ]
        with m.Else():
            with m.If(self.a.valid & self.b.valid):         # Wait until both a_data and b_data ara vailable
                sync += self.r.valid.eq(1)                  # Cuando estan las dos entradas para ser leidas
                sync += [
                    self.a.ready.eq(1),                     # Indicate that i'm working with the registers
                    self.b.ready.eq(1)
                    ]

                sync += self.r.data.eq(self.a.data + self.b.data)
                # nMigen generates a signal(N+1) if we need so add two signal(N)
                # More info: https://nmigen.info/nmigen/latest/lang.html#arithmetic-operators
            with m.Else():
                sync += self.r.valid.eq(0)                  # La salida no esta disponible
                sync += [
                    self.a.ready.eq(0),                     # Indicate that i'm not able to read cause im waiting both registers
                    self.b.ready.eq(0)
                    ]



        # # RX
        # with m.If(self.a.accepted()):           # if a_valid & a_ready
        #     sync += [
        #         self.a.ready.eq(0)              # a_data recieved, a_ready <- 0
        #     ]
        #
        # with m.If(self.b.accepted()):           # if b_valid & b_ready
        #     sync += [
        #         self.b.ready.eq(0)              # b_data recieved, b_ready <- 0
        #     ]
        #
        #
        # # TX
        # with m.If(self.r.accepted()):           # if r_valid & r_ready => Data sent! Waiting for incoming a_data & b_data
        #     sync += self.r.valid.eq(0)          # r_data was read => r_valid = 0
        #     sync += self.a.ready.eq(0)          # r_data was read => a_ready = 1
        #     sync += self.b.ready.eq(0)          # r_data was read => b_ready = 1

        return m


# init test inicia el clk, manda un pulso de reset despues de 2 clk.
async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


@cocotb.test()
async def burst(dut):
    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    N = 100
    width = len(dut.a__data)

    mask = 1 + int('1' * (width-1), 2)  # Retorna valor máximo representable con (width-1) bits.

    data_a = [randrange(-1*mask, mask-1) for _ in range(N)]   # Genera N valores random representables en N bits. (Enteros positivos)

    data_b = [randrange(-1*mask, mask-1) for _ in range(N)]   # Genera N valores random entre -2^(width-1) y 2^(width-1)+1

    expected = [(data_a[i] + data_b[i]) for i in range(N)]    # Calculo la salida esperada como la suma de las entradas


    cocotb.fork(stream_input_a.send(data))          # Entrada de datos para el puerto A

    cocotb.fork(stream_input_b.send(data))          # Entrada de datos para el puerto B

    recved = await stream_output.recv(N)            # Guardo los N datos recibidos

    assert recved == expected                       # Consulto si los datos recibidos son iguales a los esperados


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
