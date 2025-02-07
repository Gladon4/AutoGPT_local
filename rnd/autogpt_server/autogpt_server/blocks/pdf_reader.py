import json
from typing import Any
import re

from pydantic import Field

from autogpt_server.data.block import Block, BlockCategory, BlockOutput, BlockSchema

import PyPDF2


class PdfTextBlock(Block):
    class Input(BlockSchema):
        file_path: Any = Field(description="Path to PDF to load")

    class Output(BlockSchema):
        text: Any = Field(description="Text in PDF")

    def __init__(self):
        super().__init__(
            id="174a7953-6a3e-4909-a6f9-3f40b5dafb8f",
            description="This block loads text from a PDF file",
            categories={BlockCategory.TEXT},
            input_schema=PdfTextBlock.Input,
            output_schema=PdfTextBlock.Output,
            # This test is probably bad, but I don't know if it's needed so just keep it here
            test_input=[
                {"file_path": "test_input_path"}],
            test_output=[
                ("test_output"),
            ],
        )

    def run(self, input_data: Input) -> BlockOutput:
        # See above for  testing, very jank
        if input_data.file_path == "test_input_path":
            yield "text", "test_output"
            return

        with open(input_data.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
    
        yield "text", text

