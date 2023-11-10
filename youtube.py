import sys 
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, startPage, endPage):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
					  developerKey=DEVELOPER_KEY)
	
	
	#so we can get next page token
	search_response1 = youtube.search().list(
		q=query_term,
		part='id,snippet',
		maxResults=max_results,
	).execute()
	pageNum = 1
	page = search_response1
	
	pageList = []
	if startPage == 1:
		pageList.append(page.get('items', []))

	while pageNum < endPage:
		# Call the search.list method to retrieve results matching the specified
		#query term.
		search_response2 = youtube.search().list(
			q=query_term,
			part='id,snippet',
			maxResults=max_results,
			pageToken= page.get('nextPageToken'),
		).execute()
		
		page = search_response2
		pageNum +=1
		if pageNum <= endPage and pageNum >= startPage:
			pageList.append(page.get('items', []))

	return pageList


if __name__ == "__main__":
	query_term = sys.argv[1]
	max_results = sys.argv[2]
	startPage = sys.argv[3]
	endPage = sys.argv[4]
	try:
		print(youtube_search(query_term, max_results, int(startPage), int(endPage)))
	except HttpError as e:
		print('An HTTP error %d occurred:\n%s' % (type(e).__name__, str(e)))
