#!/usr/bin/env python3
import grass.script as gs
gs.setup.init('grassdata/latlng')
gs.run_command('v.in.db', database='datasets/bridges.db',
               driver='sqlite', table='bridges',
               x='longitude', y='latitude', out='bridges')
