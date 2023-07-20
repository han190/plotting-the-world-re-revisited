reset
set terminal pngcairo size 600, 600 enhanced

# Input files
coastline = "./data/ne_50m_coastline.bin"
states = "./data/ne_50m_admin_1_states_provinces.bin"
countries = "./data/ne_50m_admin_0_countries.bin"
lakes = "./data/ne_50m_lakes.bin"
land = "./data/ne_50m_land.bin"
rivers = "./data/ne_50m_rivers_lake_centerlines.bin"



# color definitions
# set border lw 1.5
set linetype 1 linecolor rgb 'white' linewidth 1
set linetype 2 linecolor rgb 'black' linewidth 1.5
set linetype 3 linecolor rgb 'gray50' linewidth 1

unset key
unset border
set tics scale 0
set lmargin screen 0
set bmargin screen 0
set rmargin screen 1
set tmargin screen 1
set format ''

set mapping spherical
set angles degrees
set hidden3d front
set xyplane at -1
set view 40, 0

set parametric
set isosamples 36, 36
set xrange [-1:1]
set yrange [-1:1]
set zrange [-1:1]
set urange [-180:180]
set vrange [-90:90]
set output 'world.png'

r = 1.0
binary_format="%float%float"
strokes="binary format=binary_format using 1:2:(r) with lines"
fills="binary format=binary_format using 1:2:(r) with polygons"

splot \
  r*cos(v)*cos(u), r*cos(v)*sin(u), r*sin(v) with lines linecolor 'gray', \
  coastline @strokes linecolor 'black'      linewidth 1, \
  states    @strokes linecolor 'gray70'     linewidth 1, \
  rivers    @strokes linecolor 'light-blue' linewidth 1, \
  countries @strokes linecolor 'black'      linewidth 1, \
  lakes     @fills   linecolor 'light-blue' linewidth 1, \
  lakes     @strokes linecolor 'web-blue'   linewidth 1
