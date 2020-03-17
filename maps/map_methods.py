from ipyleaflet import Map, Marker, AntPath, MarkerCluster, AwesomeIcon, Popup, basemaps, basemap_to_tiles, Polygon, Polyline
from ipywidgets import HTML

import pandas as pd

def get_macedonia_map():
    center=(41.6086, 21.7453)

    m = Map(
        layers=(basemap_to_tiles(basemaps.OpenStreetMap.Mapnik), ),
        center=center,
        zoom=8,
        scroll_wheel_zoom=True
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
        close_on_escape_key=False,
        keep_in_view=True
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


def add_path_layer(m, d, from_lat='from_lat', from_lng='from_lng', to_lat='from_lat', to_lng='to_lng', cols=[],
                   names=None, get_path=None):
    if names is None:
        names = cols

    paths = list()

    for ind in d.index:
        row = d.loc[ind]
        # if get_marker is None:
        #     marker = Marker(location=location, draggable=False)
        # else:
        #     marker = get_marker(ind, location, row)
        from_loc = [row[from_lat], row[from_lng]]
        to_loc = [row[to_lat], row[to_lng]]
        locations = [from_loc, to_loc]
        if get_path is None:
            ant_path = AntPath(locations=locations)
        else:
            ant_path = get_path(locations, row)

        m.add_layer(ant_path)


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
    
def add_polygon_layer(m, locations, border_color='black', opacity=1, fill_color=None, fill_opacity=0, weight=3):
    polygon = Polygon(
        locations=locations,
        color=border_color,
        opacity=opacity,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        weight=weight
    )
    m.add_layer(polygon)
    
def get_points_for_polygon_from_line_data(d, line_group, point_id, lat='lat', lon='lon'):
    points = list()
    past_ways = list()
    
    first = True
    way = d[line_group].iloc[0]
    while way not in past_ways:
        past_ways.append(way)
        nodes = d.loc[d[line_group]==way]
        if first:
            first = False
        elif last_node_id != nodes[point_id].iloc[0]:
            nodes = nodes.iloc[::-1]
        points = points + get_lat_lon_points_from_data(d=nodes, lat=lat, lon=lon)
        last_node_id = nodes[point_id].iloc[-1]
        way = d.loc[(d[point_id]==last_node_id) & (d[line_group]!=way)]['WayId'].iloc[0]
        
    return points
    
    
    
def get_lat_lon_points_from_data(d, lat='lat', lon='lon'):
    points = list()
    for ind in d.index:
        row = d.loc[ind]
        points.append((row[lat], row[lon]))
        
    return points
    
    
    
    