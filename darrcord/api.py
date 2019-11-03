import requests
from darrcord import logger


def req(conn, resource, method="GET", params={}, body={}):
    try:
        if method == "GET":
            response = requests.get(
                conn.ENDPOINT + resource,
                params=params,
                headers=conn.HEADERS
            )
        elif method == "POST":
            response = requests.post(
                conn.ENDPOINT + resource,
                params=params,
                json=body,
                headers=conn.HEADERS
            )
        elif method == "PUT":
            response = requests.put(
                conn.ENDPOINT + resource,
                params=params,
                json=body,
                headers=conn.HEADERS
            )
        else:
            logger.exception(f"Invalid HTTP method: {method}.")
            raise Exception
    except Exception as ex:
        # failed to do something
        logger.exception(f"Failed to connect to API.  Check endpoint ({conn.ENDPOINT},  {resource}) or API_KEY.  Exception message: {ex}")
        raise
    except ConnectionError as err:
        logger.error(f"Failed to connect to API.  Check endpoint ({conn.ENDPOINT},  {resource}) or API_KEY.  Error message: {err}")
        raise
    if response is None or response.json() is None:
        logger.exception(f"Failed to connect to API.  Check endpoint ({conn.ENDPOINT},  {resource}) or API_KEY.")
        raise Exception
    else:
        if isinstance(response.json(), dict):
            # this sucks lol.  TODO.
            try:
                if response.json()["error"]:
                    logger.warning(f"Error message: {response.json()['error']}")
                    raise Exception
                elif response.json()["message"]:
                    logger.info(f"Message: {response.json()['message']}.  This may be an error; please investigate.")
            except KeyError:
                pass
        else:
            logger.info(f"Successfully connected to {conn.ENDPOINT + resource}!")
    return response


def req_command(conn):
    URI = "command"
    return req(conn, URI)


def req_item_lookup(conn, URI, params):
    resp = req(conn, URI,params=params)
    logger.info(f"req_item_lookup: resp = {resp}")
    if resp:
        if isinstance(resp.json(),dict):
            json = [resp.json()]
        elif isinstance(resp.json(),list):
            json = resp.json()
        else:
            json = []
        return {"code":resp.status_code, "json":json}
    return


def req_item(conn, URI, body):
    resp = req(conn, URI, method="POST", body=body)
    logger.info(resp)
    logger.info(resp.json())

    #i messed this up
    if resp:
        if isinstance(resp.json(),dict):
            json = [resp.json()]
        elif isinstance(resp.json(),list):
            json = resp.json()
        else:
            json = [{}]
        return {"code":resp.status_code, "json":json}
    try:
        if resp.json():
            if isinstance(resp.json(), dict):
                return {"code":resp.status_code, "json":[resp.json()]}
            else:
                return {"code": resp.status_code, "json": resp.json()}
        return {"code":resp.status_code, "json":None}
    except:
        return {"code": None, "json": None}
