# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button, Select, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

# add a text renderer to our plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="26px",
           text_baseline="middle", text_align="center")

i = 0

ds = r.data_source


# create a callback that will add a number in a random location
def callback():
    global i
    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds.data['x'] + [random() * 70 + 15]
    new_data['y'] = ds.data['y'] + [random() * 70 + 15]
    new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i % 3]]
    new_data['text'] = ds.data['text'] + [str(i)]
    ds.data = new_data

    i = i + 1


# add a button widget and configure with the call back
button = Button(label="Press Me")
select = Select(title='Department:', value="Select an option", options=["CS", "FIN"])
course_num_text = TextInput(title="Course Number")
course_title_text = TextInput(title="Course Title")
submit_button = Button(label='Submit')


dept_selection = ""
course_num = ""
course_title = ""


def store_select(attr, old, new):
    global dept_selection
    dept_selection = select.value
    print(dept_selection)


def store_course_num(attr, old, new):
    global course_num
    course_num = course_num_text.value
    print(course_num)


def store_course_title(attr, old, new):
    global course_title
    course_title = course_title_text.value
    print(course_title)


def submit():
    print(dept_selection)
    print(course_num)
    print(course_title)


select.on_change('value', store_select)
course_num_text.on_change('value', store_course_num)
course_title_text.on_change('value', store_course_title)
button.on_click(callback)
submit_button.on_click(submit)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, select, course_num_text, course_title_text, submit_button, p))
