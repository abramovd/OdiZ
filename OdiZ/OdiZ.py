from __future__ import division
try:
    from Tkinter import *
    import ttk
    from tkFileDialog import askopenfilename, asksaveasfilename
except ImportError:
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename, asksaveasfilename

import re
import math

from arithmetic.Zsum import Zsum
from arithmetic.Zsub import Zsub
from arithmetic.Zprod import Zprod
from arithmetic.Zmin import Zmin
from arithmetic.Zmax import Zmax
from arithmetic.Zdiv import Zdiv
from arithmetic.Zsum import Zsum

import matplotlib
matplotlib.use("TkAgg")
#import FileDialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import time
import numpy as np
import numpy
import scipy as sp
from scipy.sparse.csgraph import _validation
from scipy.optimize import minimize
np.seterr(invalid='ignore')

TEXT_WIDTH = 20
TEXT_HEIGHT = 5
DPI = 700

def nan_to_zeros(xList, yList):
    for i in xrange(len(xList)):
        if math.isnan(xList[i]):
            xList[i] = 0
        if math.isnan(yList[i]):
            yList[i] = 0

def formating(number):
    eps = 0.00005
    if abs(number) < eps:
        number = float(format(number, '.4f'))
    elif number != np.NaN:
        number = float(format(number, '.4f'))
    return number

def tostr(li):
    res = ''
    for el in li:
        res += ', ' + str(el)
    if len(res) > 2:
        return res[2:]
    else:
        return ''

class Znumber:
    def __init__(self, A = [], As = [], B = [], Bs = []):
        self.A = A
        self.As = As
        self.B = B
        self.Bs = Bs
        if not self.validate():
            return None

    def validate(self):
        try:
            if len(self.A) != len(self.As) or len(self.A) != len(self.B) or len(self.A) != len(self.Bs):
                raise ValueError('Error - [A, As, B, Bs]: same sizes of sets expected')
            return True
        except ValueError as e:
            print(e)
            return False

class PartOfZnumber_GUI:
    def __init__(self, frame = None, part_name = ''):
        self.clicked = False
        if frame != None:
            self.text = Text(frame, width = TEXT_WIDTH, height = TEXT_HEIGHT)
            self.text.bind("<FocusIn>", lambda event: self.callbackZ())
            self.text.insert("1.0", "Part " + part_name)

    def callbackZ(self):
        if self.clicked == False:
            self.text.delete("1.0", END)
            self.clicked = True

    def get(self):
        return self.text

    def validate(self, number, part):
        format = r'^[-+]?[0-9]*\.?[0-9]+(?:,[-+]?[0-9]*\.?[0-9]+?|)+$'
        text = self.text.get("1.0", END).replace(" ", "")
        if len(text) == 0 or re.match(format, text) == None:
            raise ValueError('Error - ' + number + '[' + part + ']: bad format / mismatch')
        return

class Znumber_GUI:
        def __init__(self, frame = None):
            self.A = None
            self.As = None
            self.B = None
            self.Bs = None
            parts = ['A', 'As', 'B', 'Bs']
            self.plotted = dict(zip(['A', 'B'], [False, False]))
            if frame != None:
                for part in parts:
                    z_part = PartOfZnumber_GUI(frame, part)
                    setattr(self, part, z_part)

        def delete_spaces(self):
             self.new_A = self.A.text.get("1.0", END).replace(" ", "")
             self.new_As = self.As.text.get("1.0", END).replace(" ", "")
             self.new_B = self.B.text.get("1.0", END).replace(" ", "")
             self.new_Bs = self.Bs.text.get("1.0", END).replace(" ", "")

        def validate(self, number):
            format = r'^[-+]?[0-9]*\.?[0-9]+(?:,[-+]?[0-9]*\.?[0-9]+?|)+$'
            self.delete_spaces()
            if re.match(format, self.new_A) == None:
                raise ValueError('Error - ' + number + ' [A]: comma-separated real numbers expected')
            elif re.match(format, self.new_As) == None:
                raise ValueError('Error - ' + number + ' [As]: comma-separated real numbers expected')
            elif re.match(format, self.new_B) == None:
                raise ValueError('Error - ' + number + ' [B]: comma-separated real numbers expected')
            elif re.match(format, self.new_Bs) == None:
                raise ValueError('Error - ' + number + ' [Bs]: comma-separated real numbers expected')
            if len(self.new_A.split(',')) != len(self.new_As.split(',')) or len(self.new_A.split(',')) != len(self.new_B.split(','))\
                or len(self.new_A.split(',')) != len(self.new_Bs.split(',')):
                raise ValueError('Error - ' + number + ' [A, As, B, Bs]: same sizes of sets expected')
            return True

        def convert_to_znumber(self, number):
            self.delete_spaces()
            if number == 'Result' or self.validate(number) or self.validate(number):
                A = [float(el) for el in self.new_A.split(',')]
                As = [float(el) for el in self.new_As.split(',')]
                B = [float(el) for el in self.new_B.split(',')]
                Bs = [float(el) for el in self.new_Bs.split(',')]
                return Znumber(A, As, B, Bs)

        def delete(self):
            self.A.text.delete("1.0", END)
            self.As.text.delete("1.0", END)
            self.B.text.delete("1.0", END)
            self.Bs.text.delete("1.0", END)

        def clicked_all(self, clc = True):
            self.A.clicked = clc
            self.As.clicked = clc
            self.B.clicked = clc
            self.Bs.clicked = clc

        def set_init_text(self):
            self.delete()
            self.A.text.insert(END, 'Part A')
            self.As.text.insert(END, 'Part As')
            self.B.text.insert(END, 'Part B')
            self.Bs.text.insert(END, 'Part Bs')

BASE_FONT = ("Helvetica", 12)
BASE_FONT_BOLD = ("Helvetica", 12, 'bold')

class ToolTipManager:

    label = None
    window = None
    active = 0

    def __init__(self):
        self.tag = None

    def getcontroller(self, widget):
        if self.tag is None:

            self.tag = "ui_tooltip_%d" % id(self)
            widget.bind_class(self.tag, "<Enter>", self.enter)
            widget.bind_class(self.tag, "<Leave>", self.leave)

            # pick suitable colors for tooltips
            try:
                self.bg = "systeminfobackground"
                self.fg = "systeminfotext"
                widget.winfo_rgb(self.fg) # make sure system colors exist
                widget.winfo_rgb(self.bg)
            except:
                self.bg = "#ffffe0"
                self.fg = "black"

        return self.tag

    def register(self, widget, text):
        widget.ui_tooltip_text = text
        tags = list(widget.bindtags())
        tags.append(self.getcontroller(widget))
        widget.bindtags(tuple(tags))

    def unregister(self, widget):
        tags = list(widget.bindtags())
        tags.remove(self.getcontroller(widget))
        widget.bindtags(tuple(tags))

    # event handlers

    def enter(self, event):
        widget = event.widget
        if not self.label:
            # create and hide balloon help window
            self.popup = Toplevel(bg=self.fg, bd=1)
            self.popup.overrideredirect(1)
            self.popup.withdraw()
            self.label = Label(
                self.popup, fg=self.fg, bg=self.bg, bd=0, padx=2
                )
            self.label.pack()
            self.active = 0
        self.xy = event.x_root + 16, event.y_root + 10
        self.event_xy = event.x, event.y
        self.after_id = widget.after(200, self.display, widget)

    def display(self, widget):
        if not self.active:
            # display balloon help window
            text = widget.ui_tooltip_text
            if callable(text):
                text = text(widget, self.event_xy)
            self.label.config(text = text)
            self.popup.deiconify()
            self.popup.lift()
            self.popup.geometry("+%d+%d" % self.xy)
            self.active = 1
            self.after_id = None

    def leave(self, event):
        widget = event.widget
        if self.active:
            self.popup.withdraw()
            self.active = 0
        if self.after_id:
            widget.after_cancel(self.after_id)
            self.after_id = None

_manager = ToolTipManager()

def register(widget, text):
    _manager.register(widget, text)


def unregister(widget):
    _manager.unregister(widget)

class Main:
    def __init__(self, root):
        self.root = root
        self.set_layout()
        self.set_labels()
        self.set_input_texts()
        self.set_buttons()
        self.set_combobox()
        self.set_choice_result()
        self.set_output_texts()
        self.set_tips()
        self.set_graphics()
        self.calculated = False
        self.plotted = False
        self.root.bind('<Return>', self.calculate)

    def set_layout(self):
        self.root.title("OdiZ 1.1 | Operations on discrete Z-numbers")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.choice = StringVar()
        self.error = StringVar()

        self.canv = Canvas(self.root, highlightthickness = 0)
        self.canv.grid(column = 0, row = 0, sticky = (N, W, E, S))
        self.canv.rowconfigure(0, weight=1)
        self.canv.columnconfigure(0, weight=1)

        frame1 = Canvas(self.canv, highlightthickness = 0)
        frame1.grid(column = 0, row = 0, sticky=(N, W, E, S))
        frame1.rowconfigure(0, weight = 1)
        frame1.columnconfigure(0, weight = 1)
        self.frame1 = ttk.Frame(frame1)
        for i in range(1, 5):
            self.frame1.columnconfigure(i, weight = 1)
        self.frame1.grid(column = 0, row = 0, sticky = (N, W, E, S))

        self.frame2 = ttk.Frame(self.canv)
        self.frame2.columnconfigure(0, weight = 1)
        self.frame2.grid(column = 1, row = 0, sticky = (N, W, E, S))

        self.frame3 = ttk.Frame(self.frame2, padding = "15 0 0 0")
        self.frame3.grid(column = 0, row = 2, sticky = (N, W, E, S))

    def set_labels(self):

        Z1_label = ttk.Label(self.frame1, text="Number Z1 = (A1, B1):", anchor = CENTER, font = BASE_FONT)
        Z1_label.grid(column=1, columnspan = 2, padx = 50, pady = 5, row=1, sticky=(N, W, E, S))

        Z2_label = ttk.Label(self.frame1, text="Number Z2 = (A2, B2):", anchor = CENTER, font = BASE_FONT)
        Z2_label.grid(column=3, pady = 5, padx = 50, columnspan = 2, row = 1, sticky = (N, W, E, S))

        operation = ttk.Label(self.frame2, text = "Choose the operation:", font = BASE_FONT)
        operation.grid(column = 0, row = 0, padx = 15, pady = 1, sticky = (N, W, E, S))

        err = ttk.Label(self.frame1, textvariable = self.error, anchor = CENTER, font = BASE_FONT_BOLD)
        err.grid(column = 1, row = 7, padx = 3, columnspan = 4, pady = 5, sticky = (W, E, N, S))

        ttk.Separator(self.frame1, orient = HORIZONTAL).grid(row = 8, columnspan = 7, pady = 5, sticky = (W, E))

        col = 1
        for part in ['A', 'As', 'B', 'Bs']:
            ttk.Label(self.frame1, text = part, anchor = CENTER, font = BASE_FONT)\
                .grid(column = col, row = 10, pady = 5, padx = 15, sticky = (W, E, N, S))
            col += 1


    def set_input_texts(self):
        self.Z1 = Znumber_GUI(self.frame1)
        self.Z1.A.text.grid(column = 1, row = 2, pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z1.As.text.grid(column = 1, row = 4,  pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z1.B.text.grid(column = 2, row = 2, pady = 5,  padx = 5, sticky = (W, E, N, S))
        self.Z1.Bs.text.grid(column = 2, row = 4, pady = 5, padx = 5, sticky = (W, E, N, S))

        self.Z2 = Znumber_GUI(self.frame1)
        self.Z2.A.text.grid(column = 3, row = 2,pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z2.As.text.grid(column = 3, row = 4,  pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z2.B.text.grid(column = 4, row = 2, pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z2.Bs.text.grid(column = 4, row = 4, pady = 5, padx = 5, sticky = (W, E, N, S))

    def set_buttons(self):
        read_z1 = ttk.Button(self.frame1, text = "Z1 | read data from the file", command = lambda: self.read(self.Z1, 'Z1'))
        read_z1.grid(column=1, row = 5, columnspan = 2, sticky = (N, W, E, S))
        read_z2 = ttk.Button(self.frame1, text = "Z2 | read data from the file", command = lambda: self.read(self.Z2, 'Z2'))
        read_z2.grid(column=3, columnspan = 2, row = 5, sticky = (N, W, E, S))

        ttk.Button(self.frame2, text = "Calculate", command = self.calculate).grid(column = 1, row = 1, sticky = (N, W, E, S))

        ttk.Button(self.frame3, text = "Test values", command = self.example).grid(column=  0, row = 0, sticky = (N, W, E, S))
        ttk.Button(self.frame3, text = "Clear", command = self.clear).grid(column = 1, row = 0, sticky = (N, W, E, S))
        ttk.Button(self.frame3, text = "Help").grid(column = 2, row = 0, sticky = (N, W, E, S))

        plotZ1a = ttk.Button(self.frame1, text = "Show Z1 (Part A)", command = lambda: self.plot_one_graph(self.Z1, 'Z1', 'A'))
        plotZ1a.grid(column = 1, row = 6, sticky = (N, W, E, S))

        plotZ2a = ttk.Button(self.frame1, text = "Show Z2 (Part A)", command = lambda: self.plot_one_graph(self.Z2, 'Z2', 'A'))
        plotZ2a.grid(column = 3, row = 6, sticky = (N, W, E, S))

        plotResa = ttk.Button(self.frame1, text = "Show Result (Part A)", command = lambda: self.plot_one_graph(self.Z3, 'Result', 'A'))
        plotResa.grid(column = 1, columnspan = 2, row = 12, sticky = (N, W, E, S))

        plotZ1b = ttk.Button(self.frame1, text = "Show Z1 (Part B)", command = lambda: self.plot_one_graph(self.Z1, 'Z1', 'B'))
        plotZ1b.grid(column = 2, row = 6, sticky = (N, W, E, S))

        plotZ2b = ttk.Button(self.frame1, text = "Show Z2 (Part B)", command = lambda: self.plot_one_graph(self.Z2, 'Z2', 'B'))
        plotZ2b.grid(column = 4, row = 6, sticky = (N, W, E, S))

        plotResb = ttk.Button(self.frame1, text = "Show Result (Part B)", command = lambda: self.plot_one_graph(self.Z3, 'Result', 'B'))
        plotResb.grid(column = 3, columnspan = 2, row = 12, sticky = (N, W, E, S))

        ttk.Button(self.frame1, text="Show All", width = 20, command = self.plot_all_graphs).grid(column = 1, columnspan = 4, row = 13)

    def set_combobox(self):
        COMBOBOX_WIDTH = 60
        COMBOBOX_HEIGHT = 6

        self.operations = [u"Addition",u"Substraction",u"Multiplication", u'Division', u'Minimum', u'Maximum']
        combobox = ttk.Combobox(self.frame2, textvariable = self.choice, values = self.operations, width = COMBOBOX_WIDTH,
                                height = COMBOBOX_HEIGHT, state = 'readonly')
        combobox.set(u"Addition")
        combobox.grid(column = 0, row = 1, padx = 15, pady = 1, sticky = (N, W, E, S))
        combobox.bind('<<ComboboxSelected>>', lambda event: self.handler())

    def handler(self):
        self.res.set('Result (operation ' + self.choice.get() + '):')
        self.ch.set(self.messages[self.choice.get()])
        res_label = ttk.Label(self.frame1, textvariable = self.res, font = BASE_FONT)
        res_label.grid(column = 0, columnspan = 4, row = 9, pady = 5, padx = 15, sticky = (W, E, N, S))
        ch_label = ttk.Label(self.frame3, textvariable = self.ch, font = BASE_FONT)
        ch_label.grid(column = 0, columnspan = 3, row = 1, pady = 5, sticky = (W, E, N, S))


    def set_choice_result(self):
        self.res = StringVar()
        self.res.set('Result (operation ' + 'Addition' + '):')
        self.ch = StringVar()
        self.ch.set('The user\'s choice is ' + 'Z1 + Z2')

        base = 'The user\'s choice is '
        variants = [base + str for str in ['Z1 + Z2', 'Z1 - Z2', 'Z1 * Z2', 'Z1 / Z2', 'MIN(Z1, Z2)', 'MAX(Z1, Z2)']]
        self.messages = dict(zip(self.operations, variants))
        res_label = ttk.Label(self.frame1, textvariable = self.res, font = BASE_FONT)
        res_label.grid(column = 0, columnspan = 4, row = 9, pady = 5, padx = 15, sticky = (W, E, N, S))
        ch_label = ttk.Label(self.frame3, textvariable = self.ch, font = BASE_FONT)
        ch_label.grid(column = 0, columnspan = 3, row = 1, pady = 5, sticky = (W, E, N, S))

    def set_output_texts(self):
        self.Z3 = Znumber_GUI(self.frame1)
        self.Z3.A.text.grid(column = 1, row = 11, pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z3.As.text.grid(column = 2, row = 11, pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z3.B.text.grid(column = 3, row = 11, pady = 5, padx = 5, sticky = (W, E, N, S))
        self.Z3.Bs.text.grid(column = 4, row = 11, pady = 5, padx = 5, sticky=  (W, E, N, S))

    def set_tips(self):
        register(self.Z1.A.text, "Z1 (Part A)")
        register(self.Z1.As.text, "Z1 (Part As)")
        register(self.Z1.B.text, "Z1 (Part B)")
        register(self.Z1.Bs.text, "Z1 (Part Bs)")
        register(self.Z2.A.text, "Z2 (Part A)")
        register(self.Z2.As.text, "Z2 (Part As)")
        register(self.Z2.B.text, "Z2 (Part B)")
        register(self.Z2.Bs.text, "Z2 (Part Bs)")

    def read(self, Z, number):
        file_opt = {}
        file_opt['defaultextension'] = '.txt'
        file_opt['title'] = 'Reading Z-number'
        file_opt['filetypes'] = [('all files', '.*'), ('text files', '.txt')]

        def open_file_handler():
            filePath = askopenfilename(**file_opt)
            return filePath

        def validate(data, number, part):
            format = r'^[-+]?[0-9]*\.?[0-9]+(?:,[-+]?[0-9]*\.?[0-9]+?|)+$'
            data = data.replace(" ", "")
            if len(data) == 0 or re.match(format, data) == None:
                raise ValueError('Error - ' + number + '[' + part + ']: bad format / mismatch')

        filePath = open_file_handler()
        if filePath == '':
            return
        names = ['a', 'as', 'b', 'bs']
        self.error.set('')
        with open(filePath, 'r') as f:
            for line in f.readlines():
                s = line.replace(" ", "")
                result = s.split(':')
                name = result[0].lower()
                data = result[1].replace(" ", "")
                data = data.strip()
                part_names = ['A', 'As', 'B', 'Bs']
                names_vars = dict(zip(part_names,[Z.A, Z.As, Z.B, Z.Bs]))
                if len(result) > 0 and name in names:
                    part_name = part_names[names.index(name)]
                    part = names_vars[part_name]
                    try:
                        validate(data, number, part_name)
                        part.text.delete("1.0", END)
                        part.text.insert("1.0", data.replace(',', ', '))
                        part.clicked = True
                    except ValueError as e:
                        self.error.set(str(e))
    def set_graphics(self):
        style.use("ggplot")

    def plotter(self, Z, number, part):
        try:
            xList = []
            yList = []
            self.base.clear()
            if part == 'A':
                xList, yList = Z.convert_to_znumber(number).As, Z.convert_to_znumber(number).A
            if part == 'B':
                xList, yList = Z.convert_to_znumber(number).Bs, Z.convert_to_znumber(number).B
            nan_to_zeros(xList, yList)
            title = number + '( Part ' + part + ')'
            self.base.plot(xList, yList, marker = '8', linestyle='--')
            self.base.set_xlim([0 - (max(xList) - min(xList)) / 10, max(xList) + (max(xList) - min(xList)) / 10])
            self.base.set_ylim([-0.05, 1.05])
            self.base.set_title(title)
            Z.plotted[part] = True
            self.plotted = True
        except:
            self.error.set('Error - [Plotter]: plotting failed')


    def plot_one_graph(self, Z, number, part = 'A'):

        if Z.plotted[part]:
            self.plt.grid_forget()
            self.save_canvas.grid_forget()
            Z.plotted[part] = False
            self.plotted = False
            return

        for zn in [self.Z1, self.Z2, self.Z3]:
            if zn.plotted['A'] or zn.plotted['B']:
                self.plt.grid_forget()
                self.save_canvas.grid_forget()
                zn.plotted['A'] = False
                zn.plotted['B'] = False
                self.plotted = False

        try:
            if number == 'Result' and not self.calculated:
                raise ValueError("Error - Result [A]: Not calculated yet")
            if number != 'Result':
                Z.validate(number)
            self.error.set('')
        except ValueError as e:
            self.error.set(str(e))
            return

        self.fig = Figure()
        self.fig.set_size_inches(2400.0/float(DPI), 2100.0/float(DPI))
        self.base = self.fig.add_subplot(111)
        self.plt = Canvas(self.frame2, width = 265, height = 230)
        self.plt.grid(row = 4, column = 0, columnspan = 2, padx = 100)
        plot_canvas = FigureCanvasTkAgg(self.fig, self.plt)
        plot_canvas.show()
        plot_canvas.get_tk_widget().grid(column = 0, row = 0)
        self.save_canvas = Canvas(self.frame2, width = 1, height = 100)
        self.save_canvas.grid(row = 6, column = 0, columnspan = 2, padx = 100, pady = 15)
        ttk.Button(self.save_canvas, text = "Save Graph").grid(column = 0, row = 0)
        self.plotter(Z, number, part)

    def plotter_result(self):

        znumb = self.Z3.convert_to_znumber('Result')
        #znumb1 = self.Z1.convert_to_znumber('Z1')
        n_sub_graph = 0
        for xList, yList, part in [[znumb.As, znumb.A, 'A'], [znumb.Bs, znumb.B, 'B']]:
            self.sub_graphs[n_sub_graph].clear()
            self.sub_graphs[n_sub_graph].plot(xList, yList, marker = '8', linestyle='--')
            self.sub_graphs[n_sub_graph].set_xlim([0 - (max(xList) - min(xList)) / 10, max(xList) + (max(xList) - min(xList)) / 10])
            self.sub_graphs[n_sub_graph].set_ylim([-0.05, 1.05])
            self.sub_graphs[n_sub_graph].set_title('Result (Part' + part + ')')
            n_sub_graph += 1

    def plotter_all(self):

        znumb1 = self.Z1.convert_to_znumber('Z1')
        znumb2 = self.Z2.convert_to_znumber('Z2')
        n_sub_graph = 0
        for xList, yList, part in [[znumb1.As, znumb1.A, 'A'], [znumb1.Bs, znumb1.B, 'B'],\
                                    [znumb2.As, znumb2.A, 'A'], [znumb2.Bs, znumb2.B, 'B']]:
            self.sub_graphs[n_sub_graph].clear()
            self.sub_graphs[n_sub_graph].plot(xList, yList, marker = '8', linestyle='--')
            self.sub_graphs[n_sub_graph].set_xlim([0 - (max(xList) - min(xList)) / 10, max(xList) + (max(xList) - min(xList)) / 10])
            self.sub_graphs[n_sub_graph].set_ylim([-0.05, 1.05])
            if n_sub_graph < 2:
                title = 'Z1'
            else:
                title = 'Z2'
            self.sub_graphs[n_sub_graph].set_title(title + ' (Part' + part + ')')
            n_sub_graph += 1
        #except:
        #self.error.set('Error - [Plotter]: plotting failed')


    def plot_all_graphs(self):
        if not self.calculated:
            self.error.set("Error - Result [ALL]: Not calculated yet")
            return

        self.error.set('')
        self.all_graphs = Toplevel()
        self.all_graphs.title('All graphs')
        self.all_graphs.focus_set()
        self.all_graphs.columnconfigure(0, weight = 1)
        self.all_graphs.columnconfigure(1, weight = 1)
        self.all_graphs.columnconfigure(2, weight = 1)
        self.all_graphs.columnconfigure(3, weight = 1)
        self.all_graphs.rowconfigure(0, weight = 1)
        self.all_graphs.rowconfigure(1, weight = 1)

        self.fig1 = Figure()
        #self.fig2 = Figure()
        self.fig1.set_size_inches(5000.0/float(DPI), 4700.0/float(DPI))
        #self.fig2.set_size_inches(3000.0/float(DPI), 4700.0/float(DPI))
        self.sub_graphs = [self.fig1.add_subplot(2, 2, 1), self.fig1.add_subplot(2, 2, 2), self.fig1.add_subplot(2, 2, 3),\
                           self.fig1.add_subplot(2, 2, 4)]
        plt1 = Canvas(self.all_graphs)
        plt1.grid(row = 0, column = 0, columnspan = 2, padx = 50, pady = 5)
        plt_canvas = FigureCanvasTkAgg(self.fig1, plt1)
        plt_canvas.show()
        plt_canvas.get_tk_widget().grid(column = 0, row = 0)
        ttk.Button(self.all_graphs, text = "Save Graph").grid(column = 0, columnspan = 2, row = 1)
        Message(self.all_graphs, text = "").grid(column=0, columnspan = 2, row = 2, pady = 15)
        self.plotter_all()

        self.fig2 = Figure()
        self.fig2.set_size_inches(3000.0/float(DPI), 4700.0/float(DPI))
        self.sub_graphs = [self.fig2.add_subplot(2, 1, 1), self.fig2.add_subplot(2, 1, 2)]
        plt2 = Canvas(self.all_graphs)
        plt2.grid(row = 0, column = 2, columnspan = 2, padx = 50, pady = 5)
        plt_canvas2 = FigureCanvasTkAgg(self.fig2, plt2)
        plt_canvas2.show()
        plt_canvas2.get_tk_widget().grid(column = 2, row = 0)
        ttk.Button(self.all_graphs, text = "Save Graph").grid(column = 2, columnspan = 2, row = 1)
        Message(self.all_graphs, text = "").grid(column = 2, columnspan = 2, row = 2, pady = 15)

        self.plotter_result()

    def save_graph(self):
        pass

    def calculate(self):
        try:
            funcs = [Zsum, Zsub, Zprod, Zdiv, Zmin, Zmax]
            self.Z1_number = self.Z1.convert_to_znumber('Z1')
            self.Z2_number = self.Z2.convert_to_znumber('Z2')

        except ValueError as e:
            self.calculated = False
            self.error.set(str(e))
            self.Z3.delete()
            return

        try:
            ct = self.choice.get()
            operation_func = dict(zip(self.operations, funcs))
            Z3a, Z3as, Z3b, Z3bs, Z3p, Z1p, Z2p = operation_func[ct](self.Z1_number.A, self.Z1_number.As,\
                self.Z1_number.B, self.Z1_number.Bs, self.Z2_number.A, self.Z2_number.As, self.Z2_number.B, self.Z2_number.Bs)

            for i in range(len(Z3a)):
                Z3a[i] = formating(Z3a[i])
                Z3as[i] = formating(Z3as[i])
                Z3b[i] = formating(Z3b[i])
                Z3bs[i] = formating(Z3bs[i])
            self.Z3.delete()
            self.Z3.A.text.insert("1.0", tostr(Z3a))
            self.Z3.As.text.insert("1.0", tostr(Z3as))
            self.Z3.B.text.insert("1.0", tostr(Z3b))
            self.Z3.Bs.text.insert("1.0", tostr(Z3bs))
            self.error.set('')
            self.calculated = True
            self.Z3.clicked_all(True)
            if self.plotted:
                self.plt.grid_forget()
                self.save_canvas.grid_forget()
                self.plotted = False
        except:
            self.Z3.delete()
            self.error.set('Error - [FATAL]: calculations failed')
            self.calculated = False

    def clear(self):
        self.Z1.delete()
        self.Z2.delete()
        self.Z1.clicked_all(False)
        self.Z2.clicked_all(False)
        self.Z1.set_init_text()
        self.Z2.set_init_text()
        if self.plotted:
            self.plt.grid_forget()
            self.save_canvas.grid_forget()
            self.plotted = False
        self.Z3.delete()

    def example(self):
        self.Z1.clicked_all(True)
        self.Z2.clicked_all(True)
        self.Z1.delete()
        self.Z2.delete()
        self.Z1.A.text.insert(END, '0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 0.5, 0')
        self.Z1.As.text.insert(END, '0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10')
        self.Z1.B.text.insert(END, '0, 0, 0, 0, 0.5, 1, 0.5, 0, 0, 0, 0')
        self.Z1.Bs.text.insert(END, '0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0')

        self.Z2.A.text.insert(END, '0, 0, 0.5, 1, 0.5, 0, 0, 0, 0, 0, 0')
        self.Z2.As.text.insert(END, '0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10')
        self.Z2.B.text.insert(END, '0, 0, 0, 0, 0, 0, 0, 0.5, 1, 0.5, 0')
        self.Z2.Bs.text.insert(END, '0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0')
        self.error.set('')
        if self.plotted:
            self.plt.grid_forget()
            self.save_canvas.grid_forget()
            self.plotted = False
        self.Z3.delete()

if __name__ == "__main__":
    try:
        root = Tk()
    except:
        root = ttk.Tk()
    app = Main(root)
    root.mainloop()
