# Copyright 2018 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import select
import ssl
from io import StringIO
from urllib.parse import urlencode, urlparse, urlunparse

import certifi
from websocket import ABNF, WebSocket, enableTrace

STDIN_CHANNEL = 0
STDOUT_CHANNEL = 1
STDERR_CHANNEL = 2
ERROR_CHANNEL = 3
RESIZE_CHANNEL = 4


class WSClient:
    def __init__(self, configuration, url, headers, capture_all):
        """A websocket client with support for channels.

            Exec command uses different channels for different streams. for
        example, 0 is stdin, 1 is stdout and 2 is stderr. Some other API calls
        like port forwarding can forward different pods' streams to different
        channels.
        """
        self._connected = False
        self._channels = {}
        self._all = StringIO()
        self.sock = create_websocket(configuration, url, headers)
        self._connected = True
        self._returncode = None

    def read_all(self):
        """Return buffered data received on stdout and stderr channels.
        This is useful for non-interactive call where a set of command passed
        to the API call and their result is needed after the call is concluded.
        Should be called after run_forever() or update()

        TODO: Maybe we can process this and return a more meaningful map with
        channels mapped for each input.
        """
        out = self._all.getvalue()
        self._all = self._all.__class__()
        self._channels = {}
        return out

    def is_open(self):
        """True if the connection is still alive."""
        return self._connected

    def update(self, timeout=0):
        """Update channel buffers with at most one complete frame of input."""
        if not self.is_open():
            return
        if not self.sock.connected:
            self._connected = False
            return

        if hasattr(select, "poll"):
            poll = select.poll()
            poll.register(self.sock.sock, select.POLLIN)
            if timeout is not None:
                timeout *= 1_000  # poll method uses milliseconds as the time unit
            r = poll.poll(timeout)
            poll.unregister(self.sock.sock)
        else:
            r, _, _ = select.select((self.sock.sock,), (), (), timeout)

        if r:
            op_code, frame = self.sock.recv_data_frame(True)
            if op_code == ABNF.OPCODE_CLOSE:
                self._connected = False
                return
            elif op_code == ABNF.OPCODE_BINARY or op_code == ABNF.OPCODE_TEXT:
                data = frame.data.decode("utf-8", "replace")
                if len(data) > 1:
                    channel = ord(data[0])
                    data = data[1:]
                    if data:
                        if channel in [STDOUT_CHANNEL, STDERR_CHANNEL]:
                            # keeping all messages in the order they received
                            # for non-blocking call.
                            self._all.write(data)
                        if channel not in self._channels:
                            self._channels[channel] = data
                        else:
                            self._channels[channel] += data

    def run_forever(self):
        """Wait till connection is closed or timeout reached. Buffer any input
        received during this time."""
        while self.is_open():
            self.update(timeout=0)


WSResponse = collections.namedtuple("WSResponse", ["data"])


def get_websocket_url(url, query_params=None):
    parsed_url = urlparse(url)
    parts = list(parsed_url)
    if parsed_url.scheme == "http":
        parts[0] = "ws"
    elif parsed_url.scheme == "https":
        parts[0] = "wss"
    if query_params:
        query = []
        for key, value in query_params:
            if key == "command" and isinstance(value, list):
                for command in value:
                    query.append((key, command))
            else:
                query.append((key, value))
        if query:
            parts[4] = urlencode(query)
    return urlunparse(parts)


def create_websocket(configuration, url, headers=None):
    enableTrace(False)

    # We just need to pass the Authorization, ignore all the other
    # http headers we get from the generated code
    header = []
    if headers and "authorization" in headers:
        header.append("authorization: %s" % headers["authorization"])
    if headers and "sec-websocket-protocol" in headers:
        header.append("sec-websocket-protocol: %s" % headers["sec-websocket-protocol"])
    else:
        header.append("sec-websocket-protocol: v4.channel.k8s.io")

    if url.startswith("wss://") and configuration.verify_ssl:
        ssl_opts = {
            "cert_reqs": ssl.CERT_REQUIRED,
            "ca_certs": configuration.ssl_ca_cert or certifi.where(),
        }
        if configuration.assert_hostname is not None:
            ssl_opts["check_hostname"] = configuration.assert_hostname
    else:
        ssl_opts = {"cert_reqs": ssl.CERT_NONE}

    if configuration.cert_file:
        ssl_opts["certfile"] = configuration.cert_file
    if configuration.key_file:
        ssl_opts["keyfile"] = configuration.key_file

    websocket = WebSocket(sslopt=ssl_opts, skip_utf8_validation=False)
    connect_opt = {"header": header}
    websocket.connect(url, **connect_opt)
    return websocket


def websocket_call(configuration, _method, url, **kwargs):
    """An internal function to be called in api-client when a websocket
    connection is required. method, url, and kwargs are the parameters of
    apiClient.request method."""

    url = get_websocket_url(url, kwargs.get("query_params"))
    headers = kwargs.get("headers")
    return WSClient(configuration, url, headers, capture_all=True)
