

# google maps constants (inaccurate observations)
zoom11_half_width = 0.2193835
zoom11_half_height = 0.157381
zoom12_half_width = zoom11_half_width / 2
zoom12_half_height = zoom11_half_height / 2
zoom13_half_width = zoom12_half_width / 2
zoom13_half_height = zoom12_half_height / 2

# Bucharest center (near Universitate).
# Pictures were taken from http://maps.googleapis.com/maps/api/staticmap?center=44.4378257,26.0946376&zoom=11&size=640x640  // 640x640 is the maximum
city_center_y = 44.4378257
city_center_x = 26.0946376

image_filename = "b12.png"
margin_y0 = city_center_y + zoom12_half_height
margin_y1 = city_center_y - zoom12_half_height
margin_x0 = city_center_x - zoom12_half_width
margin_x1 = city_center_x + zoom12_half_width

coord_width = margin_x1 - margin_x0
coord_height = margin_y0 - margin_y1

# check if coordinates are inside the map
def is_inside(x, y):
    return (margin_y0 > y and margin_y1 < y and margin_x0 < x and margin_x1 > x)

# Transform coordinates to screen coordinates
def c2s_x(x):
    return int((640 * x - 640 * margin_x0) / coord_width)

def c2s_y(y):
    return int((640 * margin_y0 - 640 * y) / coord_height)



