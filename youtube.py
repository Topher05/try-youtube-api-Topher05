import sys 
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, pageNum):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
					  developerKey=DEVELOPER_KEY)
	
	
	#so we can get next page token
	search_response1 = youtube.search().list(
		q=query_term,
		part='id,snippet',
		maxResults=max_results,
	).execute()

	page = search_response1
	while pageNum > 0:
		# Call the search.list method to retrieve results matching the specified
		#query term.
		search_response2 = youtube.search().list(
			q=query_term,
			part='id,snippet',
			maxResults=max_results,
			pageToken= page.get('nextPageToken'),
		).execute()
		
		page = search_response2
		pageNum -=1

	return page.get('items', [])


if __name__ == "__main__":
	query_term = sys.argv[1]
	max_results = sys.argv[2]
	pageNum = sys.argv[3]
	try:
		print(youtube_search(query_term, max_results, int(pageNum)))
	except HttpError as e:
		print('An HTTP error %d occurred:\n%s' % (type(e).__name__, str(e)))
