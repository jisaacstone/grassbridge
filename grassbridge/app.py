from flask import Flask, request, render_template


base_context = {
    'regions': {
        'counties': 'tl_2022_us_county',
        'cities': 'tl_2022_us_uac20'
    },
    'commands': {
    }
}


def create_app():
    app = Flask('grassbridge')

    @app.route('/', methods=('GET', 'POST'))
    def main():
        if request.method == 'POST':
            results = run_grass(request.form)
        else:
            results = {}

        return render_template('index.html', results=results, **base_context)

    return app
