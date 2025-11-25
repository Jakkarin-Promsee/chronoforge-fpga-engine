`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/22/2025 04:31:58 PM
// Design Name: 
// Module Name: player_areas
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


module player_areas(
    input [9:0] x,
    input [9:0] y,
    input [9:0] p_x,
    input [9:0] p_y,
    input [9:0] c_p_x,
    input [9:0] c_p_y,
    
    output player_area
);
    
    // Player rectable 30*30 shape
    assign player_area = (x>=p_x) && (x<p_x+c_p_x) && (y>=p_y) && (y<p_y+c_p_y) ;

endmodule
