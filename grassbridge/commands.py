import grass.script as gs
from pathlib import Path


def init():
    gs.setup.init('grassdata/latlng')
    gs.run_command(
        'g.region',
        vector='bridges',
        res='0:00:01',
        flags='pa'
    )
    gs.run_command('db.tables')

def stats(regions, column, method):
    raster_name = f'{regions}_{column}_{method}'
    img_file = f'{raster_name}.png'
    img_path = Path(f'grassbridge/static/{img_file}')
    if not img_path.exists():
        gs.run_command(
            'v.vect.stats',
            points='bridges',
            areas=regions,
            method=method,
            points_column='YEAR_BUILT_027',
            stats_column=method,
            count_column='count',
            # areas_where="STATEFP = '41'"
        )
        gs.run_command(
            'v.to.rast',
            type='area',
            input=regions,
            output=raster_name,
            # where=f'{method} not NULL',
            use='attr',
            attribute_column=method,
        )
        gs.run_command(
            'r.colors',
            map=raster_name,
            color='viridis'
        )
        gs.run_command(
            'r.out.png',
            input=raster_name,
            output=str(img_path)
        )
    return img_file


def run_command(form_data):
    print(form_data)
    img_file = stats(
        form_data.get('regions', 'counties'),
        form_data.get('column', 'YEAR_BUILT_027'),
        form_data.get('method', 'average')
    )
    return {'img': img_file}
