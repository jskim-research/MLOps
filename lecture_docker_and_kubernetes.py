"""Docker 명령어들

=== 이미 있는 이미지 가져와서 사용 ===
docker pull image_name (docker hub로부터 image 가져온다)
docker images (있는 이미지들 보여줌)
docker ps (실행중 컨테이너 보여줌)
docker run image_name

docker pull ubuntu:18.04
docker run -it --name demo1 ubuntu:18.04 /bin/bash  (bash terminal을 이용해 ubuntu container에 접속)

docker run -it -d --name demo2 ubuntu:18.04
docker ps
docker exec -it demo2 /bin/bash  (daemon 실행 중인 container에 접속하는 명령어)

docker run --name demo3 -d busybox sh -c "while true; do $(echo date); sleep 1; done"  (뒤 command 실행)
docker logs demo3 -f  (계속 demo3 log tracking)
docker rmi image_name (image 제거, tag가 latest가 아닐 경우 명시 필요)

=== 새 이미지 만들어서 사용 ===
Dockerfile 생성

# Dockerfile 있는 경로에서 다음 명령어 실행 (현재 폴더 . 에서 가져오겠다 이므로)
# my-image 라는 이름과 v1.0.0 이라는 태그로 이미지 빌드
docker build -t my-image:v1.0.0 .

# image build 정상적으로 됐는지 확인
docker images | grep my-image

docker run my-image:v1.0.0

=== 내 컴퓨터에서 Docker image 저장 ===
# localhost:5000 에 registry image 실행
docker run -d -p 5000:5000 --name registry registry

# registry를 바라보게 tag 한다는데 왜 이렇게 해야하는지 잘 모르겠음
docker tag my-image:v1.0.0 localhost:5000/my-image:v1.0.0

# 방금 만든 image 확인
docker images | grep my-image

# my-image => registry에 push (업로드)
docker push localhost:5000/my-image:v1.0.0

# 정상 push 확인
# localhost:5000 이라는 registry에 어떤 이미지가 저장되어 있는지 리스트 출력
curl -X GET http://localhost:5000/v2/_catalog
# my-image 라는 이미지 네임에 어떤 태크가 저장되어있는지 리스트 출력
curl -X GET http://localhost:5000/v2/my-image/tags/list

=== Docker Hub (local registry => cloud) ===
docker login  # and type username, password
docker tag <image_name>:<tag_name> <user_name>/<image_name>:<tag_name>
e.g.,) docker tag my-image:v1.0.0 vrdd21/my-image:v1.0.0
docker push vrdd21/my-image:v1.0.0  # docker hub에 push

=== 쿠버네티스 실습 (1) ===
쿠버네티스 마스터에게 요청을 보낼 때 등, data 전송 시 쓰이는 포맷으로 변환(직렬화) 필요
직렬화에 쓰이는 포맷/양식: [XML, JSON,] YAML

YAML 포맷 예시
# << 주석 처리
apiVersion: v1
kind: Pod
metadata:
    name: example  # recursive한 key-value pair
    ...

YAML 자료형
1) string
example: this is string  # 일반적인 문자열은 그냥 써도 됨
example: "this is string"  # 따옴표를 붙이나 안 붙이나 같음
example: [123], [y, yes], [:, {, }, ...]  # 숫자, YAML 예약어, 특수문자 포함 경우엔 꼭 따옴표 필요

2) integer
example: 123 or 0x1fff

3) float
example: 99.9 or 1.23e+03

4) boolean
example: true, yes, on / false, no, off

5) list
examples:
    - ex_one: 1
    - ex_two: 2
or
examples: ["1", "2", "3"]

6) multi-line strings
example: |  # 일자 작대기임, |- 이면 마지막 \n 삭제
    Hello
    Fast
    Campus
    # "Hello\nFast\nCampus\n" 으로 처리 (빈 줄 => \n 처리)
example: >
    Hello
    Fast
    Campus
    # "Hello Fast Campus\n" 으로 처리 (맨 마지막에 \n 붙임), >- 이면 마지막 \n 삭제

7) multi-document yaml
apiVersion: v1
kind: Pod
---
apiVersion: v1
kind: Service
---
apiVersion: v1
kind: Deployment
# 3개의 yaml document로 인식

=== 쿠버네티스 실습 2 ===
minikube 설치
(https://minikube.sigs.k8s.io/docs/start/ 확인)

kubectl 설치
(https://kubernetes.io/ko/docs/tasks/tools/install-kubectl-linux)

minikube start --driver=docker  # 필요한 docker image들 다운, 서버 시작
minikube status

정상출력:
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

kubectl get pod -n kube-system  # minikube 내부 default pod 들이 정상적으로 생성됐는지 확인, 모두 Running 이어야함
minikube delete  # 간단한 삭제

kubectl apply -f <yaml-file-path> # <yaml-file-path>에 해당하는 kubernetes resource를 생성 또는 변경 가능
=> kubernetes resource의 desired state를 기록해놓기 위해 항상 YAML 파일을 저장하고, 버전 관리하는 것 권장

kubectl get pod # 현재 namespace에 속하는 pod의 desired state가 아닌 current state 출력 (RUNNING 까지 조금 시간이 걸린다)
kubectl config view --minify | grep namespace: # current namespace 확인 가능
kubectl get pod -n kube-system # kube-system namespace의 pod 조회
kubectl get pod -A # 모든 namespace pod 조회
kubectl get pod <pod-name> # pod 하나 조회
kubectl describe pod <pod-name> # 좀 더 자세히 조회
kubectl get pod -o wide  # 간단한데 조금 더 많이 조회
kubectl get pod -o yaml # 입력한 것과 비슷하게 yaml 형태로 출력
kubectl get pod -w # kubectl get pod 결과를 계속 보여주는데 변화가 있을 때마다 업데이트
kubectl logs <pod-name> # counter인 경우 1초마다 log
kubectl logs <pod-name> -f # 계속 보여줌
kubectl logs <pod-name> -c <container-name> -f # 특정 컨테이너만 log 보기
kubectl exec -it <pod-name> -- <명령어>
kubectl delete pod <pod-name>
kubectl delete -f <YAML-file-path> # 사용한 YAML 파일을 사용해서 삭제

# deployment 실습
kubectl apply -f deployment.yaml
kubectl get deployment,pod
kubectl delete pod <pod-name> # 기존 pod 삭제 후 deployment에서 auto-healing
kubectl scale deployment/nginx-deployment --replicas=5 # deployment scaling
kubectl delete deployment <deployment-name>
or kubectl delete -f deployment.yaml

# service 실습
kubectl apply -f deployment.yaml # deployment => pods 생성
kubectl get pod -o wide # pod ip 확인 => 클러스터 외부에서 접근할 수 있는 IP는 아니고 내부에서 가능한 것
minikube ssh # 클러스터 내부로 접속
curl -X GET <POD-IP> -vvv # 통신 가능, HTML return
ping <POD-IP> # 통신 가능
logout # 클러스터 logout
kubectl apply -f service.yaml
kubectl get service # PORT 80:<할당받은 PORT> 숫자 확인
minikube ip
curl -X GET $(minikube ip):<할당받은 PORT> # 클러스터 외부에서도 접속 가능 => mac docker desktop으론 불가능

# PVC 실습
# storageclass는 minikube 설치 시 같이 설치됨
# PVC를 생성하면 PVC 스펙에 맞는 PV를 즉시 자동 생성한 뒤 PVC와 매칭 (즉, 관리자가 PV를 생성해줄 필요 없음)
kubectl get storageclass
kubectl apply -f pvc.yaml
kubectl get pvc,pv # pvc, pv 동시 생성
kubectl apply -f pod-pvc.yaml
kubectl get pod
kubectl exec -it mypod -- bash # pvc mount한 pod에 접속
touch hi-fast-campus
cd /var/www/html
touch hi-fast-campus
exit
kubectl delete pod mypod # volume과 mount했던 pod 삭제
kubectl get pvc,pv # pvc, pv 남아있는지 확인
kubectl apply -f pod-pvc.yaml # 다시 pod 생성
kubectl exec -it mypod -- bash # 다시 접속 후 이전 생성 파일 확인
ls # mount 하지 않은 곳의 파일은 제거됨
cd /var/www/html
ls # /var/www/html에 생성한 파일은 남아있음 (pod가 죽었다 살아나도)

"""

