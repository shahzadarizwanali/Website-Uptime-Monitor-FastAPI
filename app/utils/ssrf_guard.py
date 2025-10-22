import socket
import ipaddress
import asyncio


async def host_is_private(host: str) -> bool:
    loop = asyncio.get_running_loop()
    try:
        infos = await loop.run_in_executor(None, socket.getaddrinfo, host, None)
        # print("Resolved addresses for", host, ":", [i[4][0] for i in infos])
    except socket.gaierror:
        # print("DNS resolution failed for", host)
        return False

    for info in infos:
        ip = info[4][0]
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            # print("Blocked private/reserved IP:", ip)
            return True

    print("Public host allowed:", host)
    return False
