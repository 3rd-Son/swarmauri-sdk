import logging
import json
from typing import List, Literal
from typing import List, Dict, Any, Literal
import cohere
from swarmauri.core.typing import SubclassUnion

from swarmauri.standard.messages.base.MessageBase import MessageBase
from swarmauri.standard.messages.concrete.AgentMessage import AgentMessage
from swarmauri.standard.messages.concrete.FunctionMessage import FunctionMessage
from swarmauri.standard.llms.base.LLMBase import LLMBase
from swarmauri.standard.schema_converters.concrete.CohereSchemaConverter import CohereSchemaConverter

class CohereToolModel(LLMBase):
    api_key: str
    allowed_models: List[str] = ['command-light',
    'command', 
    'command-r',
    'command-r-plus']
    name: str = "command-light"
    type: Literal['CohereToolModel'] = 'CohereToolModel'
    
    def _schema_convert_tools(self, tools) -> List[Dict[str, Any]]:
        return [CohereSchemaConverter().convert(tools[tool]) for tool in tools]

    def _format_messages(self, messages: List[SubclassUnion[MessageBase]]) -> List[Dict[str, str]]:
        message_properties = ['content', 'role', 'name', 'tool_call_id', 'tool_calls']
        formatted_messages = [message.model_dump(include=message_properties, exclude_none=True) for message in messages]
        return formatted_messages

    def predict(self, 
        conversation, 
        toolkit=None, 
        force_single_step = False,
        max_tokens=1024):

        formatted_messages = self._format_messages(conversation.history)

        client = cohere.Client(api_key=self.api_key)
        preamble = "" # 🚧  Placeholder for implementation logic

        response = client.chat(
            chat_history=formatted_messages[:-1],
            model=self.name, 
            message=formatted_messages[-1], 
            force_single_step=False, 
            tools=self._schema_convert_tools(toolkit.tools)
        )

        logging.info(f"response: {response}")
        # as long as the model sends back tool_calls,
        # keep invoking tools and sending the results back to the model
        while response.tool_calls:
          logging.debug(response.text) # This will be an observation and a plan with next steps
          tool_results = []
          for call in response.tool_calls:
            logging.debug(call)
            # use the `web_search` tool with the search query the model sent back
            def fn(value):
                return value
            results = {"call": call, "outputs": fn(call.parameters["query"])} # 🚧  Placeholder to determine how to find function and call it
            tool_results.append(results)
            
        # call chat again with tool results
        response = client.chat(
            model=self.name,
            chat_history=response.chat_history,
            message="",
            force_single_step=force_single_step,
            tools=self._schema_convert_tools(toolkit.tools),
            tool_results=tool_results
        )

        logging.info(f"response: {response}")
        conversation.add_message(AgentMessage(content=response.text))

        logging.info(f"conversation: {conversation}")
        return conversation
