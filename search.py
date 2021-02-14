from decouple import config
import requests
import statistics


TMDB_AUTH_TOKEN = config('TMDB_AUTH_TOKEN')
TMDB_URL = 'https://api.themoviedb.org/3/search/movie'
STATS = {
    'All': 'all',
    'Sum': 'sum',
    'Mean': 'mean',
    'Median': 'median',
    'Standard Deviation': 'stdev',
    'Null count': 'null_count',
    'Count': 'len',
    'Count Distinct': 'dist_count'
}


def get_from_tmdb(search_query):
    query_params = {}
    if not search_query.isalpha():
        raise AttributeError
    query_params.update({
        'api_key': TMDB_AUTH_TOKEN,
        'query': search_query,
        'language': 'en-US'
    })
    response = requests.get(TMDB_URL, query_params)

    return response.json()


def get_valid_statistics(values):
    if all([isinstance(value, int) or isinstance(value, float) for value in values]):
        return 'num'
    else:
        return 'not_num'


def get_columns(response):
    assert response['total_results']
    columns = response['results'][0].keys()

    for _ in enumerate(columns):
        print(f"{_[0]}: {_[1]}")

    column_selection = input("Enter property for which stats are required\n")
    values = [_[list(columns)[int(column_selection)]] for _ in response['results']]

    for _ in enumerate(STATS):
        print(f"{_[0]}: {_[1]}")

    stat_selection = input("Enter stat\n")
    try:
        result = getattr(statistics, list(STATS.values())[int(stat_selection)])(values)
        print(f"{list(STATS.keys())[int(stat_selection)]}: {result}")
    except:
        print('Duh duh duh')


if __name__ == '__main__':
    search_query = input("Please Enter a search query\n")
    response = get_from_tmdb(search_query)
    columns = get_columns(response)
