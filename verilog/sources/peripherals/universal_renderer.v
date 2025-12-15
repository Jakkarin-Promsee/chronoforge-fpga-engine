`timescale 1ns / 1ps

module universal_renderer(
    input reset,
    input [9:0] x,
    input [9:0] y,
    input blank,   
    
    input is_trigger_player, 
    
    input transparent_out_screen_display,
    
    input object_colider_signal,
    input object_trigger_signal,
    input game_display_border_render,
    input out_side_display_signal,
    input healt_bar_signal,
    input healt_bar_border_signal,
    input character_signal,
    input player_render,
    
    output reg [3:0] RED,  
    output reg [3:0] GREEN,
    output reg [3:0] BLUE
);

    always @(*) begin
        // Default (safe)
        RED   = 0;
        GREEN = 0;
        BLUE  = 0;

        if (!reset) begin
            // --------------------------------------------------
            // Blank Screen (VGA blanking = true black)
            // --------------------------------------------------
            if (blank) begin 
                RED   = 0;
                GREEN = 0;
                BLUE  = 0;
            end 

            // --------------------------------------------------
            // Object Collider (NEON CYAN)
            // --------------------------------------------------
            else if (object_colider_signal &&
                    !(out_side_display_signal && !transparent_out_screen_display)) begin
                RED   = 0;
                GREEN = 14;
                BLUE  = 14;
            end 

            // --------------------------------------------------
            // Object Trigger (NEON RED)
            // --------------------------------------------------
            else if (object_trigger_signal &&
                    !(out_side_display_signal && !transparent_out_screen_display)) begin
                RED   = 15;
                GREEN = 3;
                BLUE  = 3;
            end
                        
            // --------------------------------------------------
            // Game Display Border (SOFT WHITE)
            // --------------------------------------------------
            else if (game_display_border_render) begin
                RED   = 10;
                GREEN = 10;
                BLUE  = 10;
            end
            
            // --------------------------------------------------
            // Player (COOL BLUE / CYAN)
            // --------------------------------------------------
            else if (player_render) begin 
                RED   = 2;
                GREEN = 6;
                BLUE  = 15;
            end 
            
            // --------------------------------------------------
            // HP Bar Border
            // --------------------------------------------------
            else if (healt_bar_border_signal) begin
                RED   = 12;
                GREEN = 12;
                BLUE  = 12;
            end
            
            // --------------------------------------------------
            // HP Bar Fill
            // --------------------------------------------------
            else if (healt_bar_signal) begin
                RED   = 14;
                GREEN = 4;
                BLUE  = 4;
            end
            
            // --------------------------------------------------
            // Characters (LIGHT GRAY)
            // --------------------------------------------------
            else if (character_signal) begin
                RED   = 12;
                GREEN = 12;
                BLUE  = 12;
            end
            
            // --------------------------------------------------
            // Background (DARK GRAY)
            // --------------------------------------------------
            else begin
                // Optional effect hook
                if (is_trigger_player && 0) begin
                    RED   = 4;
                    GREEN = 4;
                    BLUE  = 4;
                end else begin
                    RED   = 1;
                    GREEN = 1;
                    BLUE  = 1;
                end
            end
        end
    end

endmodule
