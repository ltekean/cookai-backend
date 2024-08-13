#!/bin/bash

# 변경된 파일 목록을 가져오기
CHANGED_FILES=""
for file in $(git status --porcelain | sed 's/^.. //'); do
  CHANGED_FILES="$CHANGED_FILES $file"
done

# 커밋 메시지를 작성하기 위해 변경된 파일을 리스트로 나열
COMMIT_MESSAGE="test: Test Github Action CICD

Files:
$CHANGED_FILES"

# 변경된 파일을 스테이징
git add $CHANGED_FILES

# 커밋 실행
git commit -m "$COMMIT_MESSAGE"

# 푸시 실행
git push
