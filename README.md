# 내 맘을 위로해조(8조)
### 프로젝트 개요

<p align="center">
  <img src="/statics/main.png" height=400>
</p>

### AI 챗봇 기반 심리 위로 서비스
산학프로젝트 과목에서 진행한 AI 융합 프로젝트입니다.<br>
사용자는 챗봇과 커뮤니티를 통해 자신의 사연을 공유하여 위로받을 수 있으며 타인의 글에 댓글과 공감 버튼으로 위로의 메시지를 전할 수 있습니다.<br>
모든 백엔드를 서버리스로 구축하였으며 AI 담당 팀원이 koBERT 모델을 이용하여 개발한 챗봇을 서빙하였습니다.
<br><br>
📚 <a href="https://baegopa.notion.site/9891e0329bcf47b8a8b5201da58202cf?pvs=4">프로젝트 상세 문서</a>

---
### 역할 (서버리스 백엔드 구축)
- AWS를 활용하여 서버리스 백엔드 구축
- 게시판 REST API 개발
- 데이터베이스 설계

---
### 트러블 슈팅
#### 1. REST API 보안 개선
  - 기존
      - 아무나 요청을 보낼 수 있어 보안에 취약
  - 개선 방안
      - api gateway에 x-api-key 추가 발급
      - 헤더에 x-api-key 를 추가해야만 REST API에 접근 가능

#### 2. 프론트엔드 연결 시 CORS 문제 해결
  - 기존
      - 프론트에서 preflight request 전송 시 해당하는 response가 없어 오류 발생
  - 해결 방안
      - aws api gateway에서 해당 request에 대해 response를 해줄 수 있는 options 메서드 설정
      - lambda function 코드 상에서도 response 할 시 ‘Access-Control-Allow-Origin’ header 추가
        
#### 3. 챗봇 REST API 요청 시 메모리 문제 해결
  - 기존
      - 파이썬 코드 실행 중 메모리 리소스가 1gb로는 부족하여 프로세스가 killed 됨
  - 해결 방안
      - 인스턴스 메모리 단계 별 업그레이드 후 테스트 진행
      - 최종 - t3.medium으로 업그레이드

#### 4. 챗봇에게 메시지 보낼 시 응답 반복 문제 해결
  - 기존
      - 챗봇 API 요청 시 동기 처리되어 가이드 문구 두 번 출력
  - 해결방안
      - async await - promise 비동기 요청
      - 추가적으로 타임아웃 설정하여 가이드 문구로 응답
        
---
### 아키텍처
<p align="center">
  <img src="/statics/architecture.png" height=500>
</p>

---
### 프로젝트 구성
- 팀 구성 : 3인 1팀 <br>
- 개발 기간 : 2022.03. ~ 2022.06.
  
---
### 기술 스택
- AWS (Amplify, EC2, Lambda function, API gateway, Cognito, S3, RDS)
- MySQL
- Python, Flask

  
