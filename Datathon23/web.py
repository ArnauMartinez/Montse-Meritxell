from flask import Flask, render_template, request, url_for, redirect, session
from howtograph import *
import folium


app = Flask(__name__)

filter_dict = {}


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'Campus' in request.form:
            filter_dict['Campus']= request.form.getlist('Campus')
        if 'Transport' in request.form:
            filter_dict['Transport'] = request.form.getlist('Transport')
        if 'Provincies' in request.form:
            filter_dict['provincies']= request.form.getlist('Provincies')
            return redirect(url_for('map'))
    
            

    return render_template('index.html')
@app.route("/map", methods=['GET', 'POST'])
def map():
    #map_filepath = 'UPCmap.html'
    geoPaths = config_data()
    center_coord = (41.39393, 2.15896)
    vmap = folium.Map(location=center_coord, zoom_start = 8)
    
    colormap = create_colormap("step",0, 63)
    add_zip_codes(vmap, geoPaths, colormap, filter_dict['provincies'])

    vmap.get_root().render()
    
    header = vmap.get_root().header.render()
    body_html = vmap.get_root().html.render()
    script = vmap.get_root().script.render()

    if (request.method == 'POST'):
        return redirect(url_for('index'))
        
    return render_template('map.html', filters = filter_dict, head = header, html = body_html, script = script)

            
    
    


if __name__ == '__main__':
    app.run(debug= True)