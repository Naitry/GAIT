import json
import array
from typing import Any, Callable, Dict, Tuple, Union, get_args, get_origin, get_type_hints, Optional
import inspect


class gptAssistant(object):
    def __init__ (self) -> None:
        self.name: str = ""
        self.instructions: str = ""


def pythonTypeToJsonSchema(pythonType: Any) -> str:
    """
    Converts Python type annotations to JSON schema types.

    :param pythonType: A Python type or type annotation.
    :return: A string representing the JSON schema type.
    """
    # Define a mapping of Python types to JSON schema types
    typeMapping = {
        bool: 'boolean',
        int: 'integer',
        float: 'number',
        str: 'string',
        type(None): 'null'  # Handle the NoneType for optional type annotations
    }

    # If the type is directly in the mapping, return it
    if pythonType in typeMapping:
        return typeMapping[pythonType]

    # Handle generic types from typing module
    originType = get_origin(pythonType)
    if originType:
        # Example for List, Dict; you can extend this as needed
        if issubclass(originType, list):
            return 'array'
        elif issubclass(originType, dict):
            return 'object'

    # If a custom mapping for a user-defined class is needed
    if hasattr(pythonType, '__name__'):
        customTypeMapping = {
            # 'CustomClass': 'object',  # Example of a custom class to JSON type
            # You can add more custom mappings here
        }
        return customTypeMapping.get(pythonType.__name__, 'string')

    # If the type is a typing.Union or similar, you might want to handle it differently
    # For example, Optional[int] could be translated as type: ['integer', 'null']

    # Fallback to a string type if not specified or unknown
    return 'string'




def parseDocstring(docstring: str) -> dict:
    """
    Parses the docstring to find parameter descriptions and additional metadata.

    :param docstring: The docstring from which to extract parameter descriptions and metadata.
    :return: A dictionary with parameter names as keys and their descriptions and metadata as values.
    """
    lines = docstring.split('\n')
    paramDescriptions = {}
    currentParam = None
    currentKey = None

    for line in lines:
        line = line.strip()
        if line.startswith(':param'):
            _, param_name = line.split(' ', 1)
            currentParam, _ = param_name.split(':', 1)
            currentParam = currentParam.strip()
            paramDescriptions[currentParam] = {'description': ''}
            currentKey = 'description'
        elif line.startswith('-'):
            # This line contains additional metadata for the parameter
            if currentParam:
                meta_parts = line.lstrip('- ').split(': ', 1)
                if len(meta_parts) == 2:
                    key, value = meta_parts
                    key = key.strip()
                    value = value.strip()
                    # Cast the value to the appropriate type
                    if key in ['minimum', 'maximum', 'default']:
                        try:
                            value = float(value) if '.' in value else int(value)
                        except ValueError:
                            pass  # If casting fails, retain the string value
                    paramDescriptions[currentParam][key] = value
                    currentKey = key
        elif currentParam and currentKey:
            # Continue the current parameter's description or metadata
            if isinstance(paramDescriptions[currentParam][currentKey], str):
                paramDescriptions[currentParam][currentKey] += line.strip()

    # Strip any extra whitespace from the descriptions
    for param, desc in paramDescriptions.items():
        desc['description'] = desc['description'].strip()

    return paramDescriptions


def generateParamProperties(name: str, param: inspect.Parameter, paramDescriptions: Dict[str, Any]) -> Dict[str, Any]:
    # Check if the annotation is a class and extract the name, otherwise default to 'Any'
    if param.annotation != inspect._empty and hasattr(param.annotation, '__name__'):
        paramType = param.annotation.__name__
    else:
        paramType = 'Any'

    paramDescription = paramDescriptions.get(name, {}).get('description')
    type: str = pythonTypeToJsonSchema(param.annotation)

    if type != "array":
        return  {
                "type": type,
                "description": paramDescription
                }
    else:
        itemType = get_args(param.annotation)[0] if get_args(param.annotation) else 'Any'
        itemJsonType: str = pythonTypeToJsonSchema(itemType)

        return  {
                "type": type,
                "description": paramDescription
                }


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

        properties[name] = generateParamProperties(name, param, paramDescriptions)
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

def exampleFunction(decision: bool, confidence: float, reasoning: str = "") -> str:
    """
    Forces the AI to make a yes/no choice on the situation at hand.

    :param decision:
        The answer to the decision, true for yes, false for no.
    :param confidence:
        Floating point confidence values of the decisions.
        - minimum: 0.0
        - maximum: 100.0
    :param reasoning:
        The justification as to why the decision was made.

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
