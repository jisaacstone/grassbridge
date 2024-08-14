#!/usr/bin/env python3
import grass.script as gs


gs.setup.init('grassdata/latlng')


# import PA bridge data
gs.run_command('v.in.db', database='datasets/bridges.db',
               driver='sqlite', table='bridges',
               x='longitude', y='latitude', out='bridges')


# link the shapefiles
for shapefile, newname in (('tl_2022_us_county', 'county'), ('tl_2022_us_uac20', 'city')):
    #gs.run_command('v.external', input='datasets',
    #               layer=shapefile)
    gs.run_command('v.import',
                   input=f'datasets/{shapefile}.shp',
                   output=newname)
    # gs.run_command('g.copy', vector=f'{shapefile},{newname}')

gs.run_command('db.tables')
