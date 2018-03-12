from webapp import webApp
import random
import urllib.parse

def notFound():
	return ("404 Not Found",
	'<html>'
		'<body>'
			"<h2>404: Recurso no encontrado</h2>"
		'</body>'
	'</html>')

class aleat(webApp):

	def process(self, request):
		try:
			urls = open('urls.txt', 'r')
			urlList = urls.read()
			urls.close()
			try:
				count = int(urlList.split('/')[-2].split('<')[0]) + 1
			except IndexError:
				count = 0
		except IOError:
			urls = open('urls.txt', 'w')
			urlList = ''
			count = 0
			urls.close()
		if request.split(" ")[0] == "GET":
			if request.split(" ")[1] == "/":
				return ("200 OK",
				'<html>'
					'<body>'
						'<h2>Acortar URLs:</h2>'
						'<form action="/" method="post">'
						  	'<input type="text" name="URL" value="Introduce la URL">'
							'<input type="submit" value="Acortar">'
						'</form>'
						'<h2>Lista de URLs acortadas:</h2>' +
						urlList +
					'</body>'
				'</html>')
			elif request.split(" ")[1] == "/favicon.ico":
				return (notFound())
			elif 'localhost:1234' + request.split(" ")[1] + '<' in urlList:
				url = urlList.split('>' + 'localhost:1234' + request.split(" ")[1] + '<')[0]
				url = url.split('=')[-1]
				return('302 Found',
				'<html>'
					'<head><meta http-equiv="Refresh" content=' + "3;url=" + url + '></head>'
					'<body><h2>Te estamos redirigiendo...</h2></body>'
				'</html>')
			else:
				return (notFound())
		elif request.split(" ")[0] == "POST":
			url = request.split("\r\n\r\n")[1].split("=")[1]
			if url != '':
				url = urllib.parse.unquote(url)
				if not url.startswith('http://') and not url.startswith('https://'):
					url = "http://" + url
				if url not in urlList:
					link = "localhost:1234/" + str(count)
					count = count + 1
					urls = open('urls.txt', 'a')
					urls.write(
						'<b>URL</b>: '
						'<a href=' + url + '>' + url + '</a>'
						' <b>URL corta</b>: '
						'<a href=' + url + '>' + link + '</a><br>')
					urls.close()
				else:
					urls = open('urls.txt', 'r')
					link = urlList.split(url + '>')[-1].split('<')[0]
					urls.close()
				return("200 OK",
					'<html>'
						'<body>'
							'<h2>Correspondencia:</h2>'
							'<b>URL</b>: ' +
							'<a href=' + url + '>' + url + '</a>'
							' <b>URL Corta</b>: '
							'<a href=' + url + '>' + link + '</a>'
						'</body>'
					'</html>')
			else:
				return notFound()

if __name__ == '__main__':
	testwebapp = aleat('localhost', 1234)
