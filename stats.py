import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.layouts import row, column
from bokeh.models import Select
from bokeh.plotting import figure, show

##### Load the data file

file = "stats.tsv"
df = pd.read_csv(file, sep="\t")

df = df.drop(['Assembly.quality', 'Source', 'Release raw and assemblies in data note'], axis=1)

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,previewsave"
SIZES = list(range(6, 22, 3))
COLORS = ['#175676', '#A4036F', '#419D78', '#E0A458']
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)


def create_figure():
    """
    Construct and return a scatter plot from a Pandas dataframe.
    :return: pandas plot
    """

    """
    Define lists of the values that belong to the columns chosen as x and y values, then
    set their titles.
    """
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    """
    Declare a dictionary and set its key:value pairs according to the values that appear in the
    chosen data for the x and y axes.
    """
    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    """
    Declare a plot and set its axis labels.
    """
    p = figure(plot_width=1200, plot_height=550, **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    """
    If the x-values are discrete, rotate the text for these values 45 degrees counterclockwise.
    """
    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#0B3142"
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
            # groups = pd.Categorical(df[color.value])
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]

    """
    Represent the data points on the plot as circles.
    """
    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.8, hover_color='white', hover_alpha=0.5)
    #    p.circle(x=xs, y=ys, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='Latin_name', options=columns)
x.on_change('value', update)
y = Select(title='Y-Axis', value='Contig_N50..bp.', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='Source2', options=['None', 'Source2'])
color.on_change('value', update)

controls = row([x, y, color, size], width=400)
layout = column(controls, create_figure())

curdoc().add_root(layout)
# output_file("genome_statistics.html")
# save(layout)
show(layout)
print("x:\n", x)
print("\n\nx.value:\n", x.value)
print("\n\ndf[x.value]\n", df[x.value])
print("\n\ndf[x.value]\n", df[x.value].values)
print("\n\ny:\n", y)
print("\n\ny.value:\n", y.value)
print("\n\ndf[y.value]\n", df[y.value])
print("\n\ndf[y.value]\n", df[y.value].values)