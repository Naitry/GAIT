from typing import Optional


def readMarkdownFile(filePath: str) -> Optional[str]:
	"""
  Reads the content of a Markdown file and returns it as a single string.

  Args:
	  filePath (str): The path to the Markdown file.

  Returns:
	  Optional[str]: The content of the Markdown file as a single string, or None if the file could not be read.
  """
	try:
		with open(filePath,
				  'r',
				  encoding='utf-8') as file:
			content: str = file.read()
		return content
	except FileNotFoundError:
		print(f"File {filePath} not found.")
		return None
	except Exception as e:
		print(f"An error occurred: {e}")
	return None
