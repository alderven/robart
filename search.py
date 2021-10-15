import sys
import requests
from requests.auth import HTTPBasicAuth

# HTML table
TABLE_HEADER = '''<table id="table_id" class="display">
<thead>
  <tr>
    <th>Name</th>
    <th>Created at</th>
    <th>Pushed at</th>
    <th>Size</th>
    <th>Language</th>
    <th>Watched count</th>
  </tr>
</thead>
<tbody>
'''

TABLE_FOOTER = '</tbody></table>'


def search(user, watchers):
    """ Search GitHub user and generate HTML page with search results
    :param user: GitHub user name
    :param watchers: min number of watchers
    :return: HTML page
    """

    # 1. Read template page
    with open('page.html', 'r', encoding='utf-8') as f:
        page = f.read()

    # 1. Make API call to GitHub
    if user:
        r = requests.get(url=f'https://api.github.com/users/{user}/repos', auth=HTTPBasicAuth('', sys.argv[1]))

        # Generate table if user found
        if r.status_code == 200:
            table = TABLE_HEADER
            for repo in r.json():
                if repo['watchers_count'] >= watchers:  # filter min number by watchers
                    table += f"<td> <a target='blank' href='https://github.com/{user}/{repo['name']}'>{repo['name']}</a></td>" \
                             f"<td>{repo['created_at']}</td>" \
                             f"<td>{repo['pushed_at']}</td>" \
                             f"<td>{repo['size']}</td>" \
                             f"<td>{repo['language']}</td>" \
                             f"<td>{repo['watchers_count']}</td>" \
                             f"</tr>"
            page += table + TABLE_FOOTER

        # Show error message if user not found on GitHub
        else:
            page = page.replace('<!-- table -->', f'<h2>No data found for user: {user}</h2>')
            return page

    return page
