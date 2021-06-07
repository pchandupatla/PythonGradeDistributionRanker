import pandas
import sqlite3

from bokeh.io import output_file
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import Button, Select, TextInput

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', None)

# add a button widget and configure with the call back
select = Select(title='Department:', value="Select an option", options=["AAS", "ACC", "ACF", "ADV", "AED", "AET", "AFR",
                                                                        "AFS", "AHC", "ALD", "AMS", "ANS", "ANT", "ARA",
                                                                        "ARC", "ARE", "ARH", "ARI", "ART", "ASE", "ASL",
                                                                        "AST", "B A", "BCH", "BDP", "BGS", "BIO", "BME",
                                                                        "C C", "C E", "C L", "C S", "CGS", "CH", "CHE",
                                                                        "CHI", "CLD", "CMS", "COE", "COM", "CRP", "CRW",
                                                                        "CSD", "CSE", "CTI", "CZ", "DAN", "DCH", "DES",
                                                                        "E", "E E", "E M", "E S", "ECO", "EDA", "EDC",
                                                                        "EDP", "EER", "ELP", "ENM", "ENS", "EUS", "EVE",
                                                                        "EVS", "F A", "F C", "FIN", "FR", "G E", "GEO",
                                                                        "GER", "GK", "GOV", "GRC", "GRG", "GSD", "H E",
                                                                        "H S", "HCT", "HDF", "HDO", "HEB", "HED", "HIN",
                                                                        "HIS", "HMN", "I B", "ILA", "IMS", "INF", "IRG",
                                                                        "ISL", "ITC", "ITD", "ITL", "J", "J S", "JPN",
                                                                        "KIN", "KOR", "L A", "LAH", "LAR", "LAS", "LAT",
                                                                        "LAW", "LEB", "LIN", "M", "M E", "M S", "MAL",
                                                                        "MAN", "MAS", "MBU", "MDV", "MEL", "MES", "MIS",
                                                                        "MKT", "MNS", "MOL", "MRT", "MUS", "N", "N S",
                                                                        "NEU", "NOR", "NSC", "NTR", "O M", "ORI", "P A",
                                                                        "P R", "P S", "PBH", "PED", "PGE", "PGS", "PHL",
                                                                        "PHM", "PHR", "PHY", "POL", "POR", "PRC", "PRS",
                                                                        "PSY", "R E", "R M", "R S", "REE", "RHE", "RTF",
                                                                        "RUS", "S S", "S W", "SAB", "SAN", "SCA", "SCI",
                                                                        "SDS", "SED", "SEL", "SLA", "SOC", "SPC", "SPN",
                                                                        "SSC", "STA", "STC", "STM", "SUS", "SWE", "T C",
                                                                        "T D", "TAM", "TEL", "TXA", "UGS", "URB", "URD",
                                                                        "UTL", "UTS", "VAS", "WGS", "WRT", "YID",
                                                                        "YOR"])

course_num_text = TextInput(title="Course Number")
course_title_text = TextInput(title="Course Title")
submit_button = Button(label='Submit')

dept_selection = ""
course_num = ""
course_title = ""

p = figure(x_range=[], plot_height=250, title="Percentage As",
           toolbar_location=None, tools="", name='plot')
p.y_range.start = 0
p.sizing_mode = 'stretch_both'
p.xaxis.major_label_orientation = np.pi / 4
p.xaxis.axis_label = 'Professor'
p.yaxis.axis_label = '% As'


def store_select(attr, old, new):
    global dept_selection
    dept_selection = select.value


def store_course_num(attr, old, new):
    global course_num
    course_num = course_num_text.value


def store_course_title(attr, old, new):
    global course_title
    course_title = course_title_text.value


def submit():
    connection = sqlite3.connect('updatedgrades.db')
    if course_num != "":
        sql = """SELECT * FROM agg WHERE dept=? AND course_nbr=?"""
        df = pandas.read_sql_query(sql, connection, params=[dept_selection, course_num])
    else:
        sql = """SELECT * FROM agg WHERE dept=? AND course_name LIKE ?"""
        df = pandas.read_sql_query(sql, connection, params=[dept_selection, course_title.upper()])
    df['%As'] = df['a2'] / (df.sum(axis=1))
    df = df.sort_values(by=['%As'], ascending=False)
    df = df.drop_duplicates(subset=['prof'], keep='first')

    # global p
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    plotToRemove = curdoc().get_model_by_name('plot')
    listOfSubLayouts.remove(plotToRemove)
    f = figure(x_range=df['prof'], plot_height=250, title="Percentage As",
               toolbar_location=None, tools="", name='plot')
    f.vbar(x=df['prof'], top=df['%As'], width=0.9)
    f.y_range.start = 0
    f.sizing_mode = 'stretch_both'
    f.xaxis.major_label_orientation = np.pi / 4
    f.xaxis.axis_label = 'Professor'
    f.yaxis.axis_label = '% As'
    listOfSubLayouts.append(f)
    connection.close()


select.on_change('value', store_select)
course_num_text.on_change('value', store_course_num)
course_title_text.on_change('value', store_course_title)
submit_button.on_click(submit)

output_file("test.html")
mainLayout = column(select, course_num_text, course_title_text, submit_button, p, name='mainLayout')
curdoc().add_root(mainLayout)
