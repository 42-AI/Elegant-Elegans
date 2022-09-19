#!/bin/bash

abs_path=${PWD}
echo $abs_path
for dir in experiments/activity_index/*     # list img directories
    dir=${abs_path}'/'${dir%*/}      # remove the trailing "/"
    echo "${dir} audit done."    # print everything after the final "/"
    python3 -m auditor --path=${dir}
done
