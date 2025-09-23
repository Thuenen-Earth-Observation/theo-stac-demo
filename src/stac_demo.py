# Import necessary libraries: pystac_client to interact with the STAC API, stackstac to create data stacks, and geogif to generate animated GIFs.
from pystac_client import Client
import stackstac
import geogif

# Define the STAC API endpoint. This URL points to the STAC service providing remote sensing data.
STACK_ENDPOINT = "https://eodata.thuenen.de/stac/api/v1/"

# Open the STAC catalog using the defined endpoint. This allows us to browse available collections and items.
catalog = Client.open(STACK_ENDPOINT)

# Print all available collections in the catalog for verification and debugging purposes.
[print(i) for i in catalog.get_collections()]

# Define the geographic bounding box as a tuple (min_lon, min_lat, max_lon, max_lat) for the area of interest.
bbox = (8.25, 52.445, 8.4, 52.585)

# Search the catalog for items within the specified bounding box, collection, and date range.
# - collections: "crop-type-map-latest" restricts the search to the latest crop type maps.
# - datetime: "2017-01-01/2025-12-31" limits the search to items within this date range.
search = catalog.search(
    collections="crop-type-map-latest",
    bbox=bbox,
    datetime="2017-01-01/2025-12-31"
)

# Retrieve the search results as a list of STAC items.
items = list(search.items())

# The 'items' variable holds all the search results
print(items)

# Create a mosaic stack from the retrieved STAC items using stackstac.
# - resolution: Specifies the spatial resolution (10,10) in the target units.
# - bounds_latlon: Defines the spatial extent using the bounding box.
# - epsg: Sets the coordinate reference system (3035 in this case) for the stack.
mosaic_stack = stackstac.stack(
    items=items,
    resolution=(10,10),
    bounds_latlon=bbox,
    epsg=3035
) 

# Select only the 'data' band from the mosaic stack for visualization.
mosaic_stack = mosaic_stack.sel(band=["data"])

# Generate an animated GIF from the mosaic stack.
# - fps: Frames per second (speed of the animation)
# - cmap: Colormap used for displaying the data ("tab20" in this case)
# - bytes: Outputs the GIF in byte format, suitable for writing to a file
gif = geogif.dgif(mosaic_stack, fps=1, cmap="tab20", bytes=True).compute()

# Save the generated GIF to the 'output' directory as 'crop_type_series.gif'.
with open("output/crop_type_series.gif", "wb") as f:
    f.write(gif)
