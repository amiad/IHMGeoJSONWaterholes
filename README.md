# IHMGeoJSONWaterholes
GeoJSON for an external layer for [IHM](israelhiking.osm.org.il/) site.
The source is [the floods and waterholes list](https://docs.google.com/spreadsheets/d/1BbT762qaYilLnwGD7sJDo8sfs_Y5ExjvixS_Tl3rSas/edit?usp=sharing).
The conversion was performed using [csv2geojson](http://mapbox.github.io/csv2geojson/).


Requirements:
1. geojson source file available online and that is CORS enabled. Can be achived with github and [Githack](https://raw.githack.com/) as can be seen in this repo.
2. `style.json` file that has a `metadata: { "IHM:Overlay": true }` foreach layer. This file is used as the address in the IHM site for a custom layer.
