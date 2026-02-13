#!/bin/bash
# rebuild_environment.sh - NC-RES-002 Build Recovery Script
# Purpose: Re-establish the Neural-Chromium build environment from a cold start.

echo "--- INITIATING COLD-START REBUILD [NC-RES-002] ---"

# 1. Restore Depot Tools
if [ ! -d "~/depot_tools" ]; then
    echo "Restoring Depot Tools..."
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git ~/depot_tools
    export PATH="$PATH:/home/ubuntu/depot_tools"
    echo 'export PATH="$PATH:/home/ubuntu/depot_tools"' >> ~/.bashrc
fi

# 2. Re-author .gclient file
echo "Re-authoring .gclient..."
cat <<EOF > ~/chromium/.gclient
solutions = [
  {
    "name": "src",
    "url": "https://chromium.googlesource.com/chromium/src.git",
    "managed": False,
    "custom_deps": {},
    "custom_vars": {},
  },
]
EOF

# 3. Pull the Brain (Claw Capabilities)
if [ ! -d "~/claw-capabilities" ]; then
    echo "Recovering Senti-001 Brain..."
    git clone https://github.com/mcpmessenger/claw-capabilities.git ~/claw-capabilities
    ln -s ~/claw-capabilities ~/comms
    ln -s ~/claw-capabilities/MEMORY.md ~/MEMORY.md
fi

# 4. Initiate Source Sync
echo "Initiating Chromium Source Sync (Body Recovery)..."
cd ~/chromium/src && gclient sync --force

echo "--- RECOVERY ARMED ---"
