module nothing(o, i);
  // A circuit that does nothing... just for learning syntax and what not
  output o;
  input i;
  wire pointless_internal_wire;
  assign pointless_internal_wire = i;
  assign o = pointless_internal_wire;
endmodule

module nothing_test;
  reg a;
  wire o;

  nothing n (o, a);

  initial begin
    $monitor("nothing test: At time %2t, a = %d, o = %d", $time, a, o);
    $dumpfile("vcds/nothing.vcd");
    $dumpvars(0, nothing_test);

    a = 1; # 10;
    a = 0; # 10;
    a = 1; # 10;
    a = 1; # 10;
    a = 0; # 10;

  end

endmodule