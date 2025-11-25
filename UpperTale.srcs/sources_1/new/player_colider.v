`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/24/2025 09:50:41 AM
// Design Name: 
// Module Name: player_colider
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


module player_colider(
    input clk_control,
    input reset,
    input switch_up,
    input switch_down,
    input switch_left,
    input switch_right,
    
    output reg [9:0] p_x,
    output reg [9:0] p_y,
    output reg [9:0] c_p_x,
    output reg [9:0] c_p_y
    );
    
    // Intial Postion Player at center display
    initial begin
        p_x = 320;
        p_y = 240;
        c_p_x = 30;
        c_p_y = 30;
    end
        
    // physic clock work at 100Hz
    always @(posedge clk_control) begin
        if (!reset) begin
            p_x <= 320;
            p_y <= 240;
            c_p_x <= 30;
            c_p_y <= 30;
            
        end else begin
            if(switch_up) begin
                if (p_y > 0)
                    p_y <= p_y - 1;
            end
            
            if(switch_down) begin
                if (p_y < 480-c_p_y) 
                    p_y <= p_y + 1;
            end
            
            if(switch_left) begin
                if (p_x > 0)
                    p_x <= p_x - 1;
            end
            
            if(switch_right) begin
                if (p_x < 640-c_p_x)
                    p_x <= p_x + 1;
            end   
        end
    end
endmodule
