
#Import earth engine
import ee

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

#LSIB: Large scale international boundary polygon
dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
visParams = {
    'paltte': ['f5ff64', 'b5ffb4', 'beeaff', 'ffc0e8', '8e8dff', 'adadad'],
    'min': 0.0,
    'max': 894,
    'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'iso_num')

# Export the FeatureCollection to a csv file.
task = ee.batch.Export.table.toDrive(**{
  'collection': dataset,
  'description':'country_names',
  'fileFormat': 'CSV'
})
task.start()

print(dataset.limit(5).getInfo())

# Import the Folium library.
import folium

# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name = name,
    overlay = True,
    control = True
  ).add_to(self)

# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Create a folium map object.
my_map = folium.Map(location=[37.649, -99.844], zoom_start = 2)

# Add the layer to the map object.
my_map.add_ee_layer(image, visParams, 'USDOS/LSIB/2013')

# Add a layer control panel to the map.
my_map.add_child(folium.LayerControl())

# Display the map.
display(my_map)
