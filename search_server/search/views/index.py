"""
ask485 index (main) view.

URLs include:
/
"""
import heapq
import threading
import time
import itertools
import search
import requests
import flask


@search.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    # Connect to database
    connection = search.model.get_db()
    # query = ""
    # weight = 0.5
    query = flask.request.args.get('q', default="", type=str)
    weight = flask.request.args.get('w', default=0.5, type=float)
    context = {}
    context['text'] = query
    print(query)
    context['weight'] = weight
    if not query:
        return flask.render_template("index.html", **context)
    # if the query is not empty
    num_thread = len(search.app.config['SEARCH_INDEX_SEGMENT_API_URLS'])
    results = [[]] * num_thread
    threads = []
    for idx in range(num_thread):
        url = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS'][idx]
        payload = {'q': query, 'w': weight}
        thread = threading.Thread(
            target=req_index_server, args=(idx, url, payload, results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    num_results = sum(len(r) for r in results)
    if num_results > 0:
        merged_result = heapq.merge(
            *results, key=lambda x: x['score'], reverse=True)
        result_list = []
        first_results = itertools.islice(merged_result, min(num_results, 10))
        result_list = list(map(lambda x: fetch_doc_from_id(
            connection=connection,
            docid=x['docid']),
            first_results))
        context['results'] = result_list
        # print("context['results']")
        # print(context['results'])
    else:
        # no index result found for this query
        pass
    return flask.render_template("index.html", **context)


def req_index_server(tid, url, payload, results):
    """Thread to send GET requests to index server."""
    # try:
    resp = requests.get(url, params=payload, timeout=10)
    # except Exception as e:
    #     print("######### Error!")
    #     print(e)
    #     exit(-1)
    results[tid] = resp.json()['hits']
    print(f"thread-{tid} done: {len(results[tid])}")
    time.sleep(0.1)


def fetch_doc_from_id(connection, docid):
    """Fetch the document from docid."""
    doc = connection.execute(
        'SELECT * FROM Documents '
        'WHERE docid = ?',
        (docid, )
    ).fetchone()
    return doc
