#!/bin/python
"""
DFA Reader

This script reads in a DFA and is able to tell whether the given strings
are in the language of the DFA.

The DFA must be given as a JSON file in the below format:
    {
        "Sigma": <List of the characters in the alphabet>,
        "InitialState": <String of the name of the initial state of the DFA>,
        "AcceptingStates": <List of accepting states>,
        "States": {
            <STATE>: <Object mapping each character in sigma to a state>
        }
    }

Below is an example DFA which tells whether or not a string in the alphabet
of {a, b} contains the substring "ab":
    {
        "Sigma": ["a", "b"],
        "InitialState": "q0",
        "AcceptingStates": ["q2"],
        "States": {
            "q0": {"a": "q1", "b": "q0"},
            "q1": {"b": "q2", "a": "q1"},
            "q2": {"a": "q2", "b": "q2"}
        }
    }
"""
import json
import argparse


class DFAParseError(Exception):
    """
    DFA Parsing Error
    """
    pass


class DeltaException(Exception):
    """
    Exception thrown if the delta method encounters an error
    """
    pass


class DFA(object):
    """
    DFA Representation Class
    """
    def __init__(self, states, sigma, transitions, init_state, accepting):
        """
        DFA Class Constructor

        NOTE: This assumes that that the given information is a good DFA.

        Arguments:
            states      - List of states of the DFA
            sigma       - Alphabet of the DFA
            transitions - Transitions between the state in the DFA
            init_state  - Initial state of the DFA
            accepting   - Accepting states of the DFA
        """
        self.sigma = sigma
        self.states = states
        self.init_state = init_state
        self.accepting = accepting
        self.transitions = transitions

    def __str__(self):
        """
        String representation of the DFA
        """
        return \
            ("===== DFA =====\n"
             "  Q             : {q}\n"
             "  Sigma         : {sigma}\n"
             "  Initial State : {init_state}\n"
             "  Accepting     : {accepting}\n"
             "  Transitions   : {transitions}\n")\
            .format(
                sigma=self.sigma,
                q=self.states,
                init_state=self.init_state,
                accepting=self.accepting,
                transitions=self.transitions)

    def delta(self, state, value):
        """
        Delta method - transitions from the given state to the next state
        based on the given value.

        Returns the state mapped to.

        Throws a DeltaException if a problem is encountered.

        Arguments:
            state - State to transition from
            value - Value to use to determine next state
        """
        try:
            return self.transitions[state][value]
        except KeyError as e:
            raise DeltaException(
                ("Either the given state does not exist, or the value "
                "is not in the alphabet: state = {0}, value = {1}")
                .format(state, value))

    def is_in_language(self, string):
        """
        Checks if the given string is in the language of the DFA. If an error
        is encountered a DeltaException will be thrown.

        Returns a tuble (in DFA, path), where the first value is True or False
        for whether the given string is in the language represented by the
        DFA, and the second is the path that the DFA used to determin the
        answer.

        Arguments:
            string - String with only characters in sigma to check if is in
                     the language described by this DFA.
        """
        curr_state = self.init_state
        path = [curr_state]

        for a in string:
            curr_state = self.delta(curr_state, a)
            path.append(curr_state)

        return curr_state in self.accepting, path


def parse_dfa(contents):
    """
    Parse the DFA - returns a DFA object.

    Throws a DFAParseError if a problem is encountered with the given DFA.

    Arguments:
        contents - Dictionary describing the DFA
    """
    dfa = None
    try:
        # Getting the alphabet of the DFA and the intial state
        sigma = contents["Sigma"]
        init_state = contents["InitialState"]
        accepting_states = contents["AcceptingStates"]

        # Getting list of all states
        states = contents["States"].keys()

        # Verifying the initial state
        assert init_state in states, \
            "Initial state \"{0}\" is not in the list of states"\
            .format(init_state)

        if accepting_states:
            # Verifying that the accepting states are in the list of states
            assert set(accepting_states).issubset(set(states)), \
                "Accepting states are not in the set of states"

        # Verifying the states/state transitions
        for state in states:
            transitions = contents["States"][state]

            # Verifying that the state handles the entire alphabet
            assert transitions.keys() == sigma, \
                "State \"{0}\" does not handle the entire alphabet (Sigma)"\
                .format(state)

            # Verifying that the states to go to on a value are all valid
            assert set(transitions.values()).issubset(set(states)), \
                "Not all transition states are in set of states"

        dfa = DFA(states, sigma, contents["States"], init_state, accepting_states)
    except KeyError as e:
        raise DFAParseError("DFA Specification Missing Key: " + e)
    except AssertionError as e:
        raise DFAParseError(e.message)

    return dfa


def parse_args():
    """
    Parses the command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-show-path", action="store_true", default=False,
        help="Show the path of states taken for each string")
    parser.add_argument("dfa_file", type=str,
        help="JSON file describing the DFA")
    parser.add_argument("strings", nargs="+",
        help="Strings to check if are in the DFA")
    return parser.parse_args()


def main():
    """
    Main Method
    """
    # Parsing the command line arguments
    args = parse_args()

    try:
        print "=> Parsing the DFA"
        # Reading in the DFA
        with open(args.dfa_file, "r") as f:
            contents = json.load(f)
        dfa = parse_dfa(contents)
        print "=> DFA Created"
        print dfa
        print "=> Processing Strings....\n"

        for s in args.strings:
            in_dfa, path = dfa.is_in_language(s)
            if in_dfa:
                print "==> String \"{0}\" is in the language".format(s)
            else:
                print "==> String \"{0}\" is not in the language".format(s)

            if args.show_path:
                print "\tPath: ", "->" + "->".join(path)
    except IOError:
        print "=> Error: \"" + args.dfa_file + "\" does not exist"
    except (DFAParseError, DeltaException) as e:
        print "=> Error: " + e.message


if __name__ == "__main__":
    main()
