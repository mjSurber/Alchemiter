from tkinter import *
from AlchemyGlobal import items, get_item_from_name, FONT
from Alchemization import alchemize
from VisualEngine import draw_item_bounds
from Renderer import render_item, create_object

ZOOM_INCREMENT = 0.5

class AlchemyGUI:
    method = "AND"
    item_a = "Choose\nan\nItem"
    item_b = "Choose\nan\nItem"
    item_a_item = None
    item_b_item = None

    method_button = None

    new_item = None

    rotation = 0
    zoom = 1

    diagram = False

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        left_list = Frame(frame)
        left_list.pack(side=LEFT, padx=5, pady=5, fill=Y, expand=1)

        left_list_title = Label(left_list, justify=CENTER, text="SELECT ITEM A", fg="#67db74", font=(FONT, 14))
        left_list_title.pack(side=TOP)

        self.left_item_list = Listbox(left_list, width=15, borderwidth=0, fg="#67db74", font=(FONT, 14), selectbackground="#67db74", exportselection=0, activestyle=NONE, highlightthickness=0)
        self.left_item_list.pack(side=TOP, fill=Y, expand=1)

        alchemy_frame = Frame(frame)
        alchemy_frame.pack(side=LEFT, pady=5)

        right_list = Frame(frame)
        right_list.pack(side=LEFT, padx=5, pady=5, fill=Y, expand=1)

        right_list_title = Label(right_list, justify=CENTER, text="SELECT ITEM B", fg="#67db74", font=(FONT, 14))
        right_list_title.pack(side=TOP)

        self.right_item_list = Listbox(right_list, width=15, borderwidth=0, fg="#67db74", font=(FONT, 14), selectbackground="#67db74", exportselection=0, activestyle=NONE, highlightthickness=0)
        self.right_item_list.pack(side=TOP, fill=Y, expand=1)

        self.populate_lists()
        # bg="#d6d6d6"

        # Alchemy controls
        self.swap_button = Button(alchemy_frame, text="<- SWAP ->", justify=CENTER, width=10, height=1, fg="#67db74", font=(FONT, 20), borderwidth=0, command=self.swap)
        self.swap_button.pack(side=TOP)

        controls_frame = Frame(alchemy_frame)
        controls_frame.pack(side=TOP)

        self.item_a_button = Button(
            controls_frame, text=self.item_a, justify=CENTER, width=10, height=6, fg="#67db74", font=(FONT, 14), bg="white", borderwidth=0
        )
        self.item_a_button.pack(side=LEFT, padx=25)
        self.method_button = Button(
            controls_frame, text="&&", justify=CENTER, width=3, height=1, fg="#67db74", font=(FONT, 44), bg="white", borderwidth=0, command=self.toggle_method
        )
        self.method_button.pack(side=LEFT, padx=5)
        self.item_b_button = Button(
            controls_frame, text=self.item_b, justify=CENTER, width=10, height=6, fg="#67db74", font=(FONT, 14), bg="white", borderwidth=0
        )
        self.item_b_button.pack(side=LEFT, padx=25)

        self.alchemize_button = Button(
            alchemy_frame, text="COMBINE", justify=CENTER, width=10, height=2, fg="#67db74", font=(FONT, 24), bd=0, command=self.get_alchemy
        )
        self.alchemize_button.pack()

        self.rename_button = Button(alchemy_frame, text="NAME", width=20, height=1, bg="#67db74", fg="white", font=(FONT, 12), state=DISABLED, bd=0, command=self.name_item)
        self.rename_button.pack(pady=5)

        self.name_entry_string = StringVar()
        self.name_entry = Entry(alchemy_frame, textvariable=self.name_entry_string, fg="#67db74", bg="white", readonlybackground="#67db74", width=20, font=(FONT, 24), bd=0, justify=LEFT, state="readonly")
        self.name_entry.pack()
        self.name_entry_string.set("")

        #Results field
        self.result = StringVar()
        #self.result_build = Label(alchemy_frame, textvariable=self.result, fg="#67db74", bg="white", width=80, height=25, font=("Courier New Bold", 10), bd=0, justify=LEFT)
        #self.result_build.pack(pady=5)
        self.result.set("")

        render_control_frame = Frame(alchemy_frame)
        render_control_frame.pack(pady=5)

        self.rot_cw_button = Button(
            render_control_frame, text="<", justify=CENTER, width=2, height=1, bg="#67db74", fg="white",
            font=(FONT, 12), bd=0,
            command=self.rotate_cw
        )
        self.rot_cw_button.pack(side=LEFT)

        self.zoom_minus = Button(
            render_control_frame, text="-", justify=CENTER, width=2, height=1, bg="#67db74", fg="white", font=(FONT, 12), bd=0,
            command=self.zoom_out
        )
        self.zoom_minus.pack(side=LEFT)

        self.diagram_button = Button(
            render_control_frame, text="LABEL", justify=CENTER, width=10, height=1, bg="#67db74", fg="white", font=(FONT, 12), bd=0, command=self.toggle_diagram
        )
        self.diagram_button.pack(side=LEFT, padx=2)

        self.zoom_plus = Button(
            render_control_frame, text="+", justify=CENTER, width=2, height=1, bg="#67db74", fg="white", font=(FONT, 12), bd=0, command=self.zoom_in
        )
        self.zoom_plus.pack(side=LEFT)

        self.rot_ccw_button = Button(
            render_control_frame, text=">", justify=CENTER, width=2, height=1, bg="#67db74", fg="white",
            font=(FONT, 12), bd=0,
            command=self.rotate_ccw
        )
        self.rot_ccw_button.pack(side=LEFT)

        self.result_canvas = Canvas(alchemy_frame, bg="white", width=642, height=250, bd=0)
        self.result_canvas.pack()

        self.abilities = StringVar()
        self.result_abilities = Label(alchemy_frame, textvariable=self.abilities, fg="#67db74", bg="white", width=80, height=5, font=("Courier New Bold", 10), bd=0, justify=LEFT, wraplength=600)
        self.result_abilities.pack()
        self.abilities.set("")

        self.save_button = Button(alchemy_frame, text="SAVE", justify=CENTER, width=10, height=2, bg="#67db74", fg="white", font=(FONT, 24), bd=0, command=self.save_item, state=DISABLED)
        self.save_button.pack()

        self.poll()

    def save_item(self):
        if self.new_item.name == "Temp_Name":
            return
        items.append(self.new_item)
        self.save_button.config(state=DISABLED)
        self.right_item_list.delete(0, END)
        self.left_item_list.delete(0, END)
        self.populate_lists()

    def populate_lists(self):
        print("Adding items to GUI item list...")
        for item in items:
            print("Adding {}".format(item.name))
            self.left_item_list.insert(END, item.name.upper())
            self.right_item_list.insert(END, item.name.upper())

    def name_item(self):
        name = self.name_entry_string.get()
        if name == "":
            return
        self.new_item.name = name
        construct = self.new_item.get_construct()
        ability_set = self.new_item.get_ability_set()
        self.result.set(construct)
        self.abilities.set(ability_set)
        self.save_button.config(state=ACTIVE)

    def zoom_in(self):
        self.zoom += ZOOM_INCREMENT
        self.render_selection()

    def zoom_out(self):
        if self.zoom > ZOOM_INCREMENT:
            self.zoom -= ZOOM_INCREMENT
            self.render_selection()

    def toggle_diagram(self):
        if self.diagram:
            self.diagram = False
        else:
            self.diagram = True
        self.render_selection()

    def render_selection(self):
        canvas_items = self.result_canvas.find_all()
        for item in canvas_items:
            self.result_canvas.delete(item)
        self.render = create_object(self.render_item, 321, 125, self.rotation, self.zoom)
        render_item(self.result_canvas, self.render, self.diagram)

    def rotate_cw(self):
        self.rotation -= 90
        self.render_selection()

    def rotate_ccw(self):
        self.rotation += 90
        self.render_selection()

    def rotate(self):
        self.rotation += 90
        self.render_selection()


    def get_alchemy(self):
        name_a, name_b = self.parse_selected()
        self.new_item = alchemize(name_a, name_b)
        self.save_button.config(state=DISABLED)
        self.rename_button.config(state=ACTIVE)
        self.name_entry_string.set("")
        self.name_entry.config(state=NORMAL, fg="#67db74")
        construct = self.new_item.get_construct(False)
        ability_set = self.new_item.get_ability_set(False)
        self.render_item = self.new_item
        self.result.set(construct)
        self.abilities.set(ability_set)
        test_node = self.new_item.c_tree.get_node(self.new_item.c_tree.root)
        test_comp = test_node.data
        self.render_selection()
        #self.update()
        #draw_item_bounds(self.result_canvas, self.new_item, 400, 125)

    #def update(self):
    #    canvas_items = self.result_canvas.find_all()
    #    for item in canvas_items:
    #        self.result_canvas.delete(item)
    #    self.render.rotate(0, 0, 5)
    #    render_item(self.result_canvas, self.render)
    #    root.after(100000, self.update())


    def swap(self):
        select_a = self.left_item_list.curselection()
        select_b = self.right_item_list.curselection()

        if select_a is not ():
            self.left_item_list.selection_clear(select_a)
        if select_b is not ():
            self.right_item_list.selection_clear(select_b)

        if select_b is not ():
            self.left_item_list.select_set(select_b)
        if select_a is not ():
            self.right_item_list.select_set(select_a)

        self.selection_changed()

    def poll(self):
        name_a, name_b = self.parse_selected()
        if name_a != self.item_a or name_b != self.item_b:
            print("{} is not {} or {} is not {}".format(name_a, self.item_a, name_b, self.item_b))
            try:
                if name_a != self.item_a:
                    print("{} is not {}".format(name_a, self.item_a))
                    item_item = get_item_from_name(name_a)
                    item_name = name_a
                else:
                    print("{} is not {}".format(name_b, self.item_b))
                    item_item = get_item_from_name(name_b)
                    item_name = name_b
                self.render_item = item_item
                self.save_button.config(state=DISABLED)
                self.rename_button.config(state=DISABLED)
                self.name_entry.config(state="readonly", fg="white")
                self.name_entry_string.set(item_name)

                self.render_selection()

                self.result.set(item_item.get_construct())
                self.abilities.set(item_item.get_ability_set())
            except AttributeError:
                self.name_entry.config(state="readonly", fg="white")
                self.name_entry_string.set("SELECT AN ITEM")
            self.selection_changed()
            self.item_a = name_a
            self.item_b = name_b
        root.after(250, self.poll)

    def selection_changed(self):
        now_a, now_b = self.parse_selected()
        self.item_a_button.config(text=now_a.upper())
        self.item_b_button.config(text=now_b.upper())

    def get_selected(self):
        return self.left_item_list.curselection(), self.right_item_list.curselection()

    def parse_selected(self):
        select_a, select_b = self.get_selected()
        if select_a is ():
            name_a = "Choose\nan\nItem"
        else:
            name_a = self.left_item_list.get(select_a)
        if select_b is ():
            name_b = "Choose\nan\nItem"
        else:
            name_b = self.right_item_list.get(select_b)
        return name_a, name_b

    def toggle_method(self):
        try:
            if self.method == "AND":
                self.method_button.config(text="||")
                self.method = "OR"
            else:
                self.method_button.config(text="&&")
                self.method = "AND"
        except AttributeError:
            print("Error!  {}{}".format(type(self.method_button),self.method))
            return

class TESTGUI:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
        )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("Hi there, everyone!")


def begin_interface():
    gui = AlchemyGUI(root)
    root.title = "Alchemiter"
    root.mainloop()

root = Tk()
