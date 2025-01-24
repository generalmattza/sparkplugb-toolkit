#!/bin/bash

# ---------------------------------------------------------------------------
# This script compiles the .proto files in the current directory into C files
# using protoc and then uses nanopb's generator to create .c and .h files.
# ---------------------------------------------------------------------------

# 1) Check if protoc is installed
if ! [ -x "$(command -v protoc)" ]; then
  echo 'Error: protoc is not installed.' >&2
  exit 1
fi

# 2) Set up your variables
PYTHON_PATH="../../../.venv/bin/python"   # Path to your Python executable
CORE_DIR="./tahu/c/core"
OUTPUT_PATH="../../../protobuf-micro"
PROTO_PATH="../../sparkplug_b/sparkplug_b.proto"
DESCRIPTOR_FILE="tahu.pb"          # The name for the descriptor set output
OPTIONS_PATH="tahu.options"        # Nanopb options file
NANOPB_GENERATOR_PATH="../../../nanopb/generator/nanopb_generator.py"

# 3) Navigate to the core directory (where your .options file presumably is)
cd "$CORE_DIR" || exit 1

# 4) Generate a descriptor set file (.pb) from the proto
#    We use '--descriptor_set_out' so protoc produces a descriptor
#    set compatible with the Nanopb generator.
protoc --proto_path="$OUTPUT_PATH" \
       --descriptor_set_out="$DESCRIPTOR_FILE" \
       "$PROTO_PATH"

# 5) Run the Nanopb Python generator to produce .c/.h from the descriptor
"$PYTHON_PATH" "$NANOPB_GENERATOR_PATH" \
        -f "$OPTIONS_PATH" \
        "$DESCRIPTOR_FILE"

# 6) Move the generated files to their proper places
mv tahu.pb       src/
mv tahu.pb.c     src/
mv tahu.pb.h     include/

echo "Nanopb generation completed successfully."
