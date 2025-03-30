#!/bin/bash
set -e

on_error() {
  echo "에러 발생"
  echo "실패한 명령어: '$BASH_COMMAND'"
  echo "시간: $(date)"
  echo "스크립트 중단됨. 확인 후 재시도 할 것"
  exit 1
}

# 에러 발생 시 on_error 함수 호출하도록 설정
trap 'on_error' ERR

echo "### Fetching upstream..."
git fetch upstream

echo "### Checking out main branch..."
git checkout main

echo "### Merging upstream/main into local main..."
git merge upstream/main --no-edit

echo "### Pushing to origin..."
git push origin main

echo "### Sync complete!"
