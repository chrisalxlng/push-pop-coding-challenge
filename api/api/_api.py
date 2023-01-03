"""Module to setup fastapi API to expose API to the outside world."""
import logging
import random
from typing import Any, Dict

from fastapi import FastAPI
import uvicorn

ERROR_CODES = [error_code for error_code in range(50)]
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
LOGGER = logging.getLogger("API")

# globals
request_count = 0
requests = []

app = FastAPI()

def _generate_lists() -> Dict[str, Any]:
    """Generate resolved, unresolved and backlog lists."""
    return {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occured, that is `resolved`'
        } for error_idx in range(50)],
        'unresolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error DEF occured, that is `unresolved`'
        } for error_idx in range(50, 100)],
        'backlog': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error XYZ occured, that is in the `backlog`'
        } for error_idx in range(100, 150)]
    }


@app.get("/get_lists")
def get_lists(operator_name: str) -> Dict[str, Any]:
    """Return resolved, unresolved and backlog lists."""
    LOGGER.info('Generating resolved, unresolved and backlog lists.')
    global request_count, requests

    request_count += 1
    if (request_count == 1):
        LOGGER.info('%d error request received.' % request_count)
    else:
        LOGGER.info('%d error requests received.' % request_count)
    
    operator_names = [operator['operator_name'] for operator in requests]
    if (operator_name in operator_names):
        index = operator_names.index(operator_name)
        requests[index] = { 'operator_name': operator_name, 'request_count': requests[index]['request_count'] + 1 }
    else:
        requests.append({ 'operator_name': operator_name, 'request_count': 1 })
    for request in requests:
        name, count = request['operator_name'], request['request_count']
        if (count == 1):
            LOGGER.info('%s has requested errors %d time.', name, count)
        else:
            LOGGER.info('%s has requested errors %d times.', name, count)

    return _generate_lists()


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    """Return the error intersection counts between a set of resolved, unresolved and backlog lists."""
    LOGGER.info('Generating the intersection counts between a set of resolved, unresolved and backlog lists.')

    error_lists = _generate_lists()
    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

    resolved_codes = [error['code'] for error in resolved]
    unresolved_codes = [error['code'] for error in unresolved]
    backlog_codes = [error['code'] for error in backlog]

    # See https://stackoverflow.com/a/3697438
    resolved_unresolved_intersection = len(list(set(resolved_codes) & set(unresolved_codes)))
    resolved_backlog_intersection = len(list(set(resolved_codes) & set(backlog_codes)))
    unresolved_backlog_intersection = len(list(set(unresolved_codes) & set(backlog_codes)))

    return  {
        'resolved_unresolved': resolved_unresolved_intersection,
        'resolved_backlog': resolved_backlog_intersection,
        'unresolved_backlog': unresolved_backlog_intersection
    }

def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)
