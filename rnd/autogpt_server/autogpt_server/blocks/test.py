from autogpt_server.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from pydantic import Field
from typing import Any
import requests


class TestBlock(Block):
    class Input(BlockSchema):
        text: str = Field(description="Input Text")
        hostname: str = Field(description="Hostname", default="localhost")
        port: int = Field(description="Port", default=8080)

    class Output(BlockSchema):
        output: str = Field(description="Output Text")

    def __init__(self):
        super().__init__(
            id="2045ccca-dd8f-484e-9c75-b9d2ff0cb2b9",
            description="This is a test block for testing purposes.",
            categories={BlockCategory.TEXT},
            input_schema=TestBlock.Input,
            output_schema=TestBlock.Output,
            test_input=[
                {"text": "Hello"}
            ],
            test_output=[
                ("output", "World!")
            ],
        )

    def run(self, input_data: Input) -> BlockOutput:
        params = {"key1": input_data.text}
        url = "http://" + input_data.hostname + ":" + str(input_data.port)

        response = requests.get(url, params=params).text
        yield "output", response


"""Test Server for this:
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

hostName = "localhost"
serverPort = 8080

responses = {"Hello": "World!", "Java": "Script", "C": "is best"}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = []
        for p in params:
            response.append({"request": params[p][0], "response": responses.get(params[p][0], "#")})
            # print(params[p][0], responses.get(params[p][0], "#"))
            
        self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
"""