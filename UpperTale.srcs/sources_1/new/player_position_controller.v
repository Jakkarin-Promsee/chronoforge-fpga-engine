`timescale 1ns / 1ps

module player_position_controller#(
    parameter integer PLAYER_POS_X = 320,
    parameter integer PLAYER_POS_Y = 240,
    parameter integer PLAYER_W = 30,
    parameter integer PLAYER_H = 30,
    parameter integer SPEED = 16,  // Example: 16 = 1 full pixel movement per clock
    parameter integer GRAVITY = 13,  // Example: 1 = 1/16th pixel gravity per clock
    parameter integer JUMP_H = 80
    )(
    input clk_player_control,
    input reset,
    input switch_up,
    input switch_down,
    input switch_left,
    input switch_right,
    input [9:0] game_display_x0,
    input [9:0] game_display_y0,
    input [9:0] game_display_x1,
    input [9:0] game_display_y1,
    
    output reg [9:0] player_pos_x,
    output reg [9:0] player_pos_y,
    output reg [9:0] player_w,
    output reg [9:0] player_h
    );

    // Scaling Factor: 16 (4 bits for fractional part)
    localparam SCALE_FACTOR_BITS = 4;
    localparam SCALE_FACTOR = 16;
    
    // Internal High-Resolution Registers (10 bits for integer + 4 bits for fraction = 14 bits)
    reg [9 + SCALE_FACTOR_BITS : 0] player_pos_x_hires;
    reg [9 + SCALE_FACTOR_BITS : 0] player_pos_y_hires;
    
    // Position Boundaries scaled up by SCALE_FACTOR (shifted left by 4)
    wire [9 + SCALE_FACTOR_BITS : 0] game_display_x0_hires;
    wire [9 + SCALE_FACTOR_BITS : 0] game_display_y0_hires;
    wire [9 + SCALE_FACTOR_BITS : 0] game_display_x1_hires;
    wire [9 + SCALE_FACTOR_BITS : 0] game_display_y1_hires;
    
    // Player width/height are also scaled for internal use
    wire [9 + SCALE_FACTOR_BITS : 0] player_w_hires;
    wire [9 + SCALE_FACTOR_BITS : 0] player_h_hires;

    // Scale up the boundary and size inputs
    assign game_display_x0_hires = game_display_x0 << SCALE_FACTOR_BITS;
    assign game_display_y0_hires = game_display_y0 << SCALE_FACTOR_BITS;
    assign game_display_x1_hires = game_display_x1 << SCALE_FACTOR_BITS;
    assign game_display_y1_hires = game_display_y1 << SCALE_FACTOR_BITS;
    
    assign player_w_hires = PLAYER_W << SCALE_FACTOR_BITS;
    assign player_h_hires = PLAYER_H << SCALE_FACTOR_BITS;
    
    // Player's visible size is constant
    initial begin
        player_w = PLAYER_W;
        player_h = PLAYER_H;
    end

    reg on_ground;
    reg is_hold_switch_up;
    
    initial begin
        // Initialize high-resolution positions
        player_pos_x_hires = PLAYER_POS_X << SCALE_FACTOR_BITS;
        player_pos_y_hires = PLAYER_POS_Y << SCALE_FACTOR_BITS;
        
        // Initialize output positions (integer part only)
        player_pos_x = PLAYER_POS_X;
        player_pos_y = PLAYER_POS_Y;

        on_ground = 1;
        is_hold_switch_up = 0;
    end
    
    always @(posedge clk_player_control) begin
        if (!reset) begin
            // Reset high-resolution positions
            player_pos_x_hires <= PLAYER_POS_X << SCALE_FACTOR_BITS;
            player_pos_y_hires <= PLAYER_POS_Y << SCALE_FACTOR_BITS;
            
            player_w <= PLAYER_W;
            player_h <= PLAYER_H;
            is_hold_switch_up <= 0;
            on_ground <= 1;
            
        end else begin
            
            // --- Vertical Movement Logic ---
            
            // 1. Handle Jump/Up Input
            if (switch_up && (is_hold_switch_up || on_ground)) begin
                if (player_pos_y_hires > game_display_y0_hires) begin
                    // Use SPEED directly (1 unit = 1/16th pixel)
                    player_pos_y_hires <= player_pos_y_hires - SPEED; 
                    is_hold_switch_up <= 1;
                    on_ground <= 0; // Leaving the ground
                end else begin
                    player_pos_y_hires <= game_display_y0_hires; // Hit top boundary
                end
                
                // 1.1 If jump hit the upper wall
                if (player_pos_y_hires <= game_display_y0_hires) begin
                    is_hold_switch_up <= 0; // Release jump hold
                end
                
                // 1.1 If jump hit the height limit
                if (player_pos_y_hires <= game_display_y1_hires - player_h_hires - (JUMP_H*SCALE_FACTOR)) begin
                    is_hold_switch_up <= 0; // Release jump hold
                end
                
            end else begin
                is_hold_switch_up <= 0; // Release jump hold
            end

            // 2. Apply Gravity (Only if not moving up)
            if (!is_hold_switch_up) begin
                if (player_pos_y_hires < game_display_y1_hires - player_h_hires) begin
                    // Use GRAVITY directly (1 unit = 1/16th pixel)
                    if (player_pos_y_hires + GRAVITY < game_display_y1_hires - player_h_hires) begin
                        player_pos_y_hires <= player_pos_y_hires + GRAVITY;
                    end else begin
                        player_pos_y_hires <= game_display_y1_hires - player_h_hires; // Snap to floor
                    end
                end
            end
            
            // 3. Handle Down Input
            if (switch_down) begin
                if (player_pos_y_hires + player_h_hires + SPEED <= game_display_y1_hires) begin
                    // Use SPEED directly
                    player_pos_y_hires <= player_pos_y_hires + SPEED; 
                end else begin
                    player_pos_y_hires <= game_display_y1_hires - player_h_hires;
                end
            end
            
            // 4. Update Ground Check
            // Check if the player is within GRAVITY scaled units of the bottom boundary
            if (game_display_y1_hires - player_pos_y_hires - player_h_hires <= GRAVITY) begin
                on_ground <= 1;
            end else begin
                on_ground <= 0;
            end
            
            // --- Horizontal Movement Logic ---
            
            // Left axis
            if(switch_left) begin
                if(player_pos_x_hires > game_display_x0_hires) begin
                    // Use SPEED directly
                    if (player_pos_x_hires - SPEED >= game_display_x0_hires) begin
                        player_pos_x_hires <= player_pos_x_hires - SPEED;
                    end else begin
                        player_pos_x_hires <= game_display_x0_hires; // Snap to left boundary
                    end
                end 
            end
            
            // Right axis
            if(switch_right) begin
                if(player_pos_x_hires + player_w_hires < game_display_x1_hires) begin
                    // Use SPEED directly
                    if (player_pos_x_hires + player_w_hires + SPEED <= game_display_x1_hires) begin
                        player_pos_x_hires <= player_pos_x_hires + SPEED;
                    end else begin
                        player_pos_x_hires <= game_display_x1_hires - player_w_hires; // Snap to right boundary
                    end
                end
            end
            
            // --- Output Assignment (10-bit integer part only) ---
            // Divide by 16 by shifting right 4 bits to get the pixel integer value
            player_pos_x <= player_pos_x_hires >> SCALE_FACTOR_BITS;
            player_pos_y <= player_pos_y_hires >> SCALE_FACTOR_BITS;
            
        end
    end
endmodule