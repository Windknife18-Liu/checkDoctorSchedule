from flask import Flask
import requests, json, time
from bs4 import BeautifulSoup
import urllib3
app = Flask(__name__)

@app.route("/")
def hello():
    url_original="https://www.femh.org.tw/webregs/RegSec1.aspx?mtypes=1&ttypes=0&ptypes=-1&id=0204&uid=";
    for i in range(5):
        url = url_original.replace("mtypes=1","mtypes="+str(i));
        urllib3.disable_warnings();  
        s = requests.session();
        s.keep_alive = False;
        html = s.get(url,verify=False)    #向網站提出Get請求
        html.encoding = "utf-8" #指定request讀取網頁時的編碼(UTF-8)，預設為ISO-8859-1
        #print(html.text)    #物件.text 取得網頁原始碼資料
        #with open("example.txt", "w", encoding="utf-8") as f:
            #f.write(html.text)
        sp = BeautifulSoup(html.text, 'html.parser')
        datas = sp.find_all('a')
        messages = "執行完成\n";
        for data in datas:
            d = data.get('data-popover-data');
            if d is not None and "邱清裕" in d:
                d = d.replace("'","");
                status = d.split(",");
                #print(status[0],status[1],status[7],sep="\n");
                #print(status[0],status[1],status[4]);
                for j in status:
                    if ("is_online:1" in j):
                        messages += status[0].split(":")[1] + " " + status[1].split(":")[1] + "\n";
            time.sleep(3);
        
    return messages;

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
