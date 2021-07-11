import pytest

from circuit.relay import Relay


def test_relay_is_switched_off_by_default():
    relay = Relay(power=True)
    assert relay.output_state == False


def test_relay_switching_on_works():
    relay = Relay(power=True)

    relay.switch_on()
    assert relay.output_state == True


def test_relay_as_repeater():
    relay_one = Relay(power=True)
    relay_two = Relay(power=True, switch=relay_one.output)

    relay_one.switch_on()

    assert relay_one.output_state == True
    assert relay_two.output_state == True


def test_relay_as_repeater_but_more_complicated():
    relay_one = Relay(power=True)
    relay_two = Relay(power=True, switch=relay_one.output)
    relay_three = Relay(power=True, switch=relay_two.output)

    relay_one.switch_on()

    assert relay_one.output_state == True
    assert relay_two.output_state == True
    assert relay_three.output_state == True


def test_relay_in_series():
    relay_one = Relay(power=True)
    relay_two = Relay(power=relay_one.output)
    relay_three = Relay(power=relay_two.output)

    relay_one.switch_on()

    assert relay_one.output_state == True
    assert relay_two.output_state == False
    assert relay_three.output_state == False

    relay_two.switch_on()

    assert relay_one.output_state == True
    assert relay_two.output_state == True
    assert relay_three.output_state == False

    relay_three.switch_on()

    assert relay_one.output_state == True
    assert relay_two.output_state == True
    assert relay_three.output_state == True


@pytest.mark.parametrize('one_on, two_on, three_on, expected', [
    (False, False, False, False),
    (True, False, False, True),
    (True, True, False, True),
    (True, True, True, True),
    (False, False, True, True),
    (False, True, True, True)])
def test_relay_in_parallel(one_on, two_on, three_on, expected):
    relay_one = Relay(power=True)
    relay_two = Relay(power=True)
    relay_three = Relay(power=True)

    if one_on: relay_one.switch_on()
    if two_on: relay_two.switch_on()
    if three_on: relay_three.switch_on()

    assert Relay.has_output([relay_one, relay_two, relay_three]) == expected
