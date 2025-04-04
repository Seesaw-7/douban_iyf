# douban_iyf
Check whether films in a douban list are available on iyf.tv

豆瓣网想看列表爬取，并搜索是否可在爱壹帆播放

爱壹帆会员贵，且经典电影片源不全


## Run
下载对应版本的chrome driver

登录豆瓣，拷贝自己的账号的想看列表url
 eg. `https://movie.douban.com/people/<9位左右用户数字>/wish`
相应地，修改脚本中`base_url`
 
运行：
```zsh
pip install -r requirements.txt
python3 src/douban_list.py
python3 src/iyf_search.py
python3 src/refine.py
```

结果请见`available.txt`
