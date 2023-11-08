import inspect
import json
from typing import Any, Callable


class gptAssistant(object):
    def __init__ (self) -> None:
        self.name: str = ""
        self.instructions: str = ""

def parseDocstring(docstring: str) -> dict:
    """
    Parses the docstring to find parameter descriptions and additional metadata.

    :param docstring: The docstring from which to extract parameter descriptions and metadata.
    :return: A dictionary with parameter names as keys and their descriptions and metadata as values.
    """
    lines = docstring.split('\n')
    paramDescriptions = {}
    currentParam = None
    currentMetadata = None

    for line in lines:
        line = line.strip()
        if line.startswith(':param'):
            parts = line.split(':')
            if len(parts) >= 3:
                currentParam = parts[2].strip().split(' ')[0]
                paramDescriptions[currentParam] = {'description': parts[2].strip()[len(currentParam) + 1:].strip()}
                currentMetadata = paramDescriptions[currentParam]
        elif currentParam and line.startswith('-'):
            metadata_parts = line[1:].strip().split(': ')
            if len(metadata_parts) == 2:
                key, value = metadata_parts
                if key in ['minimum', 'maximum', 'default']:
                    try:
                        value = float(value) if '.' in value else int(value)
                    except ValueError:
                        pass  # Handle the case where the value is not a valid number
                currentMetadata[key] = value
        elif currentParam and line and not line.startswith(':'):
            # Ensures currentMetadata is not None before attempting to append to description
            if currentMetadata is not None:
                currentMetadata['description'] += ' ' + line
            else:
                # This branch should not be normally reached if the docstring is well-formed
                print(f"Warning: Unexpected line in docstring for parameter {currentParam}: {line}")

    return paramDescriptions


def generateToolsConfig(function: Callable) -> str:
    """
    Generates the 'tools' section of the OpenAI API configuration for a given function.

    :param function: A callable function to generate the tools configuration for.
    :return: A JSON string representing the tools configuration.
    """
    signature = inspect.signature(function)
    docstring = inspect.getdoc(function) or "No description provided."
    functionName = function.__name__
    paramDescriptions = parseDocstring(docstring)

    # Prepare the list for 'required' fields
    requiredList = [name for name, param in signature.parameters.items() if param.default is inspect.Parameter.empty]

    properties = {}
    for name, param in signature.parameters.items():
        paramType = str(param.annotation) if param.annotation != inspect._empty else 'Any'
        paramDescription = paramDescriptions.get(name, {}).get('description', f"Description for {name}.")

        properties[name] = {
            "type": "string" if paramType == 'Any' else paramType.lower(),
            "description": paramDescription
        }
        # Add additional metadata if present
        if 'minimum' in paramDescriptions.get(name, {}):
            properties[name]['minimum'] = paramDescriptions[name]['minimum']
        if 'maximum' in paramDescriptions.get(name, {}):
            properties[name]['maximum'] = paramDescriptions[name]['maximum']

    tool = {
        "type": "function",
        "function": {
            "name": functionName,
            "description": docstring,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": requiredList
            }
        }
    }

    return json.dumps(tool, indent=4)

def exampleFunction(decision: bool, confidence: float = 1.0, reasoning: str = "") -> str:
    """
    Forces the AI to make a yes/no choice on the situation at hand.

    :param decision:
        The answer to the decision, true for yes, false for no.
    :param confidence:
        Floating point confidence value of the decision.
        - type: number
        - minimum: 0
        - maximum: 1
        - default: 1.0
    :param reasoning:
        The justification as to why the decision was made.
        - type: string

    :return: A string explaining the decision.
    """
    return "Decision made."

"""
[{
    "type": "function",
    "function": {
        "name": "makeDecision",
        "description": "Forces the AI to make a yes no choice on the situation at hand.",
        "parameters": {
            "type": "object",
            "properties": {
                "decision": {"type": "boolean",
                             "description": "The answer to the decision, true for yes, false for no."},
                "confidence": {"type": "number",
                               "minimum": 0,
                               "maximum": 1,
                               "description": "Floating point confidence value of the decision, 1 for totally confident, 0 for not confident at all, and all percentage values inbetween"},
                "reasoning": {
                    "type": "string",
                    "description": "The justification as to why the decision was made."}
                },
            "required": [
                "decision"
                ]
            }
        }
    }]
"""
