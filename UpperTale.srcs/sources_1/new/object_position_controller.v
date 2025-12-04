`timescale 1ns / 1ps

module object_position_controller (
    input clk_object_control,
    input reset,
    
    input [2:0] movement_direction,
    input [9:0] object_pos_x,
    input [9:0] object_pos_y,
    input [4:0] object_speed,
    
    input sync_object_position,
        
        
    output reg update_object_position,
    output wire [9:0] object_override_pos_x,
    output wire [9:0] object_override_pos_y
);
    localparam SCALE_FACTOR_BITS = 3;
    localparam SCALE_FACTOR = 8;
    
    reg [9+SCALE_FACTOR_BITS:0] object_override_pos_x_hired;
    reg [9+SCALE_FACTOR_BITS:0] object_override_pos_y_hired;
    reg [2:0] movement_direction_hired;
    reg [4:0] object_speed_hired;
    
    assign object_override_pos_x = object_override_pos_x_hired >> SCALE_FACTOR_BITS;
    assign object_override_pos_y = object_override_pos_y_hired >> SCALE_FACTOR_BITS;

    always @(posedge clk_object_control) begin
        if(reset) begin
            update_object_position <= 0;
            object_override_pos_x_hired <= 0;
            object_override_pos_y_hired <= 0;
            
            movement_direction_hired <= movement_direction;
            object_speed_hired <= object_speed;
        end else begin
            if (!sync_object_position) begin
                object_override_pos_x_hired <= object_pos_x << SCALE_FACTOR_BITS;
                object_override_pos_y_hired <= object_pos_y << SCALE_FACTOR_BITS;
                
                movement_direction_hired <= movement_direction;
                object_speed_hired <= object_speed;
                
                update_object_position <= 1;
            end else begin
                update_object_position <= 0;
                
                case (movement_direction_hired)
                    // Upper
                    0: begin
                        object_override_pos_y_hired <= object_override_pos_y_hired - object_speed_hired;
                    end
                    
                    // Upper Right
                    1: begin
                        object_override_pos_y_hired <= object_override_pos_y_hired - object_speed_hired;
                        object_override_pos_x_hired <= object_override_pos_x_hired + object_speed_hired;       
                    end
                    
                    // Right
                    2: begin
                        object_override_pos_x_hired <= object_override_pos_x_hired + object_speed_hired;       
                    end
                    
                    // Bottom Right
                    3: begin
                        object_override_pos_y_hired <= object_override_pos_y_hired + object_speed_hired;
                        object_override_pos_x_hired <= object_override_pos_x_hired + object_speed_hired;       
                    end
                    
                    // Bottom
                    4: begin
                        object_override_pos_y_hired <= object_override_pos_y_hired + object_speed_hired;   
                    end
                    
                    // Bottom Left
                    5: begin
                        object_override_pos_y_hired <= object_override_pos_y_hired + object_speed_hired;
                        object_override_pos_x_hired <= object_override_pos_x_hired - object_speed_hired;       
                    end
                    
                    // Left
                    6: begin
                        object_override_pos_x_hired <= object_override_pos_x_hired - object_speed_hired;       
                    end
                    
                    // Upper Left
                    7: begin
                        object_override_pos_y_hired <= object_override_pos_y_hired - object_speed_hired;
                        object_override_pos_x_hired <= object_override_pos_x_hired - object_speed_hired;       
                    end
                endcase
            end
        end
    end
    

    
    
    

endmodule
