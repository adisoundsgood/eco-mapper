# eco-mapper

eco-mapper is a web-based geospatial analysis tool that processes and visualizes environmental data to support ecosystem service mapping and decision-making. The purpose of this project is to deepen my understanding of ecosystem service calculations and how they impact environmental research and decision-making..

## Project Goals

- Provide an easy-to-use interface for uploading and processing geospatial data
- Perform various ecological and environmental calculations on GeoTIFF files
- Visualize results to aid in ecosystem service assessment and land management decisions

## Calculations Performed
eco-mapper currently supports the following calculations:

### NDVI (Normalized Difference Vegetation Index)

- Assesses vegetation health and density
- Uses Near-Infrared (NIR) and Red bands from multispectral imagery
  
### Slope and Aspect

- Calculates terrain characteristics from Digital Elevation Models (DEMs)
- Useful for understanding topographic influences on ecosystems

### Carbon Storage Estimation

- Estimates carbon storage based on land cover types
- Helps in assessing the carbon sequestration potential of different areas

## Technology Stack

- Frontend: React.js
- Backend: Flask (Python)
- Geospatial Processing: GDAL, NumPy
- Deployment: Heroku

## Usage
eco-mapper is deployed on Heroku and is available to use here: [https://eco-mapper-e076ecd49dfb.herokuapp.com/]([url](https://eco-mapper-e076ecd49dfb.herokuapp.com/))

License
[Specify the license under which your project is released]

Contact
Aditya Iyer
adityasuiyer@gmail.com
