module top(dat_r, dat_w, we, clk, rst, adr);
  input [3:0] adr;
  input clk;
  output [7:0] dat_r;
  reg [7:0] dat_r;
  input [7:0] dat_w;
  reg [3:0] mem_r_addr;
  wire [7:0] mem_r_data;
  reg [3:0] mem_w_addr;
  reg [7:0] mem_w_data;
  reg mem_w_en;
  input rst;
  input we;
  reg [7:0] mem [15:0];
  $readmemh("memdump0.mem", mem);
  reg [3:0] _0_;
  always @(posedge clk) begin
    _0_ <= mem_r_addr;
    if (mem_w_en) mem[mem_w_addr] <= mem_w_data;
  end
  assign mem_r_data = mem[_0_];
  always @* begin
    mem_r_addr = 4'h0;
    mem_r_addr = adr;
  end
  always @* begin
    dat_r = 8'h00;
    dat_r = mem_r_data;
  end
  always @* begin
    mem_w_addr = 4'h0;
    mem_w_addr = adr;
  end
  always @* begin
    mem_w_data = 8'h00;
    mem_w_data = dat_w;
  end
  always @* begin
    mem_w_en = 1'h0;
    mem_w_en = we;
  end
endmodule
