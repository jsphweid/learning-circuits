module our_relay(o, switch, batt);
  output o; // simplified, but essentially the mechanical point of contact with another systme
  input switch, batt;
  wire and_wire;

  and a1(and_wire, switch, batt);
  and a2(o, and_wire);
endmodule
