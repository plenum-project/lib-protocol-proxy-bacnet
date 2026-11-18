"""Static routes (the plenum-project change): where the routes file is found, and what is entered into
bacpypes3's routing cache for each route."""
import asyncio
import json
from types import SimpleNamespace

from bacpypes3.netservice import RouterEntryStatus
from bacpypes3.pdu import Address

from protocol_proxy.protocol.bacnet.bacnet import BACnet


def test_routes_come_from_the_named_file_then_the_environment_then_volttron_home(tmp_path, monkeypatch):
    named, by_env, home = tmp_path / 'named.json', tmp_path / 'env.json', tmp_path / 'home'
    home.mkdir()
    named.write_text(json.dumps({'1010': '10.0.0.41'}))
    by_env.write_text(json.dumps({'2020': '10.0.0.42:47809'}))
    (home / 'bacnet-routes.json').write_text(json.dumps({'3030': '10.0.0.43'}))
    monkeypatch.delenv('BACNET_PROXY_STATIC_ROUTES', raising=False)
    monkeypatch.delenv('VOLTTRON_HOME', raising=False)

    assert BACnet.load_static_routes() == {}                       # no file anywhere: no routes, as upstream
    assert BACnet.load_static_routes(str(tmp_path / 'missing.json')) == {}
    monkeypatch.setenv('VOLTTRON_HOME', str(home))
    assert BACnet.load_static_routes() == {3030: '10.0.0.43'}
    monkeypatch.setenv('BACNET_PROXY_STATIC_ROUTES', str(by_env))
    assert BACnet.load_static_routes() == {2020: '10.0.0.42:47809'}
    assert BACnet.load_static_routes(str(named)) == {1010: '10.0.0.41'}    # network numbers become ints


class _Cache:
    """What install_static_routes uses of bacpypes3's RouterInfoCache."""

    def __init__(self):
        self.paths, self.dnets = {}, {}

    async def set_path_info(self, snet, dnet, address, status):
        self.paths[(snet, dnet)] = (address, status)

    async def get_router_dnets(self, snet, address):
        return self.dnets.get((snet, address))

    async def set_router_dnets(self, snet, address, dnets):
        self.dnets[(snet, address)] = set(dnets)


def test_a_route_enters_the_path_and_the_routers_own_networks():
    """post1 entered only the path. The request went out, and the routed reply was dropped because the
    router had no networks on record, so every read timed out. Both are needed."""
    cache = _Cache()
    proxy = SimpleNamespace(app=SimpleNamespace(nsap=SimpleNamespace(router_info_cache=cache)),
                            static_routes={1010: '10.0.0.41', 1011: '10.0.0.41', 2020: '10.0.0.42'})
    asyncio.run(BACnet.install_static_routes(proxy))

    a, b = Address('10.0.0.41'), Address('10.0.0.42')
    for snet in (None, 0):
        assert cache.paths[(snet, 1010)] == (a, RouterEntryStatus.available)
        assert cache.paths[(snet, 2020)] == (b, RouterEntryStatus.available)
        assert cache.dnets[(snet, a)] == {1010, 1011}              # two networks behind one router
        assert cache.dnets[(snet, b)] == {2020}
