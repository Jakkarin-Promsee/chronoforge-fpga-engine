`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/22/2025 03:09:14 PM
// Design Name: 
// Module Name: clk_div_main_system
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module clk_div_main_system(
  input wire rst_ni,
  input wire clk_i,
  output wire clk_o
);
reg [31:0] counter_r;
reg clk_r;

always @(posedge clk_i) begin
// If sw0 = false, reset condition
  if (!rst_ni) begin
    clk_r <= 0;
    counter_r <= 0;
 
// Else reduce Hz from 100MHz to 100Hz (100fps)
  end else begin
    if (counter_r == (100_000  / 2) - 1) begin
      clk_r <= ~clk_r;
      counter_r <= 0;
    end else begin
      counter_r <= counter_r + 1;
    end
  end
end

assign clk_o = clk_r;

endmodule
