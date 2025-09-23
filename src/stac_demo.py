from pystac_client import Client
import stackstac
import geogif

# Define the STAC API endpoint
STACK_ENDPOINT = "https://eodata.thuenen.de/stac/api/v1/"

# Open the STAC catalog using the defined endpoint
catalog = Client.open(STACK_ENDPOINT)

[print(i) for i in catalog.get_collections()]

# Define bounding box
bbox = [8.25, 52.445, 8.4, 52.585]

search = catalog.search(
    collections="crop-type-map-latest",
    bbox=bbox,
    datetime="2017-01-01/2025-12-31"
)

items = list(search.items())
items

mosaic_stack = stackstac.stack(
    items=items,
    resolution=(10,10),
    bounds_latlon=bbox,
    epsg=3035,
)

mosaic_stack = mosaic_stack.sel(band=["data"])

gif = geogif.dgif(mosaic_stack, fps=1, cmap="tab20", bytes=True).compute()

with open("ti_crop_type.gif", "wb") as f:
    f.write(gif)
