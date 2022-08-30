# Learning English assistant
### 簡介
* 詳細開發過程記錄 Medium 版本([傳送門](https://medium.com/@ChickenBenny/%E5%AD%B8%E7%BF%92%E8%8B%B1%E6%96%87%E5%B0%8F%E5%B7%A5%E5%85%B7%E9%96%8B%E7%99%BC%E7%AD%86%E8%A8%98-78f8a813c7af))
* HackMD 版本([傳送門](https://hackmd.io/-BLvXFm3STqacYMSedyKWA?view))

這是一個能幫助你學習英文的小工具，主要是使用Airflow和Python開發的。功能如下:
1. 每日定時使用telegram推送英文vlog讓你收看，讓你學習不間斷。
2. 能夠追蹤自己喜歡的英文頻道，頻道一有更新馬上幫你抓到資料庫中。
3. 查看自己的學習紀錄，讓你成就滿滿!

### Quick start
1. Clone the repo and get into the folder
```
$ git clone https://github.com/ChickenBenny/Airflow-Learning-English-tool.git
$ cd Airflow-Learning-English-tool
```
2. Use docker-compose up to build the app
```
$ docker-compose up -d
```
3. Set the connection and make sure you have telegram and youtube api
```
$ docker exec -it webserver airflow connections add 'database' --conn-type 'postgres' --conn-login 'airflow' --conn-password 'airflow' --conn-host 'database' --conn-port '5432' --conn-schema 'airflow'
$ docker exec -it webserver airflow connections add 'telegram' --conn-type 'http' --conn-host ${chat id} --conn-password ${api token}
```
4. You need to change the api token in the folders, which are `/dags/credentials` and `/init/credentials`.
![](https://i.imgur.com/6Kq09lx.png)

5. Have fun and play with it !!


