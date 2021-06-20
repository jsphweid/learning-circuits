from circuit.relay import Relay


def test_relay():
	relay = Relay(power=True)

	assert relay.output_state == False
	relay.switch_on()
	assert relay.output_state == True


def test_relay_as_repeater():
	relay_one = Relay(power=True)
	relay_two = Relay(power=True, switch=relay_one.output)

	assert relay_one.output_state == False
	assert relay_two.output_state == False

	relay_one.switch_on()

	assert relay_one.output_state == True
	assert relay_two.output_state == True


def test_relay_as_repeater_but_more_complicated():
	relay_one = Relay(power=True)
	relay_two = Relay(power=True, switch=relay_one.output)
	relay_three = Relay(power=True, switch=relay_two.output)

	assert relay_one.output_state == False
	assert relay_two.output_state == False
	assert relay_three.output_state == False

	relay_one.switch_on()

	assert relay_one.output_state == True
	assert relay_two.output_state == True
	assert relay_three.output_state == True


