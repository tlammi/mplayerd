#!/bin/bash

set -e

THISDIR="$(dirname $(realpath ${BASH_SOURCE}))"
cd "${THISDIR}"

CONFDIR=~/.config/systemd/user
WORKDIR=~/mplayerd
mkdir -p $CONFDIR
mkdir -p $WORKDIR
cp mplayerd.service $CONFDIR

pip install --user .
systemctl --user enable mplayerd
