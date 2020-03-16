from ipyleaflet import Map, Marker, MarkerCluster, AwesomeIcon, Popup, basemaps, basemap_to_tiles, Polygon, Polyline
from ipywidgets import HTML

import pandas as pd

def get_macedonia_map():
    center=(41.6086, 21.7453)

    m = Map(
        layers=(basemap_to_tiles(basemaps.OpenStreetMap.Mapnik), ),
        center=center,
        zoom=8
    )
    
    return m

def get_popup_html_message(name, row, cols, names):
    text = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }

        td, th {
          border: 1px solid #999999;
          text-align: left;
          padding: 2px;
        }

        tr:nth-child(even) {
          background-color: #eeeeee;
        }
        </style>
        </head>
        <body>

        <h4>""" + name + """</h4>

        <table>
    """
    for i, col in enumerate(cols):
        text += """
            <tr>
                <td>""" + str(names[i]) + """</td>
                <td>""" + str(row[col]) + """</td>
            </tr>
        """
    text +="""
    </table>

    </body>
    </html>
    """
    message = HTML()
    message.value = text
    return message
    
def get_popup(message):
    popup = Popup(
        child=message,
        close_button=True,
        auto_close=False,
        close_on_escape_key=False
    )
    return popup

def add_marker_layer(m, d, lat='lat', lng='lng', cols=[], names=None, get_marker=None, hide_marker=None):
    if names is None:
        names = cols
    
    marker_list = list()

    for ind in d.index:
        row=d.loc[ind]
        if hide_marker is not None and hide_marker(ind, row):
            continue
        location = (row[lat], row[lng])
        if get_marker is None:
            marker = Marker(location=location, draggable=False)
        else:
            marker = get_marker(ind, location, row)
        
        
        marker.popup = get_popup(get_popup_html_message(ind, row[cols], cols, names))
        marker_list.append(marker)



    markers = MarkerCluster(markers=tuple(marker_list))
    m.add_layer(markers)

def add_polygon_layer(m, d, lat='lat', lon='lon', border_color='black', opacity=1, fill_color='black', fill_opacity=0.3):
    locations = list()
    for ind in d.index:
        row = d.loc[ind]
        locations.append((row[lat], row[lon]))

    polygon = Polygon(
        locations=locations,
        color=border_color,
        opacity=opacity,
        fill_color=fill_color,
        fill_opacity=fill_opacity
    )

    m.add_layer(polygon)
    
def add_polyline_layer(m, d, line_group, lat='lat', lon='lon', border_color='black', opacity=1, fill_color=None, fill_opacity=0, weight=3):
    all_locations = dict()
    for ind in d.index:
        row = d.loc[ind]
        locations = list()
        if row[line_group] in all_locations.keys():
            locations = all_locations[row[line_group]]
        locations.append((row[lat], row[lon]))
        all_locations[row[line_group]] = locations
        
    polyline = Polyline(
        locations=list(all_locations.values()),
        color=border_color,
        opacity=opacity,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        weight=weight
    )
    
    m.add_layer(polyline)
