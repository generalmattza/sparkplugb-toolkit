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
<<<<<<< HEAD
PROTO_PATH="../../"
PROTO_TARGET="../../sparkplug_b/sparkplug_b.proto"
DESCRIPTOR_SET="tahu.pb"          # The name for the descriptor set output
OUTPUT_PATH="../src-micro-protobuf"                   # Where the .pb.c/.pb.h files will be generated
=======
OUTPUT_PATH="../../../protobuf-c"
PROTO_PATH="../../sparkplug_b/sparkplug_b.proto"
DESCRIPTOR_FILE="tahu.pb"          # The name for the descriptor set output
>>>>>>> 96fb48b35787d1a7227174d0f12f64a6248e87fe
OPTIONS_PATH="tahu.options"        # Nanopb options file
NANOPB_DIR="../../../nanopb"        # Path to Nanopb
NANOPB_GENERATOR_PATH="$NANOPB_DIR/generator/nanopb_generator.py"

# 3) Navigate to the core directory (where your .options file presumably is)
cd "$CORE_DIR" || exit 1

# 4) Generate a descriptor set file (.pb) from the proto
#    We use '--descriptor_set_out' so protoc produces a descriptor
#    set compatible with the Nanopb generator.
protoc --proto_path="$PROTO_PATH" \
        -o "$DESCRIPTOR_SET" \
       "$PROTO_TARGET"

# 5) Run the Nanopb Python generator to produce .c/.h from the descriptor
"$PYTHON_PATH" "$NANOPB_GENERATOR_PATH" \
        -f "$OPTIONS_PATH" \
        "$DESCRIPTOR_SET"

# 6) Move the generated files to their proper places

cd "$NANOPB_DIR" || exit 1
mv "../$CORE_DIR/sparkplug_b/"* "$OUTPUT_PATH"
cp "../$CORE_DIR/src/tahu.c" "$OUTPUT_PATH"
cp "../$CORE_DIR/src/tahu.pb.c" "$OUTPUT_PATH"
cp "../$CORE_DIR/include/tahu.h" "$OUTPUT_PATH"
cp "../$CORE_DIR/include/tahu.pb.h" "$OUTPUT_PATH"

# Copy files direct from nanopb
cp pb_common.c pb_common.h pb_decode.c pb_decode.h pb_encode.c pb_encode.h pb.h "$OUTPUT_PATH"

echo "Nanopb generation completed successfully."
