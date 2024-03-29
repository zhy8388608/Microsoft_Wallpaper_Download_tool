#pip install requests

import requests
import os
import json
import datetime

output_folder = 'out'
os.makedirs(output_folder, exist_ok=True)

def getWallpaperImageList():	#Note: Wallpapers are different for different regions.
	result = []
	for i in (0,7):	#idx is the number of the first image and n is the number of response images. idx+n<14.
		response = requests.get('https://bing.com/HPImageArchive.aspx?format=js&idx=%d&n=7' % (i))
		if response.status_code != 200:
			print('Error: Unable to connect to the server.')
			return result
		result += json.loads(response.text)['images']
	return result

def download(images, number, size='1920x1080'):
	print('Image resolution: %s' % (size))
	number = min(number, len(images))
	now = datetime.datetime.now()
	for i in range(0,number):
		dateText = (now + datetime.timedelta(days = -i)).strftime('%Y-%m-%d')
		name = 'out/%s_%s_%s.jpg' % (dateText, size, images[i]['copyright'].replace('/','#'))
		print('Downloading image%d...' % (i), end = '')
		if os.path.exists(name):
			print('Skipped: The image file already exists.')
			continue
		url = 'https://bing.com' + images[i]['url']
		url = url.replace('1920x1080', size)
		response = requests.get(url)
		if response.status_code != 200:
			print('Error: Images of this resolution do not exist.')
			return
		with open(name, 'wb') as f:
			f.write(response.content)
		print('Success.')
	print('Done.')

def main():
	print('Getting URLs...', end = '')
	urls = getWallpaperImageList()
	print('Done.')
	download(urls, 14, '1920x1080')
	download(urls, 14, '1080x1920')
	#download(urls, 14, '1920x1200')

if __name__ == '__main__':
	main()
