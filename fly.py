"""FSM Playground - the fly"""

'''
The fly is trapped in a room with some bread crumbs lying around.
It flies around annoying the human that sleeps in
the room. When it is not wandering around on human skin, it
flies around in the room, looking for a place to sit and rest
awhile, and then it starts looking for human skin again.

To make things simple, the only property the fly has is it's "energy level".
When this is low, the fly look for food.
When it is high, the fly will try and rest.

When the fly is on human skin, there is a chance it gets hit by the human.

Three clear states emerge:

1 Resting
2 Eating
3 Dead

Possible extensions:
- the food is never exhausted in current model. it could be finite,
  thus letting the fly die of starvation.
- currently there is no state "moving" where the fly flies or walks on skin.
  during such times, the energy level should lessen quicker than in resting
  state as it's a lot more energy consuming activities!
- what about if the human wakes up? then (s)he could smite the fly with
  much higher probability, and in more states than "EATING". a second FSM to model this?
'''

import unittest

from statemachine import StateMachine
import logging
logging.basicConfig(level=logging.DEBUG)
import random


class Cargo(object):

    def __init__(self, energy):
        self.energy = energy
        self.food = 0

    def hit_by_human(self):
        return random.uniform(0, 100) > 90

    def full(self):
        return self.energy > 90


def resting(cargo):
    logging.debug('Resting, energy level is %d.' % cargo.energy)
    cargo.energy -= 1
    if cargo.energy < 70:
        logging.debug('Getting hungry, going for a snack.')
        return ('eating', cargo)
    else:
        logging.debug('So nice to sleep.')
        return ('resting', cargo)


class TestRestingState(unittest.TestCase):

    def test_stays_in_resting_if_not_hungry(self):
        # The fly is hungry if less than 70 energy units
        cargo = Cargo(80)
        (new_state, cargo) = resting(cargo)
        self.assertEqual('resting', new_state)

    def test_goes_to_looking_state_if_hungry(self):
        # The fly is hungry if less than 70 energy units
        cargo = Cargo(60)
        (new_state, cargo) = resting(cargo)
        self.assertEqual('eating', new_state)

    def test_loses_one_energy_per_update(self):
        cargo = Cargo(99)
        (new_state, cargo) = resting(cargo)
        self.assertEqual(98, cargo.energy)


def eating(cargo):
    logging.debug('Eating, energy level is %d.' % cargo.energy)
    cargo.energy += 5
    cargo.food -= 5
    if cargo.hit_by_human():
        logging.debug('Damn, hit by human!')
        return ('dead', cargo)
    elif cargo.full():
        logging.debug('I am full, going for a nap.')
        return ('resting', cargo)
    else:
        logging.debug('Still hungry, eat more.')
        return ('eating', cargo)


class TestEatingState(unittest.TestCase):

    def setUp(self):
        self.cargo = Cargo(100)

    def test_goes_to_rest_if_full(self):
        def full():
            return True
        cargo = self.cargo
        cargo.full = full
        (new_state, cargo) = eating(cargo)
        self.assertEqual('resting', new_state)

    def test_dies_if_hit_by_human(self):
        cargo = self.cargo

        def hit():
            return True
        cargo.hit_by_human = hit
        (new_state, cargo) = eating(cargo)
        self.assertEqual('dead', new_state)

    def test_energy_increases_when_eating(self):
        cargo = self.cargo
        cargo.energy = 60
        (new_state, cargo) = eating(cargo)
        self.assertEqual(65, cargo.energy)

    def test_food_decreases_when_eating(self):
        cargo = self.cargo
        cargo.food = 65
        (new_state, cargo) = eating(cargo)
        self.assertEqual(60, cargo.food)

    def test_keeps_eating_if_human_misses_and_not_full(self):
        cargo = Cargo(70)

        def hit():
            logging.debug('hit returning False')
            return False
        cargo.hit_by_human = hit
        (new_state, cargo) = eating(cargo)
        self.assertEqual('eating', new_state)


def dead(cargo):
    pass


def selftest():
    unittest.main()


def build_machine():
    m = StateMachine()
    m.add_state("resting", resting)
    m.add_state("eating", eating)
    m.add_state("dead", dead, end_state=1)
    m.set_start("resting")
    return m

if __name__ == '__main__':
    # selftest()
    m = build_machine()
    cargo = Cargo(100)
    m.run(cargo)

# cargo -> env or world or ...
