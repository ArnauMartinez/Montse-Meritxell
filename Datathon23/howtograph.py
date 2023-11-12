import folium
import geopandas as gpd
import branca.colormap as cm
import pandas as pd



alumnes_renamed = pd.read_csv('Dataset1.csv')

def find_popup_slice(html):
    '''
    Find the starting and edning index of popup function
    '''

    pattern = "function latLngPop(e)"

    # startinf index
    starting_index = html.find(pattern)

    #
    tmp_html = html[starting_index:]

    #
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == "{":
            found += 1
            opening_found = True
        elif tmp_html[index] == "}":
            found -= 1

        index += 1

    # determine the edning index of popup function
    ending_index = starting_index + index

    return starting_index, ending_index

def find_map_variable_name(html):
    pattern = "var map_"

    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def find_popup_variable_name(html):
    pattern = "var lat_lng"

    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def custom_code(popup_variable_name, map_variable_name):
    return '''
            // custom code
            function latLngPop(e) {
                %s
                    .setLatLng(e.latlng)
                    .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                "<br>Longitude: " + e.latlng.lng.toFixed(4))
                    .openOn(%s);

                console.log("Latitude: " + e.latlng.lat.toFixed(4));
                console.log("Longitude: " + e.latlng.lng.toFixed(4));
            }
            // end custom code
    ''' % (popup_variable_name, map_variable_name)


def how_many(postal_code:str, codis):
    a = sum(int(postal_code) == codis)
    return a

def config_data():
    filepaths = ['Data/Geometries/Barcelona.geojson', 'Data/Geometries/Girona.geojson', 'Data/Geometries/Lleida.geojson', 'Data/Geometries/Tarragona.geojson']
    geoPaths = []
    for filepath in filepaths:
        file = open(filepath, 'r')
        geoPaths.append(file.read())
    return geoPaths

def add_zip_codes(vmap, geoPaths,colormap, provincies, function = how_many):
    i = 0 
    for geoPath in geoPaths:
        if str(i) in provincies:
            folium.GeoJson(
            data = geoPath,
            style_function = lambda feature: {
                
                "fillColor": colormap(function(feature['properties']['COD_POSTAL'], alumnes_renamed['POSTAL_CODE'])),
                "color": "black",
                "weight": 2,
                "dashArray": "5, 5",
                "fill_opacity": 1
            }
            ).add_to(vmap)
        i = i + 1

    colormap.add_to(vmap)
    
def create_colormap(type, min_val, max_val):
    if type == "step":
        colormap = cm.StepColormap(
        ["green", "yellow", "orange", "red"], vmin=min_val, vmax=max_val, index=[0,1,5,15,63], caption="step")
    elif type == "discrete":
        colormap = cm.StepColormap(
        ["blue", "red"], vmin=0, vmax=1, index=[0,1], caption="step")
    else:
        colormap = cm.LinearColormap(["green", "yellow", "orange", "red"], vmin=min_val, vmax=max_val, index=[0,1,5,15,63], caption="step")
    return colormap




if __name__ == '__main__':
    map_filepath = 'UPCmap.html'
    geoPaths = config_data()
    center_coord = (41.39393, 2.15896)
    vmap = folium.Map(location=center_coord, zoom_start = 10)
    
    colormap = create_colormap("step",0, 63)
    add_zip_codes(vmap, geoPaths, colormap)

    

    #vmap.save(map_filepath)

    
