#!/bin/zsh
pytest
allure generate ./report/allure-results -o ./report/allure-report --clean
allure open ./report/allure-report