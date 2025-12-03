`timescale 1ns / 1ps

module object_position_controller (
    input clk_object_control,
    input reset,
    input [2:0] movement_direction,
    input [9:0] object_pos_x,
    input [9:0] object_pos_y,
    input [4:0] speed,
    input sync_object_position,
        
        
    output reg update_object_position,
    output reg [9:0] object_override_pos_x,
    output reg [9:0] object_override_pos_y
);

    always @(posedge clk_object_control) begin
        if(reset) begin
            update_object_position <= 0;
            object_override_pos_x <= 0;
            object_override_pos_y <= 0;
            
        end else begin
            if (!sync_object_position) begin
                object_override_pos_x <= object_pos_x;
                object_override_pos_y <= object_pos_y;
                
                update_object_position <= 1;
            end else begin
                update_object_position <= 0;
                
                case (movement_direction)
                    // Upper
                    0: begin
                        object_override_pos_y <= object_override_pos_y - 1;
                    end
                    
                    // Upper Right
                    1: begin
                        object_override_pos_y <= object_override_pos_y - 1;
                        object_override_pos_x <= object_override_pos_x + 1;       
                    end
                    
                    // Right
                    2: begin
                        object_override_pos_x <= object_override_pos_x + 1;       
                    end
                    
                    // Bottom Right
                    3: begin
                        object_override_pos_y <= object_override_pos_y + 1;
                        object_override_pos_x <= object_override_pos_x + 1;       
                    end
                    
                    // Bottom
                    4: begin
                        object_override_pos_y <= object_override_pos_y + 1;   
                    end
                    
                    // Bottom Left
                    5: begin
                        object_override_pos_y <= object_override_pos_y + 1;
                        object_override_pos_x <= object_override_pos_x - 1;       
                    end
                    
                    // Left
                    6: begin
                        object_override_pos_x <= object_override_pos_x - 1;       
                    end
                    
                    // Upper Left
                    7: begin
                        object_override_pos_y <= object_override_pos_y - 1;
                        object_override_pos_x <= object_override_pos_x - 1;       
                    end
                endcase
            end
        end
    end
    

    
    
    

endmodule
