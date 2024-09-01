from .fixed import Fixed


class ADC(Fixed):

    type = "Uadc"
    sketch_net = 'U adc'
    sketch_key = 'adc'
    label_offset_pos = (0, 0)
    anotation_offset_pos = None

    pins = {'in': ('l', -0.5, 0),
            'in+': ('l', -0.4375, 0.125),
            'in-': ('l', -0.4375, -0.125),
            'vref-': ('l', -0.375, -0.25),
            'vref+': ('l', -0.375, 0.25),
            'avss': ('b', -0.1, -0.5),
            'vss': ('b', 0.1, -0.5),
            'dvss': ('b', 0.3, -0.5),
            'clk': ('r', 0.5, -0.25),
            'data': ('r', 0.5, 0),
            'fs': ('r', 0.5, 0.25),
            'dvdd': ('t', 0.3, 0.5),
            'vdd': ('t', 0.1, 0.5),
            'avdd': ('t', -0.1, 0.5)}
