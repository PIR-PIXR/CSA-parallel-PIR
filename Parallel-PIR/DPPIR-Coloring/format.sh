#!/bin/bash
# Formats source files according to Google's style guide. Requires clang-format.

# Only files with these extensions will be formatted by clang-format.
CLANG_FORMAT_EXTENSIONS="cc|h|proto|inc"

# Display clang-format version.
clang-format --version

# Run clang-format.
find . -not -path "./third_party/**" \
       -not -path "./.git/**" \
       -not -path "./experiments/**" \
  | egrep "\.(${CLANG_FORMAT_EXTENSIONS})\$" \
  | xargs clang-format --verbose -style=google -i
