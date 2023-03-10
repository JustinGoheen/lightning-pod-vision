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

import torch
from visionpod.core.module import Decoder, Encoder, PodModule


def test_module_not_abstract():
    _ = PodModule()


def test_module_forward():
    input_sample = torch.randn((1, 784))
    model = PodModule()
    preds, label = model.forward(input_sample)
    assert preds.shape == input_sample.shape


def test_module_training_step():
    input_sample = torch.randn((1, 784)), 1
    model = PodModule()
    loss = model.training_step(input_sample)
    assert isinstance(loss, torch.Tensor)


def test_optimizer():
    model = PodModule()
    optimizer = model.configure_optimizers()
    optimizer_base_class = optimizer.__class__.__base__.__name__
    assert optimizer_base_class == "Optimizer"


def test_encoder_not_abstract():
    _ = Encoder()


def test_encoder_forward():
    input_sample = torch.randn((1, 784))
    model = Encoder()
    output = model.forward(input_sample)
    assert output.shape == torch.Size([1, 3])


def test_decoder_not_abstract():
    _ = Decoder()


def test_decoder_forward():
    input_sample = torch.randn((1, 3))
    model = Decoder()
    output = model.forward(input_sample)
    assert output.shape == torch.Size([1, 784])
