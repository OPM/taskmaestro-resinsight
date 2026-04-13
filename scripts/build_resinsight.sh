#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
RESINSIGHT_SRC="${REPO_ROOT}/vendor/ResInsight"
BUILD_DIR="${RESINSIGHT_SRC}/build"

# Check submodule is initialized
if [ ! -f "${RESINSIGHT_SRC}/CMakeLists.txt" ]; then
    echo "Initializing ResInsight submodule..."
    git -C "$REPO_ROOT" submodule update --init --recursive vendor/ResInsight
fi

# Bootstrap vcpkg if needed
if [ ! -f "${RESINSIGHT_SRC}/ThirdParty/vcpkg/vcpkg" ]; then
    echo "Bootstrapping vcpkg..."
    "${RESINSIGHT_SRC}/ThirdParty/vcpkg/bootstrap-vcpkg.sh"
fi

# Prefer a virtual environment python with pip available
if [ -n "${RESINSIGHT_GRPC_PYTHON_EXECUTABLE:-}" ]; then
    PYTHON_EXE="$RESINSIGHT_GRPC_PYTHON_EXECUTABLE"
elif [ -n "${VIRTUAL_ENV:-}" ]; then
    PYTHON_EXE="${VIRTUAL_ENV}/bin/python"
else
    PYTHON_EXE="$(which python3)"
fi

echo "Configuring ResInsight with Ninja..."
cmake -G Ninja -S "$RESINSIGHT_SRC" -B "$BUILD_DIR" \
    -DCMAKE_BUILD_TYPE=Release \
    -DRESINSIGHT_ENABLE_GRPC=ON \
    -DRESINSIGHT_GRPC_PYTHON_EXECUTABLE="$PYTHON_EXE" \
    -DRESINSIGHT_GRPC_DOWNLOAD_PYTHON_MODULE=true \
    -DRESINSIGHT_ENABLE_HDF5=false \
    -DCMAKE_TOOLCHAIN_FILE="${RESINSIGHT_SRC}/ThirdParty/vcpkg/scripts/buildsystems/vcpkg.cmake"

echo "Building ResInsight..."
ninja -C "$BUILD_DIR"

echo "Build complete. Binary at: ${BUILD_DIR}/ResInsight"
