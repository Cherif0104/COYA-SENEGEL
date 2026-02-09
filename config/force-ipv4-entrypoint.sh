#!/bin/bash
# Force la résolution du hostname DB en IPv4 (contourne "Network unreachable" IPv6 vers Supabase).
set -e
if [ -n "$HOST" ]; then
  IPV4=$(python3 -c "
import socket
try:
    infos = socket.getaddrinfo('$HOST', None, socket.AF_INET)
    if infos:
        print(infos[0][4][0])
except Exception:
    pass
" 2>/dev/null)
  if [ -n "$IPV4" ]; then
    export HOST="$IPV4"
  fi
fi
exec /entrypoint.sh "$@"
