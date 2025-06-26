#!/bin/sh
set -e

UID=${USER_ID:-1000}
GID=${GROUP_ID:-1000}
UNAME=${USER_NAME:-appuser}
GNAME=${GROUP_NAME:-appgroup}

echo "[entrypoint] UID=${UID} GID=${GID}"

# ----- グループ -----
if ! getent group ${GID} >/dev/null; then
    groupadd -g ${GID} ${GNAME}
fi 
GNAME=$(getent group "${GID}" | cut -d: -f1)

# ----- ユーザ -----
if ! getent passwd ${UID} >/dev/null; then
    useradd -u "${UID}" -g "${GID}" -m -s /bin/bash ${UNAME}
fi
UNAME=$(getent passwd "${UID}" | cut -d: -f1)

# ----- 権限調整 -----
mkdir -p /workspace
chown -R "${UID}:${GID}" /app /workspace

echo "[entrypoint] Exec as ${UNAME} (${UID}:${GID})"
exec gosu "${UNAME}" "$@"
