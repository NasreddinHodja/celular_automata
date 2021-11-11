#!/usr/bin/env python3

import os
import sys
import random

import tkinter
from PIL import Image

class ElemCelAutomaton():
    def __init__(self, rule, length, iterations,
                 canvas, canvas_w, canvas_h,
                 cell_size,
                 random=False):
        self.rule = "{0:08b}".format(rule)
        self.length = length
        self.iterations = iterations
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.canvas = canvas
        self.cell_size = cell_size
        self.cells = [0] * length

        # init cells
        self.cells[int(length / 2) + 1] = 1
        if random: self.random_cells()

    def random_cells(self):
        self.cells = [random.randint(0, 1) for i in range(0, self.length)]

    def draw(self, save=False):
        self.canvas.delete(tkinter.ALL)

        for it in range(0, self.iterations):
            new_cells = [0] * self.length

            for cell in range(0, self.length):
                # draw current cell
                pos_x = self.cell_size * cell
                pos_y = self.cell_size * it

                color = "#f8f8f2" if self.cells[cell] else "#000000"
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x + self.cell_size,
                                             pos_y + self.cell_size,
                                             fill=color)
                self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

                # compute new cell
                state = int(str(self.cells[cell-1]) + str(self.cells[cell])
                         + str(self.cells[(cell+1) % self.length]), 2)
                new_cells[cell] = int(self.rule[-1-state])

            self.cells = new_cells

        self.canvas.update()

        if save:
            self.save()

    def save(self):
        self.canvas.postscript(file=f'out/automaton_{int(self.rule, 2)}.eps')
        img = Image.open(f'out/automaton_{int(self.rule, 2)}.eps')
        img.save(f'out/automaton_{int(self.rule, 2)}.png', 'png')
        os.remove(f'out/automaton_{int(self.rule, 2)}.eps')

    def __str__(self):
        s = (f"rule: {self.rule} ({int(self.rule, 2)})\n"
             + f"length: {self.length}\n"
             + f"iterations: {self.iterations}\n"
             + f"canvas_w, canvas_h: {self.canvas_w}, {self.canvas_h}\n"
             + f"cell_size: {self.cell_size}\n")
        return s

def main():
    root = tkinter.Tk()
    root.geometry('+0+0')


    rule = 107
    automaton_length = 200
    automaton_iterations = 200
    canvas_w = 500
    canvas_h = 500
    cell_size = int(canvas_w / automaton_length) + 1


    canvas = tkinter.Canvas(root, bg='black',
                            width=canvas_w, height=canvas_h)

    automaton = ElemCelAutomaton(rule, automaton_length,
                                    automaton_iterations,
                                    canvas, canvas_w, canvas_h,
                                    cell_size,
                                    random=True)
    automaton.draw(save=True)

    # if '-s' in sys.argv:
    #     automaton.draw(save=True)
    # else:
        # automaton.draw()

    tkinter.mainloop()

if __name__ == '__main__':
    main()
