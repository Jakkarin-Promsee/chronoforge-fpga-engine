`timescale 1ns / 1ps

module game_display_controller #(
    parameter integer GAME_DISPLAY_X0 = 100,
    parameter integer GAME_DISPLAY_Y0 = 100,
    parameter integer GAME_DISPLAY_X1 = 540,
    parameter integer GAME_DISPLAY_Y1 = 380
)(
    input clk_object_control,
    input reset,
    
    input  [9:0]  display_pos_x1,
    input  [9:0]  display_pos_y1,
    input  [9:0]  display_pos_x2,
    input  [9:0]  display_pos_y2,
    
    output reg [9:0] game_display_x0,
    output reg [9:0] game_display_y0,
    output reg [9:0] game_display_x1,
    output reg [9:0] game_display_y1
    );
        
    // physic clock work at 100Hz
    always @(posedge clk_object_control) begin
        // Set player center in display
        if (reset) begin
            game_display_x0 <= GAME_DISPLAY_X0;
            game_display_y0 <= GAME_DISPLAY_Y0;
            game_display_x1 <= GAME_DISPLAY_X1;
            game_display_y1 <= GAME_DISPLAY_Y1;
        end else begin
            game_display_x0 <= display_pos_x1;
            game_display_y0 <= display_pos_y1;
            game_display_x1 <= display_pos_x2;
            game_display_y1 <= display_pos_y2;
        end
    end
    
endmodule
