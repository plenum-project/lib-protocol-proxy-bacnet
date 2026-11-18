> **This is the plenum-project build of `protocol-proxy-bacnet`.** It is the
> upstream library ([eclipse-volttron/lib-protocol-proxy-bacnet](https://github.com/eclipse-volttron/lib-protocol-proxy-bacnet))
> at `2.0.0rc4` plus one change: **static routes**, so a VOLTTRON node can read
> BACnet devices behind a router that is on another subnet (most MS/TP trunks).
> Everything else is upstream's, unchanged.
>
> - The change is on the branch `plenum-static-routes`. `main` and `develop` are upstream's.
> - Install the tag, in the node's venv, after the platform's first start:
>   `pip install --force-reinstall --no-deps "git+https://github.com/plenum-project/lib-protocol-proxy-bacnet@plenum-2.0.0rc4.post2"`
> - Use `post2` or later. `post1` sends the request but drops the routed reply, so every read of a routed device times out.
> - How it is used, and the routes file Plenum writes: the [Plenum runbook](https://github.com/plenum-project/plenum/blob/main/docs/runbook.md), section 8.5.
> - The same change as a patch against the stock package: `contrib/lib-protocol-proxy-bacnet` in the Plenum repository.
>
> ## Static routes
>
> The stock proxy finds routers by a local broadcast (Who-Is-Router-To-Network),
> which never leaves the node's subnet. With a routes file, the proxy tells
> bacpypes3 at start which router reaches each BACnet network, and requests to
> `<network>:<mac>` are sent to that router directly.
>
> The file is JSON, network number to router address: `{"1010": "10.0.0.41"}`.
> It is read from `--static-routes-file`, else the file named by
> `BACNET_PROXY_STATIC_ROUTES`, else `$VOLTTRON_HOME/bacnet-routes.json`.
> No file: no routes, and the proxy behaves as upstream's.

# Protocol Proxy BACnet Library
![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
[![Passing?](https://github.com/eclipse-volttron/lib-protocol-proxy-bacnet/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/lib-protocol-proxy-bacnet/actions/workflows/run-tests.yml)
[![pypi version](https://img.shields.io/pypi/v/protocol-proxy-bacnet.svg)](https://pypi.org/project/protocol-proxy-bacnet/)

This library provides support for communication and management of BACnet devices to a [Protocol Proxy](https://github.com/eclipse-volttron/lib-protocol-proxy) Manager.
Communication with a BACnet device on a network happens via a virtual BACnet device.

## Automatically installed dependencies
- python = ">=3.10,<4.0"
- protocol-proxy = ">=2.0.0rc0"
- bacpypes3 = ">=0.0.102"


[//]: # (# Documentation)

[//]: # (More detailed documentation can be found on [ReadTheDocs]&#40;https://eclipse-volttron.readthedocs.io/en/latest/external-docs/lib-protocol-proxy-bacnet/index.html. The RST source)

[//]: # (of the documentation for this component is located in the "docs" directory of this repository.)

# Installation
This library, along with its dependencies, can be installed using pip:

```shell
pip install lib-protocol-proxy-bacnet
```

# Development
This library is maintained by the VOLTTRON Development Team.

Please see the following [guidelines](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md)
for contributing to this and/or other VOLTTRON repositories.

[//]: # (Please see the following helpful guide about [using the Protocol Proxy]&#40;https://github.com/eclipse-volttron/lib-protocol-proxy/blob/develop/developing_with_protocol_proxy.md&#41;)

[//]: # (in your VOLTTRON agent or other applications.)

# Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.
