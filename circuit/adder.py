def _convert_to_binary(inpt) -> str:
	if type(inpt) == int:
		return bin(inpt)[2:]
	if type(inpt == str):
		return inpt
	
	raise NotImplementedError


def add_two_binary_numbers_of_equal_size(_num1: str, _num2: str) -> str:
	num1 = _convert_to_binary(_num1)
	num2 = _convert_to_binary(_num2)

	max_str_length = len(num1) if len(num1) > len(num2) else len(num2)

	num1_reversed = num1.rjust(max_str_length, "0")[::-1]
	num2_reversed = num2.rjust(max_str_length, "0")[::-1]

	reversed_result = ""
	remainder = "0"
		
	for left, right in zip(num1_reversed, num2_reversed):
		one_count = "".join([remainder, left, right]).count("1")
		reversed_result += "1" if one_count % 2 == 1 else "0"
		remainder = "1" if one_count > 1 else "0"
	
	if remainder == "1":
		reversed_result += "1"
	return reversed_result[::-1]



		
	