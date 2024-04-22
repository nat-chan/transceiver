#!/bin/bash

set -euxo pipefail

python -m build
python -m twine upload  dist/*