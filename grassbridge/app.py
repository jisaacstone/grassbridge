from flask import Flask, request, render_template

from . import commands

base_context = {
    'regions': {
        'counties': 'tl_2022_us_county',
        'cities': 'tl_2022_us_uac20'
    },
    'commands': {
        'stats': 'stats',
    },
    'methods': [
        'sum',
        'average',
        'median',
        'mode',
        'minimum',
        'maximum',
        'range',
        'stddev',
        'variance',
        'diversity'
    ],
    'columns': {
        'year built': 'YEAR_BUILT_027',
        'traffic lanes': 'TRAFFIC_LANES_ON_028A',
        'daily traffic': 'ADT_029',
        'design load': 'DESIGN_LOAD_031',
        'degrees skew': 'DEGREES_SKEW_034',
    }
}


def create_app():
    app = Flask('grassbridge')
    commands.init()

    @app.route('/', methods=('GET', 'POST'))
    def main():
        if request.method == 'POST':
            results = commands.run_command(request.form)
        else:
            results = {}

        return render_template('index.html', results=results, **base_context)

    return app
