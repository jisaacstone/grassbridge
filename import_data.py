#!/usr/bin/env python3
import grass.script as gs
import grass.exceptions


gs.setup.init('grassdata/latlng')


# import PA bridge data
gs.run_command('v.in.db', database='datasets/bridges.db',
               driver='sqlite', table='bridges',
               x='longitude', y='latitude', out='bridges')


# link the shapefiles
for shapefile in ('tl_2022_us_county', 'tl_2022_us_uac20'):
    gs.run_command('v.external', input='datasets',
                   layer=shapefile)
