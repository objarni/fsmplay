"""FSM Playground - the fly"""

'''
The fly is trapped in a room with some bread crumbs lying around.
It flies around annoying the human that sleeps in
the room. When it is not wandering around on human skin, it
flies around in the room, looking for a place to sit and rest
awhile, and then it starts looking for human skin again.

So it has these different states:
1 Flying / Looking for restplace
2 Flying / Looking for skin
3 Sitting / Resting
4 Walking / Looking for food on skin
5 Sitting / Eating on skin
6 Dead / Hit by human or starvation

To make things simple, the only property the fly has is it's "energy level".
When this is low, the fly look for food, or die if not replenished.
When it is high, the fly will try and rest.

The energy level is reduced by flying (a lot) and walking (a little), and
minimally by resting sitting still. It is replenished by sitting and eating.

When the fly is on human skin, there is a chance it gets hit by the human,
or else it flies away and starts looking for skin again.

If it does not replenish energy level before it reaching zero, it dies.

There is only so much food on the human skin, so eventually the fly dies
of starvation (if not dead before by being hit!).

This means the state visible to each state is 'energy' and 'food'.
Energy is internal to the fly, and Food is the world food.

(also, a random number generator will determine random events, so it's
kind of part of the state too, but let's ignore that).

*** Simplification of states ***
In a simpler model, we ignore the two "flying" states, and see them
as transitions instead. We get:

1 Resting
2 Searching (flying or walking)
3 Eating
4 Dead
'''

import unittest

from statemachine import StateMachine
import logging
logging.basicConfig(level=logging.DEBUG)
import random

'''
def flying_to_rest(cargo):
    cargo.energy -= 1
    if cargo.energy == 0:
        return ('dead', cargo)
    else:
        print "I'm flying for a nap now."
        return ('flying_to_skin', cargo)

def flying_to_skin(cargo):
    print "I'm flying to skin."
    if random.uniform(0, 100) > 90:
        print "Scheize, got wacked!"
        return ('dead', cargo)
    else:
        return ('flying_to_rest', cargo)

def dead(cargo):
    pass  # End state is never executed
'''

'''
def exploring_skin():
    pass

def resting():
    print "I'm resting on the wall."

def eating_on_skin():
    print "Wo-hoo, eating food!"


def dead():
    print 'Bummer, died.'
    return 'dead'
'''


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
