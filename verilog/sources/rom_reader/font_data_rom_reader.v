`timescale 1ns / 1ps

module font_data_rom_reader #(
    parameter integer CHAR_COUNT = 256,
    parameter integer CHAR_W     = 17,
    parameter integer CHAR_H     = 17
)(
    input  wire [7:0] char_index,
    input  wire [$clog2(CHAR_W)-1:0]      x,   // 0..16
    input  wire [$clog2(CHAR_H)-1:0]      y,   // 0..16
    output wire                           is_character
);

    // Total rows = CHAR_COUNT * CHAR_H
    localparam integer TOTAL_ROWS = CHAR_COUNT * CHAR_H;

    // Each row is 17 bits
    reg [CHAR_W-1:0] rom [0:TOTAL_ROWS-1];

    // Row address = char_index * CHAR_H + y
    wire [$clog2(TOTAL_ROWS)-1:0] row_addr;
    assign row_addr = char_index * CHAR_H + y;

    // Select bit
    assign is_character = rom[row_addr][CHAR_W-1 - x];
    // (MSB on left; remove "-1-x" if you want LSB first)

    initial begin
        $readmemb("font_data.mem", rom);
    end

endmodule
