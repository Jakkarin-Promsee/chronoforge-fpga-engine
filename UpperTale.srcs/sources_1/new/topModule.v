`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/22/2025 03:01:44 PM
// Design Name: 
// Module Name: topModule
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


module topModule(
    // Setting Inputs
    input clk,
    input reset,
    
    // Controller Input
    input switch_up,
    input switch_down,
    input switch_left,
    input switch_right,
    
    // Output
    output HS,
    output VS,
    output [3:0] RED, 
    output [3:0] GREEN,
    output [3:0] BLUE
    );
    
    // Internal Variable
    wire clk_div_main_system;
    wire clk_div_display_system;
    wire clk_div_control_system;
    
    // Connect main clk div (1KHz)
    clk_div_main_system clk_m (
        .clk_i(clk), 
        .rst_ni(reset), 
        
        .clk_o(clk_div_main_system)
    );
    
    // Conect display clk div (25MHz)
    clk_div_display_system clk_d (
        .clk_i(clk), 
        .rst_ni(reset), 
        
        .clk_o(clk_div_display_system)
    );
    
    // Conect display clk div (1kHz)
    clk_div_control_system clk_c (
        .clk_i(clk), 
        .rst_ni(reset), 
        
        .clk_o(clk_div_control_system)
    );
        
    // VGA Variable
    wire [9:0] x, y;
    wire blank;
    
    vga vga (
        .clk_display(clk_div_display_system),
        .reset(reset),
        
        .HS(HS),
        .VS(VS),
        .x(x),
        .y(y),
        .blank(blank)
    );
    
    wire player_areas_signal;
    wire [9:0] p_x;
    wire [9:0] p_y;
    wire [9:0] c_p_x;
    wire [9:0] c_p_y;
    
    player_colider p_c(
        .clk_control(clk_div_control_system),
        .reset(reset),
        .switch_up(switch_up),
        .switch_down(switch_down),
        .switch_left(switch_left),
        .switch_right(switch_right),
        
        .p_x(p_x),
        .p_y(p_y),
        .c_p_x(c_p_x),
        .c_p_y(c_p_y)
    );
    
    player_areas p_a (
        .x(x),
        .y(y),
        .p_x(p_x),
        .p_y(p_y),
        .c_p_x(c_p_x),
        .c_p_y(c_p_y),
        
        .player_area(player_areas_signal)
    );
    
    render_areas_color renderer(
        .x(x),
        .y(y),
        .blank(blank),
        .player_areas(player_areas_signal),
        
        .RED(RED),
        .GREEN(GREEN),
        .BLUE(BLUE)
    );
endmodule
