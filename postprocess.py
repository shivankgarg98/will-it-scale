#!/usr/bin/python3

import sys
import os
import csv
import json
import string

template = '''
<html>
<head>
  <title>Will it scale?</title>
  <script src="https://cdn.plot.ly/plotly-3.1.0.min.js" charset="utf-8"></script>
  <script src="plot.js"></script>
</head>

<body>
  <div id="plot"></div>
  <script>
    var data = $data;
    createPlot(data, '$title');
  </script>
</body>
</html>
'''

def parse_data(csvfile):
    data = []
    fp = open(csvfile)
    csv_reader = csv.reader(fp, dialect='excel')
    for row in csv_reader:
        data.append(row)
    fp.close()
    return data


def process(base):
    csvfile = base + '.csv'
    titlefile = base + '.title'
    htmlfile = base + '.html'

    try:
        data = parse_data(csvfile)
        try:
            with open(titlefile, 'r') as f:
                title = f.readline().strip()
        except FileNotFoundError:
            title = f"Chart for {base}"
            print(f"Warning: {titlefile} not found, using default title")

        json_data = json.dumps(data)
        t = string.Template(template)
        html = t.substitute(data=json_data, title=title)

        with open(htmlfile, 'w') as f:
            f.write(html)
        print(f'Created {htmlfile}')

    except Exception as e:
        print(f"Error processing {base}: {e}")
        return False

if __name__ == '__main__':

    for root, dirs, files in os.walk('.'):
        if root == '.':
            for f in files:
                if f.endswith('.csv'):
                    tmp = f.split('.', 1)
                    try:
                        process(tmp[0])
                    except:
                        sys.exit(1)
