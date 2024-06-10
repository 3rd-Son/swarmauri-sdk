import re
from typing import List, Union, Any
from swarmauri.standard.documents.concrete.Document import Document
from swarmauri.standard.parsers.base.ParserBase import ParserBase

class RegExParser(ParserBase):
    """
    A parser that uses a regular expression to extract information from text.
    """
    pattern: str
    
    def parse(self, data: Union[str, Any]) -> List[Document]:
        """
        Parses the input data using the specified regular expression pattern and
        returns a list of IDocument instances containing the extracted information.

        Parameters:
        - data (Union[str, Any]): The input data to be parsed. It can be a string or any format 
                                   that the concrete implementation can handle.

        Returns:
        - List[IDocument]: A list of IDocument instances containing the parsed information.
        """
        # Ensure data is a string
        if not isinstance(data, str):
            data = str(data)

        # Use the regular expression pattern to find all matches in the text
        matches = re.findall(self.pattern, data)

        # Create a Document for each match and collect them into a list
        documents = [Document(content=match, metadata={}) for i, match in enumerate(matches)]

        return documents