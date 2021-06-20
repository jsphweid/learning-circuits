from circuit.relay import Relay

def test_relay_as_repeater():
	relay_one = Relay(power=True)
	relay_two = Relay(power=True, switch=relay_one.output)

	assert relay_one.output_state == False
	assert relay_two.output_state == False

	relay_one.switch_on()

	assert relay_one.output_state == True
	assert relay_two.output_state == True

