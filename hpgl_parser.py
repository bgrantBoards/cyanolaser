"""
functions for parsing an hpgl file generated from Inkscape

#####################################################
INSTRUCTIONS FOR GENERATING HPGL FILES FROM INKSCAPE:

- Open any cool svg you want in inkscape

- Set the canvas size equal to the bed size of the cyanolaser

- Make sure all text has been converted to paths via Path > Object to Path
  Use a single stroke font such as "CNC Vector" for doing excited text

- Go to File > Save and save the svg as "HP Graphics Language file (.hpgl)"

- A window will come up with some settings options
    - Resolution X (dpi) and Resolution Y (dpi) are the settings for steps per
      inch. Set both of them to [i can't remember what the spi of the cyanolaser
      is]
    - Pen number: 1
    - Pen force:  0
    - Pen speed:  0
    - Rotation:   0
    - Check the "Center zero point" box

- Go to the Plot Features tab
    - Overcut:                0
    - Tool offset correction: 0
    - Curve flatness:         0.1
    - Make sure that the precut and autoalign boxes are unchecked

- Click OK
"""

# from os import path

def get_polyline(polyline_string, dpi):
    """
    Returns a polyline (list of coordinates with each coordinate being a list of
    [x,y]) from a string in "x1,y1,x2,y2,..." form

    Args:
        polyline_string (string): polyline coords in "x1,y1,x2,y2,..." form
        dpi (int): steps per inch value that the hpgl file was generated with.
        This is used for converting to inches global coordinate system.
    """
    unsorted_coords = polyline_string.split(",")
    polyline = []
    for i in range(len(unsorted_coords)//2):
        x_i = int(unsorted_coords[i*2])   / dpi
        y_i = int(unsorted_coords[i*2+1]) / dpi
        polyline.append([x_i, y_i])
    return polyline


def get_multiple_polylines(polyline_strings, dpi):
    """
    Returns a list of polylines (each polyline is a list of coordinates and
    each coordinate is a list [x,y])

    Args:
        polyline_strings (list of strings): list of strings in
        "x1,y1,x2,y2,..." form
        dpi (int): steps per inch value that the hpgl file was generated with.
        This is used for converting to inches global coordinate system.
    """
    return [get_polyline(polyline_string, dpi) for polyline_string in \
                                                   polyline_strings]

def get_polylines_from_hpgl(filepath, dpi):
    """
    Generates and returns a list of polylines from an hpgl file

    Args:
        filepath (string): path to the hpgl file

        dpi (int): steps per inch value that the hpgl file was generated with.
        This is used for converting to inches global coordinate system.
    """
    with open(filepath, "r") as file:
        # read the one-liner hpgl file into a string
        lines = file.readlines()
        # create list of lines in the hpgl file
        lines = lines[0].split(";")

        # list of all pen down commands
        path_lines = [line for line in lines if line[0:2] == "PD"]

        # create list of all unsorted poly lines, e.g. "x1,y1,x2,y2,x3,y3"
        # which in [x,y] form should be [[x1,y1],[x2,y2],[x3,y3]
        unsorted_polylines = [line[2:] for line in path_lines]

        return get_multiple_polylines(unsorted_polylines, dpi)


# check the output:

# polylines = get_polylines_from_hpgl("/Users/bengrant/school/PIE/cyanolaser/vector/shapes.hpgl", 500)
# for pl in polylines:
#     print(pl)
#     print("\n\n\n")
