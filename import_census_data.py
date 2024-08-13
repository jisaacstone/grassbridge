#!/usr/bin/env python3
import grass.script as gs
import grass.exceptions
gs.setup.init('grassdata/latlng')
# TODO: why does this throw an error?
try:
    gs.run_command('v.in.db', database='datasets/bridges.db',
                   driver='sqlite', table='bridges',
                   x='longitude', y='latitude', out='bridges')
except grass.exceptions.CalledModuleError:
    pass

gs.run_command('v.external', input='datasets',
               layer='tl_2022_us_county',
               output='county')
