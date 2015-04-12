# DFAReader
This script reads in a DFA and is able to tell whether the given strings are in the language of the DFA.

# DFA Specification
The script uses a JSON file to specify the DFA.  Below is the specification for the JSON file.

```
{
    "Sigma": <List of the characters in the alphabet>,
    "InitialState": <String of the name of the initial state of the DFA>,
    "AcceptingStates": <List of accepting states>,
    "States": {
        <STATE>: <Object mapping each character in sigma to a state>
    }
}
```

Below is an example DFA which tells whether or not a string in the alphabet of {a, b} contains the substring "ab":
```json
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
```

# Command Line Usage
Below is the help for the command line:
```sh
usage: dfa_reader.py [-h] [-show-path] dfa_file strings [strings ...]

positional arguments:
  dfa_file    JSON file describing the DFA
  strings     Strings to check if are in the DFA

optional arguments:
  -h, --help  show this help message and exit
  -show-path  Show the path of states taken for each string
```

# License
This code is provided AS-IS with no support or warranty.
