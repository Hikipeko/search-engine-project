"""
ask485 index (main) view.
URLs include:
/
"""
from datetime import datetime
import flask
import search
import requests
import heapq
import threading
import time
import itertools

@search.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    # Connect to database
    connection = search.model.get_db()
    query = ""
    weight = 0.5
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w')
    num_thread = len(search.config.SEARCH_INDEX_SEGMENT_API_URLS)
    results = [[]] * num_thread
    threads = []

    for idx in range(num_thread):
        url = search.config.SEARCH_INDEX_SEGMENT_API_URLS[idx]
        payload = {'q': query, 'w': weight}
        thread = threading.Thread(target=reqIndexServer, args=(idx, url, payload, results))
        threads.append(thread)
        thread.start()
    # for url in search.config.SEARCH_INDEX_SEGMENT_API_URLS:
    #     payload = {'q': quest, 'w': weight}
    #     thread = threading.Thread(target=reqIndexServer, args=(url,payload,results,))
    #     threads.append(thread)
    #     thread.start()
        # print(resp.json)
        # heapq.merge(results,resp.json)
        
    for thread in threads:
        thread.join()
    context = {}
    num_results = sum([len(r) for r in results])
    if num_results > 0:
        merged_result = heapq.merge(*results, key = lambda x: x['score'], reverse=True)
        result_list = []
        first_results = itertools.islice(merged_result, min(num_results, 10))
        result_list = list(map(lambda x: fetchDocFromId(connection=connection, docid=x['docid']), first_results))
        context['results'] = result_list
        # print("context['results']")
        # print(context['results'])
    else:
        # no index result found for this query
        pass 
    context['text'] = query
    # print(context['text'])
    context['weight'] = weight
    return flask.render_template("index.html", **context)


def reqIndexServer(tid, url, payload, results):
    try:
        resp = requests.get(url, params=payload)
    except Exception as e:
        print("######### Error!")
        print(e)
        exit(-1)
    results[tid] = resp.json()['hits']
    print(f"thread-{tid} done: {len(results[tid])}")
    time.sleep(0.1)

def fetchDocFromId(connection, docid):
    doc = connection.execute(
    'SELECT * FROM Documents '
    'WHERE docid = ?',
    (docid, )
    ).fetchone()
    return doc