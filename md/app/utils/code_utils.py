import re

def extract_code_and_text(response_text):
    """
    Extracts text and code blocks from the generated response.
    Returns a list of dictionaries with each part labeled as either 'text' or 'code'.
    """
    code_pattern = r'```python\n(.*?)```|([^`]+)' # Regex to match code blocks, optionally with a language like python
    parts = []
    
    # Split response by code blocks
    matches = re.findall(code_pattern, response_text, re.DOTALL)
    # Go through the matches and alternate between text and code
    i = 0
# List to store the results
    content_list = []

    # Separate text and code
    for match in matches:
        if match[0]:  # if it's a code block
            content_list.append({'type': 'code', 'content': match[0]})
        elif match[1].strip():  # if it's a text block and not empty
            content_list.append({'type': 'text', 'content': match[1].strip()})
        #i += 1

    print(f"Content list: {content_list}")
    return content_list
