# Fastapi-template

## app includes
#### User model and basic user routes
#### Simple auth implementation and etc.


## Virtual environment
dependency separated to 3 group
main - all what need to application works
dev  - main deps + development libraries (black, isort, etc. )
test - main deps + testing libraries

activate poetry
```shell
poetry shell
```
install only main deps
```shell
poetry install
```

Install all dependencies.
```shell
poetry install --with dev,test
```

Add new deps to dev or test dependency.
```shell
poetry add <new_lib> --group=dev
```

### Pre-commit hooks
It should be work in active environment
```shell
pre-commit install
```
in first commit it require more time for install hooks dependencies.




## Migrations
generate migrations

```shell
alembic revision --autogenerate -m "init"
```

apply migrations
```shell
alembic upgrade head
```
**Note:**
out scope of docker need redefine db url
```shell
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
```


## Start apps
in docker
```shell
docker-compose up -d
```

Maybe requires
```shell
export PYTHONPATH=src
```

### start fastapi server
```shell
uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```
### start dramatiq worker
```shell
dramatiq src.worker -p 4
```


### App structures
/auth - authentication and authorization module
   from auth.depednecoes
   Use AuthDependency - for check authorization info
   Use validate_permissions - for check user permission

/user - user model and routes
/worker - dramatiq worker, implement task here.

about all routes can get info from

http://127.0.0.1:8000/docs


## Curl examples
```shell
curl -X POST "http://127.0.0.1:8000/users" \
-H "Content-Type: application/json" \
-d '{
  "email": "mail@example.com",
  "password": "12345"
}'
```

```shell
curl -X POST "http://127.0.0.1:8000/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "mail@example.com",
  "password": "12345"
}'
```

```shell
curl -X POST "http://127.0.0.1:8000/auth/refresh" \
-H "Content-Type: application/json" \
-d '{"token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3JvbGUiOiJ1c2VyIiwidXNlcl9wayI6MSwic3ViIjoibWFpbEBleGFtcGxlLmNvbSIsImp0aSI6IjZjMDAwMzkxLTY0YTYtNDE0MS1iY2Q2LWNhZWU1YzliMDA0YyIsImlhdCI6MTcxMjAzOTQxOCwiZXhwIjoxNzEyMTI1ODE4LCJ0eXBlIjoicmVmcmVzaCJ9.FXqr2SK0E4bjLfr7qGzd1R7oO8Bp8Gak-mAFHDlR-kPZh97xuLX7Hc7raLVFQkf4-Y9EJE0TFcjVVdPQmQ_z2lcJ2R-oXNgdfO5Wpn7iz27kw-a513buDuQQdMavStSup3Ndn6qq_lljNdPcCIKRXyHzu7UU0LcX9qQcbgU4CR31MkyKiU9YFFc6e7qjPWIDAdYWJ3D0kMaRjzlWvGoBNujumXbPM8VRr2Qe1c1IWEomNCkEczvrCX9_QzzR_y6cEwgkqSTSHwVSHKSYbBx_JUy5a5GzCnsIj2e0F6MFH5SCB1z6kuyIz2V2uVmjlV6LxaWDd8fkIvbLwhCE_5rchDJ7fr0u82eQObfxdKr-gwDZPP80uBnOZo1zukE-80wh9SsPk__5bIOS79mj5WbH6eCP-qTIMWAWuAp5AC0FNd0DU9S1vCN9rTeorKR-YL9c9yEZeG2p6X2B0SEZBCKd9WdPd1JerbmWKWJFsypQ_dRxz6ozCKdp50QoNrzXhhv5wdQznBf_H2tYx23rIh2FZWRGXaGzrIqCxDjYJ1f-9JKygZHqOSbqj3T84SL4qwS97LWtXJrY02-uPi7Rx5028QdkLKXuHBiTF8dbsDRhGhvdIRAmLo5nyzLem8E98wwVoznnpspDIhk2CVQb0wxnZiE3PA3o4a_kaVctVuyiAgk"}'
```


```shell
curl -X GET "http://127.0.0.1:8000/users" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwayI6MSwicm9sZSI6ImNvbW1vbiIsImV4cCI6MTcxMTc1MDU2MywidHlwZSI6ImFjY2VzcyIsImlhdCI6MTcxMTc0OTY2M30.cR88gIjZkhgWmDNFkXpx2a1xJ7gHYMEQmJrR1IhS1fyLiZw4huNTDBivY71BkvNqeEz4UYEcX18It6lb14vpwNS6Ne-ovoUP3gbThF7ueHhZtpgqM5Tliau-TLM76ppNaaDmeRNkeFNJ17lmixAxFkh8xk2E9bqs5RZPIc6CQ5ECxCCRSzs2R2KKD6YXLqKV6EYhNajir8-SWs0gIKXDnWDO5_CuTymLhDgZaEQm2LItcPm2dnubJKdHElzzzCHHzTZi7jmhYxTf22k_-ou0HFtK_2W7O0GUPlRiJ7X6GdLjabghEiXmvYYle6EeI685tR_YFR6FFz7XosKh_TQrguXSF-eOj4MghbvzWLpaUNabDdWzas7vFke2N54uivMWSYI06gaMNbKOzQ6AaRXLvVjzbN0o86bL7Vx8lNQbMUOHeU0xrfcvTjUCaZFixnQ_2eTDOeLhn0UFY7i80JOqlxFY9RhmSTbv71Sz3JHiVicHdLLWuA9M0gOMKCb-Xy51_0CV04w6LDxUniNZSJJgDQ0Z_AjaNQPsJ2BrUub0Qx9Wqu56xyvRRvml1L36j56y53f4fdeSsmDS-b0weYorIN_AfvAPIKcywOXGsLwN7EC4Hk5E17rApcn5AmRl150-UAO8wx6mSS4HS4LSES39PuTivPcELJ0mz7XpyzbNYZM"
```

```shell
curl -X GET "http://127.0.0.1:8000/users/me" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3JvbGUiOiJ1c2VyIiwidXNlcl9wayI6MSwianRpIjoiZjhiMzhhNTgtOTA1Yy00YjYzLTkzZDMtNTYyNGQ5MmJlZGJiIiwiaWF0IjoxNzExOTMxMjYzLCJleHAiOjE3MTE5MTMzMjMsInR5cGUiOiJhY2Nlc3MiLCJzdWIiOiJleGFtcGxlQGV4YW1wbGUuY29tIn0.I5a0hpEo-QC7Mzu5DOMDuiwKFWQtOvuh9fTIYY9VMFiMoN7JYAkaEvLXsM69BrTNxC6wqUwJNlx8hFnCQ0Xny2bpb3G2sd6Oh7kVQJHYLsr1gAfQj-HcaZTdmU9FKg203t5V0Il8M9zB1abDx0_VKk9JAd-RQFVNpJgRCssZvw8qFm1dt8JODImi2qPIM5u0wJ-KcGHifil9LrsPB4JCVWB6NEwXYo2onCH289TiZA9lohPYD19QZnKMUV0OTyXg_70igr6d-sO1ZzzirItzOxCWFege3NJmMHNG1ee4ujX6Gm0sTTSiUPWVjz3QrIG8IFXr9XnR4iSrmrgsuKx6lyWPfeUNxi3g2_TnoIba_xZDPf5w4sPdft6xpMx3gys-1_3ZAnmMlEy933ouO20tAFPNhP7k3bOo3f0IYp40lBMFJPKgtNRIR3Lx_vObiGLrUuVJlkrd4NtYVMEjjg0utGfZk75KyHFo0xTq4OX3VjL5Sy5NNL3mUTU4vV5ASWLYhIZ1r0Ff-bl156K14NvuyIwD2__gN0Uj4NsaYKDuCIDkvjGWggG9eHfNl1rWcd9yB04-v8489_kMytH9Dep2XrADJgFwBPyA3Z34CfnOKNQPiRkm8JlpEiXctdqB78WvkLxXfpDRR3c-DRa-Rh5Cwtp02XFid0Lu98Cx5rOFVfo"
```


# activate user
```shell
curl -X GET "http://127.0.0.1:8000/users/me?token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3JvbGUiOiJ1c2VyIiwidXNlcl9wayI6MSwic3ViIjoibWFpbEBleGFtcGxlLmNvbSIsImp0aSI6Ijk0MzQxYTlhLWRiYmItNDg1NC1hYTFmLWQ4MTZlODMwYjcyNCIsImlhdCI6MTcxMjIzOTY2MywiZXhwIjoxNzEyMzI2MDYzLCJ0eXBlIjoiYWN0aXZhdGUifQ.RqFkJCKldjj43Ls26T7OysepMlRjhr4G9UuqDHx4TAr66kGjwMf22pO4iGI0M-J7UswmQj68ycTZVAIX0HeQxkYqf-Sdl95mHK9aUl-xCQVHn-CL8h_rc9NZLDpOM6Hj_rNA_rq_1Urv4yj91OxvgkLSzmwSzOw2TF1l9WUToCxA1cVasMU6ARa-mMwPjS7imu7nnvcvuJxKC5JkocXMWpTL3aRaFALSUOJoCOPCWAaTCVExd5Z-fjG5ob-c5QEqSXPF9zoHdCAQREHyEeCJ0wyVb066BGdH9-LqI9fMsvVG8AUkdI1JdnH5wg1UbH9cUGa7wvhuirNAn8bp0uTb2Nm05qlTdL4zaPpcCAVs8UBiWyGaEEgPYRBXm5FTzFJtBAVvkjkh4kPdcT0DiF3mcw5-3gFJpdPaewiMaJ9QPueL32-xDaB9f8wIJxd0lZbK1Z39nICX0rXAX5E3HIVJTxOWZ7_ZnC4uTmLiOV6QAgCMcn81LGjqO57r6OCqlv6GG-cXr8_IMH2ghlmBWFVPcWUWLvsQ3kDkZnmimTirfdrK1M0JhAjPHA-5-1c7XqgiAOp787EqmTel21uJ0v-xAMNSa-YcP1u97JAPpsBDrCmrKmtlhIYbJkYenYlMsZ3R5HOCXoM0B7lrLX6dDr1lrsso71aKivgfIYsVn1XjEzE
```
