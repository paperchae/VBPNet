import torch
import torch.nn as nn
from nets.modules.sub_modules.Trend_module import Trend_module_1D
from nets.modules.sub_modules.Detail_module import Detail_module_1D
from nets.modules.sub_modules.Linear_module import Linear_module_1D
from nets.modules.sub_modules.Amplitude_module import Amplitude_module


class bvp2abp(nn.Module):
    def __init__(self, in_channels):
        super(bvp2abp, self).__init__()
        self.in_channel = in_channels

        self.trend_model = Trend_module_1D(self.in_channel)
        self.detail_model = Detail_module_1D(self.in_channel)
        self.linear_model = Linear_module_1D()
        self.amplitude_model = Amplitude_module()



    def forward(self, ple_input):
        ple_input = torch.reshape(ple_input, (-1, self.in_channel, 360))  # [ batch , channel, size]
        # at1, at2 = self.detail_model.forward(ple_input)
        # t_out = self.trend_model.forward(ple_input, at1, at2)
        # l_out = self.linear_model.forward(t_out)
        # dbp, sbp = self.amplitude_model.forward(t_out)
        at1, at2 = self.trend_model.forward(ple_input)
        d_out = self.detail_model.forward(ple_input,at1,at2)
        l_out = self.linear_model.forward(d_out)
        dbp, sbp = self.amplitude_model.forward(d_out)

        return l_out, dbp, sbp
