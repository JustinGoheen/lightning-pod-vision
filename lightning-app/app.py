# Copyright Justin R. Goheen.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from lightning import LightningApp, LightningFlow
from lightning.app.frontend import StaticWebFrontend


class ReactUI(LightningFlow):
    def __init__(self):
        super().__init__()

    def configure_layout(self):
        return StaticWebFrontend(Path(__file__).parents[1] / "react-ui/build/")


class RootFlow(LightningFlow):
    def __init__(self):
        super().__init__()
        self.react_ui = ReactUI()

    def run(self):
        self.react_ui.run()

    def configure_layout(self):
        return [{"name": "ReactUI", "content": self.react_ui}]


app = LightningApp(RootFlow())
