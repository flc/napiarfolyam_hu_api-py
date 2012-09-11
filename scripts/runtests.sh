#!/bin/bash

mkdir -p reports/jenkins
nosetests -v \
    --with-coverage3 \
    --cover3-package=peek \
    --cover3-erase \
    --cover3-html --cover3-html-dir=./reports/coverage-html \
    --cover3-xml --cover3-xml-file=./reports/jenkins/coverage.xml \
    --cover3-tests \
    --with-xunit --xunit-file=./reports/jenkins/TEST-nosetests.xml \
    --exclude-dir-file=./scripts/nose-excludes.txt \
    $*
