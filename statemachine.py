import logging


class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startstate = None
        self.endstates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        logging.debug('Adding state %s.' % name)
        self.handlers[name] = handler
        if end_state:
            logging.debug('%s is an end state.' % name)
            self.endstates.append(name)

    def set_start(self, name):
        self.startstate = name.upper()
        logging.debug('Setting %s as start state.' % self.startstate)

    def run(self, cargo):
        logging.debug('Running StateMachine containing %d states.',
                      len(self.handlers))
        try:
            handler = self.handlers[self.startstate]
        except:
            raise ValueError("must call .set_start() before .run()")
        if not self.endstates:
            raise ValueError("at least one state must be an end_state")

        while True:
            current_state = handler.__name__.upper()
            logging.debug('Current state is %s.', current_state)
            (new_state, cargo) = handler(cargo)
            new_state = new_state.upper()
            if current_state != new_state:
                logging.debug('Switching to state %s.', new_state)
            if new_state in self.endstates:
                logging.debug("Exiting as we reached end state %s.",
                              new_state)
                break
            else:
                handler = self.handlers[new_state]
