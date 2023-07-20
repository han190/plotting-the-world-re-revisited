import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon, LineString, MultiLineString
import numpy as np
import subprocess
import sys


def extract_coords(polygon):
    """Extract coordinates from a polygon"""
    if type(polygon) is Polygon:
        x, y = polygon.exterior.coords.xy
    elif type(polygon) is LineString:
        x, y = polygon.coords.xy
    ret = (np.vstack([x, y]).T).tolist()
    return ret


def shp2latlon(filename, format):
    """
    Read shape file and convert it to
    gnuplot-ready text and binary files.
    """
    shapefile = gpd.read_file(filename)
    shapes = []
    for i, polygons in enumerate(shapefile["geometry"]):
        if "featurecla" in shapefile:
            if shapefile["featurecla"][i] == "Reservoir":
                continue  # Skip Reservoir

        if type(polygons) is Polygon:
            polygon = polygons
            shapes.append(extract_coords(polygon))
        elif type(polygons) is LineString:
            polygon = polygons
            shapes.append(extract_coords(polygon))
        elif type(polygons) is MultiPolygon:
            for polygon in list(polygons.geoms):
                shapes.append(extract_coords(polygon))
        elif type(polygons) is MultiLineString:
            for polygon in list(polygons.geoms):
                shapes.append(extract_coords(polygon))

    if format == "binary":
        binary_file = open(filename.replace("shp", "bin"), "wb")
        nan_sp = np.array([np.nan, np.nan], dtype=np.float32)
        for shape in shapes:
            for coord in shape:
                coord_sp = np.array(coord, dtype=np.float32)
                binary_file.write(coord_sp)
            binary_file.write(nan_sp)
        binary_file.close()
    elif format == "text":
        text_file = open(filename.replace("shp", "txt"), "w")
        for shape in shapes:
            for coord in shape:
                coord_sp = np.array(coord, dtype=np.float32)
                binary_file.write(coord_sp)
                text_file.write("{} {}\n".format(*coord_sp))
            text_file.write("\n")
        text_file.close()
    else:
        sys.exit("Invalid format.")

    return shapes


def run_command(cmd, verbose=True):
    """Run command line"""
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


def convert_shape(types, ress, keep_download=False, format="binary"):
    site_url = "https://www.naturalearthdata.com/"
    download_url = site_url + "http//www.naturalearthdata.com/download/"

    def proc(resolution, major_type, minor_type):
        zip_file = "ne_{}m_{}.zip".format(resolution, minor_type)
        url = download_url + "{}m/{}/".format(resolution, major_type) + zip_file
        run_command("wget {}".format(url))
        zip_dir = zip_file.replace(".zip", "")
        run_command("rm -rf {}".format(zip_dir))
        run_command("unzip {} -d {}".format(zip_file, zip_dir))
        run_command("mv {} {}".format(zip_file, zip_dir))
        shp_file = zip_file.replace(".zip", ".shp")
        shp2latlon("{}/{}".format(zip_dir, shp_file), format=format)

        bin_file = zip_file.replace(".zip", ".bin")
        run_command("mv {}/{} .".format(zip_dir, bin_file))
        if not keep_download:
            run_command("rm -rf {}".format(zip_dir))

    for resolution in ress:
        for major_type in types:
            for minor_type in types[major_type]:
                proc(resolution, major_type, minor_type)


if __name__ == "__main__":
    types = {
        "physical": ["coastline", "lakes", "rivers_lake_centerlines"],
        "cultural": ["admin_0_countries", "admin_1_states_provinces"],
    }
    ress = [110, 50, 10]
    convert_shape(types, ress)
