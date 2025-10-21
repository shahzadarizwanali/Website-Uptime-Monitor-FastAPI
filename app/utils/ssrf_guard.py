import asyncio
import socket
import ipaddress


async def host_is_private(hostname: str) -> bool:

    loop = asyncio.get_running_loop()

    def _resolve():
        try:
            return socket.getaddrinfo(hostname, None)
        except Exception:
            return []

    infos = await loop.run_in_executor(None, _resolve)
    addrs = set()
    for info in infos:
        try:
            addr = info[4][0]
            addrs.add(addr)
        except Exception:
            continue
    for ip in addrs:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
                return True
        except Exception:
            continue
    return False
