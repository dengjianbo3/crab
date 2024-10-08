# =========== Copyright 2024 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ CAMEL-AI.org. All Rights Reserved. ===========
import base64
import io
import json
from typing import Any, Dict, List, Optional, Tuple, Union

from PIL import Image

from crab import Action, ActionOutput, BackendModel, BackendOutput, MessageType
from crab.utils.common import base64_to_image

try:
    from camel.agents import ChatAgent
    from camel.configs import ChatGPTConfig
    from camel.messages import BaseMessage
    from camel.models import ModelFactory
    from camel.toolkits import OpenAIFunction
    from camel.types.enums import ModelPlatformType, ModelType

    CAMEL_ENABLED = True
except ImportError:
    CAMEL_ENABLED = False


def find_model_platform_type(model_platform_name: str) -> ModelPlatformType:
    for platform in ModelPlatformType:
        if platform.value.lower() == model_platform_name.lower():
            return platform
    all_models = [platform.value for platform in ModelPlatformType]
    raise ValueError(
        f"Model {model_platform_name} not found. Supported models are {all_models}"
    )


def find_model_type(model_name: str) -> Union[ModelType, str]:
    for model in ModelType:
        if model.value.lower() == model_name.lower():
            return model
    return model_name


def decode_image(encoded_image: str) -> Image:
    data = base64.b64decode(encoded_image)
    return Image.open(io.BytesIO(data))


class CamelModel(BackendModel):
    def __init__(
        self,
        model: str,
        model_platform: str,
        parameters: Optional[Dict[str, Any]] = None,
        history_messages_len: int = 0,
    ) -> None:
        if not CAMEL_ENABLED:
            raise ImportError("Please install camel-ai to use CamelModel")
        self.parameters = parameters or {}
        # TODO: a better way?
        self.model_type = find_model_type(model)
        self.model_platform_type = find_model_platform_type(model_platform)
        self.client: Optional[ChatAgent] = None
        self.token_usage = 0

        super().__init__(
            model,
            parameters,
            history_messages_len,
        )

    def get_token_usage(self):
        return self.token_usage

    def reset(self, system_message: str, action_space: Optional[List[Action]]) -> None:
        action_schema = self._convert_action_to_schema(action_space)
        config = self.parameters.copy()
        if action_schema is not None:
            config["tool_choice"] = "required"
            config["tools"] = action_schema

        chatgpt_config = ChatGPTConfig(
            **config,
        )
        backend_model = ModelFactory.create(
            self.model_platform_type,
            self.model_type,
            model_config_dict=chatgpt_config.as_dict(),
        )
        sysmsg = BaseMessage.make_assistant_message(
            role_name="Assistant",
            content=system_message,
        )
        self.client = ChatAgent(
            model=backend_model,
            system_message=sysmsg,
            external_tools=action_schema,
            message_window_size=self.history_messages_len,
        )
        self.token_usage = 0

    @staticmethod
    def _convert_action_to_schema(
        action_space: Optional[List[Action]],
    ) -> Optional[List[OpenAIFunction]]:
        if action_space is None:
            return None
        return [OpenAIFunction(action.entry) for action in action_space]

    @staticmethod
    def _convert_tool_calls_to_action_list(tool_calls) -> List[ActionOutput]:
        if tool_calls is None:
            return tool_calls

        return [
            ActionOutput(
                name=call.function.name,
                arguments=json.loads(call.function.arguments),
            )
            for call in tool_calls
        ]

    def chat(self, messages: List[Tuple[str, MessageType]]):
        # TODO: handle multiple text messages after message refactoring
        image_list: List[Image.Image] = []
        content = ""
        for message in messages:
            if message[1] == MessageType.IMAGE_JPG_BASE64:
                image = base64_to_image(message[0])
                image_list.append(image)
            else:
                content = message[0]
        usermsg = BaseMessage.make_user_message(
            role_name="User",
            content=content,
            image_list=image_list,
        )
        response = self.client.step(usermsg)
        self.token_usage += response.info["usage"]["total_tokens"]
        tool_call_request = response.info.get("tool_call_request")

        # TODO: delete this after record_message is refactored
        self.client.record_message(response.msg)

        return BackendOutput(
            message=response.msg.content,
            action_list=self._convert_tool_calls_to_action_list([tool_call_request]),
        )
