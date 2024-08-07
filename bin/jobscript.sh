#!/bin/bash
#PBS -j oe
#PBS -q huge
#PBS -l select=1:ncpus=16:mem=32gb

echo "Using python:" $(which python)
echo "Using PATH:" $PATH

set -x

{exec_job}
