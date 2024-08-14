import grass.script as gs


def init():
    gs.setup.init('grassdata/latlng')
    gs.run_command(
        'g.region',
        vector='bridges',
        flags='pa'
    )

def stats(regions, column, method):
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
        'v.colors',
        map=regions,
        use='attr',
        column=method,
        color='viridis'
    )
    output_name = f'{regions}_{column}_{method}.svg'
    gs.run_command(
        'v.out.svg',
        input=regions,
        output=f'grassbridge/static/{output_name}'
    )
    return output_name


def run_command(form_data):
    print(form_data)
    img_file = stats(
        form_data.get('regions', 'tl_2022_us_county'),
        form_data.get('column', 'YEAR_BUILT_027'),
        form_data.get('method', 'average')
    )
    return {'img': img_file}
