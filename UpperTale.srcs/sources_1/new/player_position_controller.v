`timescale 1ns / 1ps

module player_position_controller#(
    parameter integer PLAYER_POS_X = 320,
    parameter integer PLAYER_POS_Y = 240,
    parameter integer PLAYER_W = 30,
    parameter integer PLAYER_H  = 30,
    parameter integer SPEED = 3,
    parameter integer GRAVITY = 1,           // gravity acceleration per tick
    parameter integer MAX_FALL_SPEED = 3     // max falling speed
)(
    input clk_player_control,
    input clk_update_position,
    input clk_calculation,
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

    // --- NEW DECLARATION ---
    reg [9:0] player_vel_y; // Register for vertical velocity
    // -----------------------
    
    // Intial Postion Player at center display
    initial begin
        player_pos_x = PLAYER_POS_X;
        player_pos_y = PLAYER_POS_Y;
        player_w = PLAYER_W;
        player_h = PLAYER_H;
        player_vel_y = 0; // Initialize velocity
    end
    
    // ... (Rest of your module code before always block)
    
    // physic clock work at 100Hz
    always @(posedge clk_player_control) begin
        // Set player center in display
        if (!reset) begin
            player_pos_x = PLAYER_POS_X;
            player_pos_y = PLAYER_POS_Y;
            player_w = PLAYER_W;
            player_h = PLAYER_H;
            player_vel_y = 0;
        end else begin
            
            // 1. Vertical Movement (Gravity and Jump)
            // If 'Up' is pressed, set a fixed upward velocity (Jump/Reverse Gravity)
            if (switch_up) begin
                // You can tune this negative value for a better 'jump' feel
                player_vel_y <= -SPEED;
            end else begin
                // Apply GRAVITY (acceleration) to velocity unless max speed is reached
                if (player_vel_y < 10) // 10 is an arbitrary max-fall-speed value (tune this!)
                    player_vel_y <= player_vel_y + GRAVITY;
            end
            
            // Update Y position based on velocity
            // Boundary check and position update for Y-axis
            if (player_pos_y + player_vel_y < game_display_y0) begin
                // Hit top boundary
                player_pos_y <= game_display_y0;
                player_vel_y <= 0; // Stop vertical movement
            end else if (player_pos_y + player_vel_y > game_display_y1 - player_h) begin
                // Hit bottom boundary (ground)
                player_pos_y <= game_display_y1 - player_h;
                player_vel_y <= 0; // Stop vertical movement
            end else begin
                // Move player by the current velocity
                player_pos_y <= player_pos_y + player_vel_y;
            end
    
            // 2. Horizontal Movement (Standard, no change from your original logic)
            // Check for boundary before moving left
            if(switch_left) begin
                if (player_pos_x > game_display_x0)
                    player_pos_x <= player_pos_x - SPEED;
            end
            // Check for boundary before moving right
            if(switch_right) begin
                if (player_pos_x < game_display_x1 - player_w)
                    player_pos_x <= player_pos_x + SPEED;
            end
            
            // Optional: Implement a dead-stop for horizontal movement if neither is pressed
            // For simple controls like this, leaving it as-is (stops when not pressed) is fine.
            
            // Optional: If 'Down' is pressed, you might increase the downward velocity faster
            if(switch_down) begin
                player_vel_y <= player_vel_y + SPEED; // Optional fast-fall/crouch
            end
            
        end
    end
endmodule