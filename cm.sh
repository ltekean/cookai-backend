#!/bin/bash

# 첫 번째 인자로 커밋 메시지를 전달받음
INPUT_COMMIT_MESSAGE=$1

# 변경된 파일 목록을 가져오기
CHANGED_FILES=""
for file in $(git status --porcelain | sed 's/^.. //'); do
  CHANGED_FILES="$CHANGED_FILES $file"
done

# 커밋 메시지가 전달되었는지 확인
if [ -z "$INPUT_COMMIT_MESSAGE" ]; then
  # 인자가 없으면 기본 커밋 메시지 사용
  COMMIT_MESSAGE="test: Test Github Action CICD

Files:
$CHANGED_FILES"
else
  # 인자가 있으면 해당 메시지를 커밋 메시지로 사용
  COMMIT_MESSAGE="$INPUT_COMMIT_MESSAGE"
fi

# 변경된 파일을 스테이징
git add $CHANGED_FILES

# 커밋 실행
git commit -m "$COMMIT_MESSAGE"

# 푸시 실행
git push
