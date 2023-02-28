from ...components.vcvs import VCVS
from ...components.vccs import VCCS
from ...components.ccvs import CCVS
from ...components.cccs import CCCS
from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class CptPropertiesDialog:

    def __init__(self, ui, cpt, update=None, title=''):

        self.cpt = cpt
        self.gcpt = cpt.gcpt
        self.update = update
        self.ui = ui

        self.master = Tk()
        self.master.title(title)

        entries = []
        if self.gcpt.kinds != {}:
            kind_name = self.gcpt.kinds[self.gcpt.kind]
            entries.append(LabelEntry(
                'kind', 'Kind', kind_name, list(self.gcpt.kinds.values()),
                command=self.on_update))

        if self.gcpt.styles != {}:
            style_name = self.gcpt.styles[self.gcpt.style]
            entries.append(LabelEntry(
                'style', 'Style', style_name, list(self.gcpt.styles.values()),
                command=self.on_update))

        entries.append(LabelEntry('name', 'Name', self.cpt.name,
                                  command=self.on_update))
        entries.append(LabelEntry('value', 'Value', self.gcpt.value,
                                  command=self.on_update))

        if cpt.is_capacitor:
            entries.append(LabelEntry(
                'initial_value', 'v0', self.gcpt.initial_value,
                command=self.on_update))
        elif cpt.is_inductor:
            entries.append(LabelEntry(
                'initial_value', 'i0', self.gcpt.initial_value,
                command=self.on_update))
        elif isinstance(cpt, (VCVS, VCCS, CCVS, CCCS)):
            names = [c.name for c in ui.model.components if c.name[0] != 'W']
            entries.append(LabelEntry('control', 'Control',
                                      self.gcpt.control, names,
                                      command=self.on_update))

        for k, v in self.gcpt.fields.items():
            entries.append(LabelEntry(k, v, getattr(self.gcpt, k),
                                      command=self.on_update))

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_update(self, arg=None):

        if self.gcpt.kinds != {}:
            self.gcpt.kind = self.gcpt.inv_kinds[self.labelentries.get(
                'kind')]

        if self.gcpt.styles != {}:
            self.gcpt.style = self.gcpt.inv_styles[self.labelentries.get(
                'style')]

        name = self.labelentries.get('name')
        if name.startswith(self.gcpt.name[0]):
            self.gcpt.name = self.labelentries.get('name')
        else:
            self.ui.show_error_dialog('Cannot change component type')

        self.gcpt.value = self.labelentries.get('value')

        try:
            self.gcpt.initial_value = self.labelentries.get(
                'initial_value')
        except KeyError:
            pass

        try:
            self.gcpt.control = self.labelentries.get('control')
        except KeyError:
            pass

        for k, v in self.gcpt.fields.items():
            setattr(self.gcpt, k, self.labelentries.get(k))

        if self.update:
            self.update(self.cpt)

    def on_ok(self):

        self.on_update()

        self.master.destroy()
