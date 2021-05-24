import ipaddress
import netifaces
import re
import subprocess
import typing
import zlib


class NetworkInfo:

    _LINE_RE = re.compile(r"(?P<iface>[\w|-]+)\s+(?P<destination>\w+)\s+(?P<gateway>\w+)\s+(?P<flags>\w+)\s+(?P<refcnt>\w+)\s+(?P<use>\w+)\s+(?P<metric>\w+)\s+(?P<mask>\w+).+")

    _INSTANCE = None

    def __init__(self, data: str, checksum: int):
        self._data = data
        self._checksum = checksum

    def parse(self):
        try:
            default_routes = self._parse_default_routes()
            default_route = self._find_default_route(default_routes)
            self._default_interface = default_route.group("iface")
            self._default_ip = self._get_iface_address(iface=default_route.group("iface"))
            if self.is_wireless:
                self._ssid = self._get_ssid()
            self._is_connected = True
        except Exception:
            self._is_connected = False

    @classmethod
    def update(cls):
        with open("/proc/net/route", "rb") as route_file:
            contents = route_file.read()
        checksum = zlib.crc32(contents)
        if cls._INSTANCE and cls._INSTANCE.checksum == checksum:
            return cls._INSTANCE
        cls._INSTANCE = cls(data=contents.decode("utf-8"), checksum=checksum)
        cls._INSTANCE.parse()
        return cls._INSTANCE

    def _parse_default_routes(self) -> typing.List[re.Match]:
        default_routes = list()
        for line in self._data.split("\n")[1:-1]:
            line_p = self._LINE_RE.match(line)
            if line_p.group("destination") == "00000000" and line_p.group("mask") == "00000000":
                default_routes.append(line_p)
        return default_routes

    def _find_default_route(self, default_routes: typing.List[re.Match]) -> re.Match:
        default_routes.sort(key=lambda r: r.group("metric"))
        return default_routes[0]

    def _get_iface_address(self, iface: str) -> str:
        addresses = netifaces.ifaddresses(iface)
        address = addresses.get(netifaces.AF_INET)[0].get("addr")
        netmask = addresses.get(netifaces.AF_INET)[0].get("netmask")
        ip_with_cidr = ipaddress.IPv4Interface(f"{address}/{netmask}").compressed
        return ip_with_cidr

    def _get_ssid(self) -> str:
        return subprocess.check_output(["iwgetid", "-r"], encoding="utf-8")[:-1]

    @property
    def default_interface(self) -> str:
        return self._default_interface

    @property
    def default_ip(self) -> str:
        return self._default_ip

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def is_wireless(self) -> bool:
        return self._default_interface.startswith("wlan")

    @property
    def ssid(self) -> str:
        return self._ssid

    @property
    def checksum(self) -> int:
        return self._checksum

    @property
    def summary(self) -> str:
        if not self._is_connected:
            return "disconnected"
        if self.is_wireless:
            return f"wireless {self.default_interface} ({self.default_ip} {self.ssid})"
        else:
            return f"wired {self.default_interface} ({self.default_ip})"


def main():
    routing_table = NetworkInfo.update()
    print(routing_table.summary)


if __name__ == "__main__":
    main()
