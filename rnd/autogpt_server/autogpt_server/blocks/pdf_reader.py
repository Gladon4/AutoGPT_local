import json
from typing import Any

from pydantic import Field

from autogpt_server.data.block import Block, BlockCategory, BlockOutput, BlockSchema

import PyPDF2


class PdfInput(Block):
    class Input(BlockSchema):
        file_path: Any = Field(description="Path to PDF to load")

    class Output(BlockSchema):
        text: Any = Field(description="Text in PDF")

    def __init__(self):
        super().__init__(
            id="f4728aeb-5774-4516-bf48-86c6093d1bed",
            description="This block loads text from a PDF file",
            categories={BlockCategory.TEXT},
            input_schema=PdfInput.Input,
            output_schema=PdfInput.Output,
            # test_input=[
            #     {"text": "ABC", "match": "ab", "data": "X", "case_sensitive": False},
            #     {"text": "ABC", "match": "ab", "data": "Y", "case_sensitive": True},
            #     {"text": "Hello World!", "match": ".orld.+", "data": "Z"},
            #     {"text": "Hello World!", "match": "World![a-z]+", "data": "Z"},
            # ],
            # test_output=[
            #     ("positive", "X"),
            #     ("negative", "Y"),
            #     ("positive", "Z"),
            #     ("negative", "Z"),
            # ],
        )

    def run(self, input_data: Input) -> BlockOutput:
        with open(input_data.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
    
        yield "output", text

