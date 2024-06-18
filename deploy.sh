#!/bin/bash
# --------------------------------------------------------
#
# [Lamba Function Deployment Script]
#
# - This script is used to deploy the lambda function.
#   It will create a zip file and update the lambda function.
#
# [Since]
# - 2024/06/18
#
# --------------------------------------------------------

# Constants
readonly COMPACT_DIR="package"
readonly TARGET_PY_NAME="lambda_function.py"
readonly FUNCTION_NAME="py-lambda-money-management-app-east"
readonly ENV_NAME=".env"
readonly REQUIRE_NAME="requirement.txt"
readonly ZIP_FILE="lambda_function.zip"

# Functions
pre_exec_deployment() {
    mkdir -p "${COMPACT_DIR}"
    pip install -r "${REQUIRE_NAME}" -t ./${COMPACT_DIR}
    cp "${TARGET_PY_NAME}" ${COMPACT_DIR}/
    cp "${ENV_NAME}" ${COMPACT_DIR}/
    cd ${COMPACT_DIR}
    zip -r ../${ZIP_FILE} .
    cd ..
}

exec_deployment() {
    aws lambda update-function-code --function-name "${FUNCTION_NAME}" --zip-file fileb://${ZIP_FILE}
}

main () {
  pre_exec_deployment
  exec_deployment
}

main "$@"
exit $?
