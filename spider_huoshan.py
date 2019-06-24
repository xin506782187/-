# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:23:04 2019
使用文档：

使用前，请打开redis数据库并配置连接

调用spider_ziduan（）方法获取首页视频 返回值是字典 key为info 值为视频列表 

chuli_ziduan() 处理字段 传入一个视频（类型为字典）参数 返回值为字典

download_video() 下载视频 传入name和视频url参数 自动下载到本地 name为视频名称

search_spider() 搜索用户 传入name或ID参数 返回值为字典 


@author: Lenovo
"""

import requests as r
import json
from redis import StrictRedis
class spider_huoshan:
    
    def __init__(self):
        
        # 火山视频首页url
        self.url = 'https://api-a.huoshan.com/hotsoon/feed/?type=video&tab_id=5&min_time=0&offset=0&count=10&req_from=feed_refresh&diff_stream=1&ad_user_agent=com.ss.android.ugc.live%2F600+%28Linux%3B+U%3B+Android+5.1.1%3B+zh_CN%3B+sm-g9350%3B+Build%2FLMY48Z%3B+Chrome%29&live_sdk_version=600&iid=75668895904&device_id=60557671082&ac=wifi&channel=pcandroid&aid=1112&app_name=live_stream&version_code=600&version_name=6.0.0&device_platform=android&ssmix=a&device_type=sm-g9350&device_brand=samsung&language=zh&os_api=22&os_version=5.1.1&uuid=865166025247605&openudid=97ac9662ad102cc2&manifest_version_code=600&resolution=1280*720&dpi=240&update_version_code=6003&_rticket=1561020746271&ab_version=938059%2C957640%2C959407%2C922854%2C712301%2C914029%2C304713%2C936961%2C689928%2C928648%2C839334%2C963001%2C692223%2C870745%2C850766%2C841787%2C830473%2C662292%2C943434%2C557631%2C956109%2C951620%2C947985%2C911477%2C950307%2C848691%2C819014%2C661942%2C949507%2C705072%2C960847%2C929430%2C682009%2C841998%2C913504%2C963175%2C665355%2C832456%2C914333%2C949017%2C643984%2C920238%2C927646%2C957244%2C958583%2C457535%2C797937%2C768607%2C526417&ab_group=526417&mcc_mnc=46000&ts=1561020745&as=a2d594b0c9c4fd596b6200&cp=4949db5b9eb8069fe2Uc]g&mas=00fd2a95688dccaa8f4de78f0d7a1e40bd5ead880082c0c4b2'
                    
        self.headers = {
            'User-Agent': 'okhttp/3.10.0.1',
            'Connection': 'Keep-Alive',
            'Cookie': 'odin_tt="9f592d7ed78933e8252693c82fd967563faf7b0079a71cfb4a709b1d3b4b1b3f39b114d0990989156be5908db8a11e974d5367f540e176341fc5dd7970cdb7e9";qh[360]=1;install_id="75668895904";ttreq="1$7ca535fd378401b4fc72ec7859d899e849883c72";$Path="/";$Domain="snssdk.com";',
            'Accept-Encoding': 'gzip',
            'X-SS-REQ-TICKET': '1561013633154',
            'sdk-version': '1',
            'X-Gorgon': '03006cc004005eb00c0f7d58cad357d1f66be2ac9f2ddb49cf4b',
            'X-Khronos': '1561013633',
            'X-Pods': '',
            'Host': 'api.huoshan.com'
            }
        
        #  评论url
        self.comment_url = 'https://api-a.huoshan.com/hotsoon/item/{}/comments/?offset=0&count=20&req_from=normal&sort_type&live_sdk_version=600&iid=75668895904&device_id=60557671082&ac=wifi&channel=pcandroid&aid=1112&app_name=live_stream&version_code=600&version_name=6.0.0&device_platform=android&ssmix=a&device_type=sm-g9350&device_brand=samsung&language=zh&os_api=22&os_version=5.1.1&uuid=865166025247605&openudid=97ac9662ad102cc2&manifest_version_code=600&resolution=720*1280&dpi=240&update_version_code=6003&_rticket=1560823766596&ab_version=938059%2C818773%2C839334%2C922854%2C712301%2C914029%2C304713%2C936961%2C689928%2C928648%2C692223%2C870745%2C850766%2C956295%2C830473%2C662292%2C943434%2C557631%2C927652%2C953519%2C956109%2C951620%2C947985%2C911477%2C950307%2C848691%2C819014%2C661942%2C949507%2C705072%2C929458%2C929430%2C682009%2C901581%2C841998%2C913504%2C665355%2C913408%2C832456%2C914333%2C949017%2C643984%2C920238%2C908118%2C927646%2C457535%2C797937%2C768607%2C526417&ab_group=526417&mcc_mnc=46000&ts=1560823767&as=a2655470979d3da7a86288&cp=4cd5d258768b0970e2[cIg&mas=008417becd0b92d3afc2265443a9de2e928c407ca582d0d5f8'
        
        self.r1 = StrictRedis(db='3',port='6379')
        
        self.rst = ''
        
        self.cont = ''
    def spider_ziduan(self):
        
        try:
            
            # 获取 8 个首页视频（每次请求，视频都不同）
            self.rst = r.get(self.url, headers = self.headers,timeout=60).text
            
        except Exception as arr:
            
            print('失败!',arr.args)
        
        # 判断是否成功获取视频
        if 'data' not in self.rst:
            
            return self.rst
        
        self.rst = json.loads(self.rst)['data']
        
        # 处理过后的视频列表
        info_list = []
        
        if 'info_to' in self.r1:
            
            info_to = json.loads(self.r1.get('info_to'))
        
        else:
            
            info_to = {'info':[]}
        
        for i in self.rst:
            
            # 单个视频的数据
            j = i['data']
            
            # 判断stats 是否在每个视频里面(因为要过滤掉广告)
            if 'stats' in j:
                
                # 下载视频
                self.download_video(j['share_title'],j['video']['download_url'][0])
                
                # 评论列表
                comment_content = []
                
                try:
                    # 获取评论内容 返回值为列表
                    for c in json.loads(r.get(self.comment_url.format(j['id']),headers = self.headers).text)['data']['comments']:
                        
                        comment_content.append(c['text'])
                        
                except:
                    
                    print('失败',j['id'])
                    
                else:
                    
                    # 调用方法 提取字段
                    info = self.chuli_ziduan(j)
                    
                    # 添加评论内容
                    info['comment_content'] = comment_content
                        
                
                    info_list.append(info)
                    
                    info_to['info'].insert(0,info)
                
        print('成功!')
        
        self.r1.set('info',json.dumps({'info': info_list}))
        
        self.r1.set('info_to',json.dumps(info_to))
        
        return {'info': info_list}        
    
    def chuli_ziduan(self,info):
        
        author = info['author'] # 作者信息
            
        stats = info['stats'] # 视频信息统计
        
        video = info['video'] # 视频信息
        
        info_to = {  # 单个视频的总字段
                
             # 视频id
            'id':info['id'], 
            
             # 作者的城市
            'auth_city':author['city'], 
            
            # 作者的昵称
            'auth_nickname':author['nickname'], 
            
            #  作者标志 
            'auth_hotsoon_verified_reason':author['hotsoon_verified_reason'],
            
            # 视频火力值
            'auth_fan_ticket_count':author['fan_ticket_count'],
            
            # 年龄描述 例如(90后)
            'auth_birthday_description':author['birthday_description'],
            
            # 作者头像
            'auth_avatar_jpg':author['avatar_jpg']['url_list'][0],
            
            # 性别(1:男, 2:女)
            'auth_gender':author['gender'],
            
            # 作者ID
            'auth_short_id':author['short_id'],
            
            # 个人签名
            'auth_signature':author['signature'],
            
            # 视频描述
            'description':info['description'],
            
            # 分享描述
            'share_description':info['share_description'],
            
            # 分享标题
            'share_title':info['share_title'],
            
            # 分享url
            'share_url':info['share_url'],
            
            # 评论数
            'stats_comment_count':stats['comment_count'],
            
            # 点心人数
            'stats_digg_count':stats['digg_count'],
            
            # 播放次数
            'stats_play_count':stats['play_count'],
            
            # 转发次数
            'stats_share_count':stats['share_count'],
            
            # 封面
            'video_cover':video['cover']['url_list'][0],
            
            # 视频url
            'video_download_url':video['download_url'][0],
            
            # 播放时长
            'video_duration':video['duration'],
            
#            # 音频url
#            'video_h265_url':video['h265_url'][0],
            
            }
        return info_to
    
    # 下载视频
    def download_video(self,name,url):
        
        try:
            
            self.cont = r.get(url,timeout=60)
        
        except Exception as arr:
            
            print(name,arr.args)
        
        with open('static/MP4/{}.mp4'.format(name),'wb') as f:
                
            f.write(self.cont.content)
            
        print('下载成功!')
    
    # 下载视频
    def download_video_(self,name,url):
        
        try:
        
            self.cont = r.get(url,timeout=60)
            
        except Exception as arr:
            
            print(name,arr.args)
            
        with open('static/geren_mp4/{}.mp4'.format(name),'wb') as f:
                
            f.write(self.cont.content)
        
        print('下载成功!')
    
    # 搜索用户
    def search_spider(self,name):
        
        # 判断用户是否存在redis内
        if name in self.r1:
            
            return json.loads(self.r1.get(name))
        
        name_to = r.utils.quote(name)
        
        # 搜索url
        search_url = 'https://api.huoshan.com/hotsoon/general_search/?query={}&count=20&search_id&user_action=Initiative&click_rectify_bar=0&offset=0&search_type=2&live_sdk_version=600&iid=75668895904&device_id=60557671082&ac=wifi&channel=pcandroid&aid=1112&app_name=live_stream&version_code=600&version_name=6.0.0&device_platform=android&ssmix=a&device_type=sm-g9350&device_brand=samsung&language=zh&os_api=22&os_version=5.1.1&uuid=865166025247605&openudid=97ac9662ad102cc2&manifest_version_code=600&resolution=1280*720&dpi=240&update_version_code=6003&_rticket=1560993770331&ab_version=938059%2C957640%2C959407%2C922854%2C712301%2C914029%2C304713%2C936961%2C689928%2C928648%2C839334%2C692223%2C870745%2C850766%2C830473%2C662292%2C943434%2C557631%2C956109%2C951620%2C947985%2C911477%2C950307%2C848691%2C819014%2C661942%2C949507%2C705072%2C960847%2C929430%2C682009%2C841998%2C913504%2C665355%2C832456%2C914333%2C949017%2C643984%2C920238%2C927646%2C938437%2C957244%2C958583%2C457535%2C797937%2C768607%2C526417&ab_group=526417&mcc_mnc=46000&ts=1560993770&as=a275fd708a2ecdef2a6655&cp=dcebd055aba108fae2Wc_g&mas=00a861dfc576bed36f37df054c5716a8f604224a0ca2626ee2'
        
        while True:
            
            try:
                
                # 获取用户信息
                rst = json.loads(r.get(search_url.format(name_to),headers = self.headers,timeout = 60).text)
            
                # 判断返回值是否等于 0  如果不等于 返回值内容不对 重新获取
                if rst['status_code'] == 0:
                       
                    break
                    
                print('失败!')
                
                
            except Exception:
                
                print('请求超时!')
                
#                return {'info':'请求超时!'}
        
        print('成功!')
        
        # 视频列表
        info_list = []
        
        for i in rst['data'][0]['item_result']['items']:
            
            # 提取字段
            info_ = self.chuli_ziduan(i['item'])
            
            # 下载视频
            self.download_video_(info_['share_title'],info_['video_download_url'])
            
#            if info_['auth_nickname'] == name:
            
            # 添加到视频列表
            info_list.append(info_)
        
        # 保存到redis
        self.r1.set(name,json.dumps({'info':info_list}))
       
        return {'info':info_list}

if __name__ == '__main__':
    
    spider = spider_huoshan()

#    info = spider.spider_ziduan()

    info_tto = spider.search_spider('多多🎙唱歌给你听')
