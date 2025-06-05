from math import cos, radians, sqrt

def calcular_distancia(lat1, lon1, lat2, lon2):
  lat1_rad, lat2_rad = radians(lat1), radians(lat2)
  lat_media = (lat1_rad + lat2_rad) / 2
  dx = 111320 * cos(lat_media) * (lon2 - lon1)
  dy = 111320 * (lat2 - lat1)
  return sqrt(dx**2 + dy**2)
