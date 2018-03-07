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
		global urls
		global count
		global urlList
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
			elif request.split(" ")[1].startswith("/"):
				for key in urls:
					if str(request.split(" ")[1].split("/")[1]) == str(urls[key]):
						return('302 Found',
						'<html>'
							'<head><meta http-equiv="Refresh" content=' + "3;url=" + key + '></head>'
							'<body><h2>Te estamos redirigiendo...</h2></body>'
						'</html>')
						break
				return (notFound())
			else:
				return (notFound())
		elif request.split(" ")[0] == "POST":
			url = request.split("\r\n\r\n")[1].split("=")[1]
			if url != '':
				url = urllib.parse.unquote(url)
				if not url.startswith('http://') and not url.startswith('https://'):
					url = "http://" + url
				if url not in urls:
					urls[url] = count
					link = "localhost:1234/" + str(count)
					count = count + 1
					urlList = urlList + (
						'<b>URL</b>: '
						'<a href=' + url + '>' + url + '</a>'
						' <b>URL corta</b>: '
						'<a href=' + url + '>' + link + '</a><br>')
				else:
					link = "localhost:1234/" + str(urls[url])
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
	urls = {}
	count = 0
	urlList = ''
	testwebapp = aleat('localhost', 1234)
