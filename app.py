# Copyright 2022 Rohit Sood

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import urllib.parse
from utility import getstaticheader, getfreshcookie, getstocklist, get_stock_data, start_collector
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.response import json as json_response
import asyncio
from sanic import Sanic

app = Sanic("Quote_Collector", configure_logging=False)
app.add_task(start_collector)


@app.route('/nse/<symbol>', methods=['GET'])
def nsedata(request: Request, symbol) -> HTTPResponse:
    symbol = str.upper(urllib.parse.unquote(symbol))
    headers = getstaticheader(urllib.parse.quote(symbol))
    cookies = getfreshcookie()
    try:
        return json_response(get_stock_data(symbol, headers, cookies))
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Next entry.")
        print()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        server = app.create_server(
            host="0.0.0.0",
            port=5000,
            debug=True,
            return_asyncio_server=True,
            asyncio_server_kwargs=None,
        )
        asyncio.ensure_future(server, loop=loop)
        loop.run_forever()
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Next entry.")
        print()


