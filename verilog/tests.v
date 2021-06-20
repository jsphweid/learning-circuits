
// TODO: come back and try to understand this.
// For now I just copied and pasted this from:
// https://stackoverflow.com/questions/13904794/assert-statement-in-verilog
// module assert(input clk, input test);
//     always @(posedge clk)
//     begin
//         if (test !== 1)
//         begin
//             $display("ASSERTION FAILED in %m");
//             $finish;
//         end
//     end
// endmodule


module assert(input actual, input expected);
  begin
    if (actual !== expected)
      begin
        $display("ASSERTION FAILED: ACTUAL %d, EXPECTED %d", actual, expected);
        $finish;
      end
  end
endmodule



// test bench
module n_test;
  reg a, b; // inputs for the test
  wire c; // output from our_nand module

  our_nand n (c, a, b);


  // initial blocks are done in parallel
  initial begin


    $monitor("At time %2t, a = %d b = %d c = %d", $time, a, b, c);
    $dumpfile("n.vcd");
    $dumpvars(0, n_test);

    a = 1; b = 0; # 10; 
    // a = 0; b = 1; # 10; assert(1, c)
    // a = 1; b = 0; # 10; assert(1, c)
    // a = 1; b = 1; # 10; assert(0, c)

    $finish;
  end
endmodule