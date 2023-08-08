# Plotting the world re-revisited
Although with no actual data, I'm pretty sure that the blog [Plotting the world](http://www.gnuplotting.org/plotting-the-world/) and [Plotting the world revisited](http://www.gnuplotting.org/plotting-the-world-revisited/) have been visited and used by many many gnuplot users. However, the shell script provided by the blog to convert downloaded `.shp` file is a bit outdated (the original blog was posted 13 years ago). Thus, I wrote a python script to download data from [Natural Earth](https://www.naturalearthdata.com/downloads/), and convert `.shp` file to gnuplot-ready binary files. You could download the gnuplot-ready binary files from the releases. If you want to modify the python script, clone this repo, navigate to the repository and 
```
python ./src/shapefile_converter.py
```

## Examples

Map of the world.
![](images/world_dark.png#gh-dark-mode-only)
![](images/world_light.png#gh-light-mode-only)

