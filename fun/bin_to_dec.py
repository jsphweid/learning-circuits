def bin_to_dec(bin: str) -> int:
  total = 0
  for i, num_str in enumerate(list(reversed(bin))):
    total += (1 if num_str == "1" else 0) * (2 ** i)
  return total