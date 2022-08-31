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

### API 如何取得
1. Youtube API 的取得方法請詳 : https://medium.com/%E5%BD%BC%E5%BE%97%E6%BD%98%E7%9A%84%E8%A9%A6%E7%85%89-%E5%8B%87%E8%80%85%E7%9A%84-100-%E9%81%93-swift-ios-app-%E8%AC%8E%E9%A1%8C/101-%E4%BD%BF%E7%94%A8-youtube-data-api-%E6%8A%93%E5%8F%96%E6%9C%89%E8%B6%A3%E7%9A%84-youtuber-%E5%BD%B1%E7%89%87-mv-d05c3a0c70aa
2. Telegram API 的取得方法請詳 : https://tcsky.cc/tips-01-telegram-chatbot/

### 能帶走的東西
1. ETL (Extraction、Transform、Load) 搭建流程
2. Managing airflow connection by CLI([傳送門](https://https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html))
3. Airflow TaskFlowAPI ([傳送門](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html))
4. Airflow HookOperator([傳送門](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html))
5. Youtube API 和 Telegram API的使用([傳送門](https://medium.com/彼得潘的試煉-勇者的-100-道-swift-ios-app-謎題/101-使用-youtube-data-api-抓取有趣的-youtuber-影片-mv-d05c3a0c70aa))
