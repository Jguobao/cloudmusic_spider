#-*-coding:UTF-8-*-
import requests
import json
import execjs
import hashlib
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable


def main():
	class cloudmusic():

		session = requests.Session()

		#相关参数
		phone = "***********"	# 手机号
		password = "**********"	# 密码
		myInfo = {}

		def __init__(self):		# 初始化

			if self.login():
				while(True):

					op_dict = {
						'person':[
							'获取个人信息','获取最新消息通知','获取个人歌单','获取个人听歌记录',
							'获取每日推荐','获取关注的用户','获取粉丝','歌曲评论','歌单评论',
							'回复歌曲评论','回复歌单评论','关注某人','取关某人'
						],
						'search':[
							'搜索单曲','搜索歌手','搜索专辑','搜索视频', 
						 	'搜索歌词','搜索歌单','搜索主播电台','搜索用户'
						],
						'song':[
							'获取歌曲详细信息','获取歌曲真链','获取歌曲评论','获取歌词'
						],
						'playlist':[
							'获取歌单详细信息','获取歌单评论'
						]
					}

					operator = [self.printMyInfo,self.getNewInfo,self.getPlayList,self.getRecord,
					self.getDaySong,self.getFollowing,self.getFollowed,self.addSongComment,
					self.addPlayListComment,self.follow,self.defollow,self.searchSong,self.searchSinger,
					self.searchAlbum,self.searchMv,self.searchLyric,self.searchPlayList,self.searchDiantai,
					self.searchUser,self.getSongDetail,self.getSongUrl,self.getComments,
					self.getLyric,self.getPlayListInfo,self.getPlayListComments]

					print('所有功能如下：\n')
					table = PrettyTable(['功能编号','功能名称','功能类型'])
					table.padding_width = 2

					for i in range(0,len(op_dict['person'])):
						table.add_row([i,op_dict['person'][i],'个人操作'])
					
					for i in range(0,len(op_dict['search'])):
						op_num = i + len(op_dict['person'])
						table.add_row([op_num,op_dict['search'][i],'搜索操作'])

					for i in range(0,len(op_dict['song'])):
						op_num = i + len(op_dict['person']) + len(op_dict['search'])
						table.add_row([op_num,op_dict['song'][i],'歌曲操作'])

					for i in range(0,len(op_dict['playlist'])):
						op_num = i + len(op_dict['person']) + len(op_dict['search']) + len(op_dict['song'])
						table.add_row([op_num,op_dict['playlist'][i],'歌单操作'])

					print(table)

					op = input('\n请输入功能编号：')
					operator[int(op)]()

		def md5Encrypt(self,str_data):	# MD5加密

			m = hashlib.md5()
			m.update(str_data.encode("UTF-8"))
			return m.hexdigest()


		def paramEncrypt(self,json_data):	# 加密参数

			str_data = json.dumps(json_data)
			fp = open('./参数加密.js','r',encoding='utf-8')
			js = fp.read()
			fp.close()
			ctx = execjs.compile(js)
			encryptParams = ctx.call('getParams',str_data)
			return encryptParams


		######  个人操作  ######

		def login(self):	# 登录操作

			loginUrl = "http://music.163.com/weapi/login/cellphone?csrf_token="
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Pragma':'no-cache',
				'Proxy-Connection':'keep-alive',
				'Referer':'http://music.163.com/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			# 密码先进行md5加密
			json_data = {
				"phone":self.phone,
				"password":self.md5Encrypt(self.password),
				"rememberLogin":"true",
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			params = encryptParams['encText']
			encSecKey = encryptParams['encSecKey']
			post_data = {
				'params':params,
				'encSecKey':encSecKey
			}
			req = self.session.post(url=loginUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			if json_return_data['code'] == 200:
				print('登录成功')
				self.myInfo = json_return_data
				return True
			else:
				print('登录失败')
				return False

		def printMyInfo(self):

			print(self.myInfo)


		def getNewInfo(self):	# 获取最新消息通知

			newInfoUrl = "http://music.163.com/weapi/pl/count?csrf_token="
			json_data = {
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=newInfoUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def getPlayList(self):	# 获取个人歌单

			playListUrl = "http://music.163.com/weapi/user/playlist?csrf_token="
			limit = 36
			offset = 0
			uid = self.myInfo["bindings"][0]["userId"]
			wordwrap = 7
			json_data = {
				"csrf_token":"",
				"limit":limit,
				"offset":offset,
				"total":True,
				"uid":uid,
				"wordwrap":wordwrap
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=playListUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def getRecord(self):	# 获取个人听歌记录

			recordUrl = "http://music.163.com/weapi/v1/play/record?csrf_token="
			limit = 1000
			offset = 0
			uid = self.myInfo["bindings"][0]["userId"]
			wordwrap = 7	
			type = "-1"		# -1、周排行和所有时间排行 0、所有时间排行 1、周排行
			json_data = {
				"csrf_token":"",
				"limit":limit,
				"offset":offset,
				"total":True,
				"type":type,
				"uid":uid
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=recordUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def getDaySong(self):	# 获取每日推荐

			discoveryUrl = "http://music.163.com/weapi/v2/discovery/recommend/songs?csrf_token="
			limit = 20
			offset = 0
			json_data = {
				"csrf_token":"",
				"limit":limit,
				"offset":offset,
				"total":True
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=discoveryUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def getFollowing(self):		# 获取关注的用户

			uid = self.myInfo["bindings"][0]["userId"]
			followingUrl = "http://music.163.com/weapi/user/getfollows/"+str(uid)+"?csrf_token="
			limit = 1000
			offset = 0
			json_data = {
				"csrf_token":"",
				"limit":limit,
				"offset":offset,
				"order":True,
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=followingUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		def getFollowed(self):		# 获取粉丝

			followedUrl = "http://music.163.com/weapi/user/getfolloweds?csrf_token="
			uid = self.myInfo["bindings"][0]["userId"]
			limit = 1000
			offset = 0
			json_data = {
				"userId":uid,
				"csrf_token":"",
				"limit":limit,
				"offset":offset,
				"total":True,
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=followedUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def addComment(self,type,content,id):	# 评论，type为歌曲评论或歌单评论

			addCommentUrl = "http://music.163.com/weapi/resource/comments/add?csrf_token="
			if type=="song":
				threadId = "R_SO_4_"+str(id)
				referer = 'http://music.163.com/song?id='+str(id)
			elif type=="playList":
				threadId = "A_PL_0_"+str(id)
				referer = 'http://music.163.com/playlist?id='+str(id)
			json_data = {
				"threadId":threadId,
				"content":content,
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':referer,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=addCommentUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		def addSongComment(self):	# 评论单曲

			content = input('输入评论内容：')
			songId = input('输入歌曲id：')
			self.addComment('song',content,songId)

		def addPlayListComment(self):	# 评论歌单

			content = input('输入评论内容：')
			playListId = input('输入歌单id：')
			self.addComment('playList',content,playListId)

		def replyComment(self,type,commentId,content,id):	# 回复评论

			replyCommentUrl = "http://music.163.com/weapi/v1/resource/comments/reply?csrf_token="
			if type=="song":
				threadId = "R_SO_4_"+str(id)
				referer = 'http://music.163.com/song?id='+str(id)
			elif type=="playList":
				threadId = "A_PL_0_"+str(id)
				referer = 'http://music.163.com/playlist?id='+str(id)
			json_data = {
				"commentId":commentId,
				"threadId":threadId,
				"content":content,
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':referer,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=replyCommentUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		def replySongComment(self):	# 回复歌曲评论

			commentId = input('输入评论id：')
			content = input('输入评论内容：')
			songId = input('输入歌曲id：')

			self.replyComment('song',commentId,content,songId)

		def replyPlayListComment(self):	# 回复歌单评论

			commentId = input('输入评论id：')
			content = input('输入评论内容：')
			playListId = input('输入歌单id：')

			self.replyComment('playList',commentId,content,playListId)

		def follow(self):	# 关注某人

			followId = input('关注的用户的id：')
			followUrl = "http://music.163.com/weapi/user/follow/"+str(followId)+"?csrf_token="
			json_data = {
				"followId":followId,
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':"http://music.163.com/user/home?id="+str(followId),
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=followUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		def defollow(self):	# 取关

			followId = input('取关用户的id：')
			followUrl = "http://music.163.com/weapi/user/defollow/"+str(followId)+"?csrf_token="
			json_data = {
				"followId":followId,
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':"http://music.163.com/user/home?id="+str(followId),
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=followUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		######  搜索操作  ######

		def search(self,type,content):	# 搜索

			searchUrl = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/search/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			# 搜索类型：1、单曲 100、歌手 10、专辑 1014、视频 1006、歌词 1000、歌单 1009、主播电台
			# 1002、用户
			type = "1"
			offset = 0
			limit = 30
			json_data = {
				"hlposttag":"</span>",
				"hlpretag":"<span class=\"s-fc7\">",
				"id":"289257301",
				"limit":limit,
				"offset":offset,
				"s":content,
				"total":True,
				"type":type
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/search/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=searchUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		def searchSong(self):

			content = input('输入搜索内容：')
			self.search(1,content)

		def searchSinger(self):

			content = input('输入搜索内容：')
			self.search(100,content)

		def searchAlbum(self):

			content = input('输入搜索内容：')
			self.search(10,content)

		def searchMv(self):

			content = input('输入搜索内容：')
			self.search(1014,content)

		def searchLyric(self):

			content = input('输入搜索内容：')
			self.search(1006,content)

		def searchPlayList(self):

			content = input('输入搜索内容：')
			self.search(1000,content)

		def searchDiantai(self):

			content = input('输入搜索内容：')
			self.search(1009,content)

		def searchUser(self):

			content = input('输入搜索内容：')
			self.search(1002,content)

		######  歌曲操作  ######

		def getSongUrl(self):	# 根据songId获取歌曲播放url

			songId = input('歌曲id：')
			requestUrl = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
			json_data = {
				"ids":"["+songId+"]",
				"br":"128000",
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=requestUrl,data=post_data,headers=headers)
			print(req.text) 


		def getComments(self):	# 获取评论

			songId = input('歌曲id：')
			getCommentsUrl = "http://music.163.com/api/v1/resource/comments/R_SO_4_"+songId
			offset = 0
			limit = 20
			json_data = {
				"rid":"R_SO_4_"+songId,
				"offset":offset,
				"limit":limit,
				"total":True,
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/song?id='+songId,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=getCommentsUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def getLyric(self):	# 获取歌词

			songId = input('歌曲id：')
			getCommentsUrl = "http://music.163.com/weapi/song/lyric?csrf_token="
			offset = 0
			limit = 20
			json_data = {
				"id":songId,
				"lv":"-1",
				"tv":"-1",
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/song?id='+songId,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=getCommentsUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)


		def getSongDetail(self):

			songId = input('歌曲id：')
			songDetailUrl = "http://music.163.com/weapi/v3/song/detail?csrf_token="
			json_data = {
				"id":songId,
				"c":"[{\"id\":\""+songId+"\"}]",
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/song?id='+songId,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=songDetailUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		######  歌单操作  ######

		def getPlayListComments(self):	# 获取歌单评论

			playListId = input('歌单id：')
			playListCommentsUrl = "http://music.163.com/weapi/v1/resource/comments/A_PL_0_"+str(playListId)+"?csrf_token="
			offset = 0
			limit = 20
			json_data = {
				"rid":"A_PL_0_"+playListId,
				"offset":offset,
				"limit":limit,
				"total":True,
				"csrf_token":""
			}
			encryptParams = self.paramEncrypt(json_data)
			post_data = {
				'params':encryptParams["encText"],
				'encSecKey':encryptParams['encSecKey']
			}
			headers = {
				'Host':'music.163.com',
				'Origin':'http://music.163.com',
				'Referer':'http://music.163.com/playlist?id='+playListId,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
			}
			req = self.session.post(url=playListCommentsUrl,data=post_data,headers=headers)
			json_return_data = json.loads(req.text)
			print(json_return_data)

		def getPlayListInfo(self):		# 获取歌单详细信息

			playListId = input('歌单id：')
			playlistInfoUrl = "http://music.163.com/playlist?id=864112683"
			headers = {
				'Host':'music.163.com',
				'Referer':'http://music.163.com/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
			}
			req = self.session.get(playlistInfoUrl,headers=headers)
			html = BeautifulSoup(req.text,"html.parser")

			playListInfo = {}

			# 歌单信息
			script = html.select('script')[0].text
			json_script = json.loads(script)
			playListInfo['title'] = json_script['title']	# 标题
			playListInfo['images'] = json_script['images']	# 图片
			playListInfo['description'] = json_script['description']	# 描述
			playListInfo['pubDate'] = json_script['pubDate']	# 创建时间
			playListInfo['href'] = json_script['@id']	# 创建时间
			playListInfo['id'] = playListId		# 歌曲id
			tag_is = html.select('.tags .u-tag i')
			playListInfo['tags'] = '/'.join([i.text for i in tag_is])
			playListInfo['playCount'] = html.select('#play-count')[0].text

			# 歌单歌曲
			playListInfo['songs'] = []
			li_as = html.select("#song-list-pre-cache ul li a")
			for li_a in li_as:
				songInfo = {}
				songInfo['name'] = li_a.text
				songInfo['href'] = 'http://music.163.com'+li_a['href']
				songInfo['id'] = re.findall(r'id\=(\d*)',li_a['href'])[0]

				playListInfo['songs'].append(songInfo)

			print(playListInfo)


	cloudmusic = cloudmusic()

if __name__ == '__main__':
	main()