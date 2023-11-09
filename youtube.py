import sys 
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
					  developerKey=DEVELOPER_KEY)
	
	#so we can get next page token
	search_response1 = youtube.search().list(
		q=query_term,
		part='id,snippet',
		maxResults=max_results,
	).execute()

	# Call the search.list method to retrieve results matching the specified
	#query term.
	search_response2 = youtube.search().list(
		q=query_term,
		part='id,snippet',
		maxResults=max_results,
		pageToken= search_response1.get('nextPageToken'),
	).execute()

	#added this to make it a little more readable
	videos = []

	for search_result in search_response1.get('items', []):
		if search_result['id']['kind'] == 'youtube#video':
			videos.append('%s (%s)' % (search_result['snippet']['title'], 
										search_result['id']['videoId']))
	
	print('Videos:\n', '\n'.join(videos), '\n')
	return search_response1.get('items', []), search_response2.get('items', [])


if __name__ == "__main__":
	query_term = sys.argv[1]
	max_results = sys.argv[2]
	try:
		print(youtube_search(query_term, max_results))
	except HttpError as e:
		print('An HTTP error %d occurred:\n%s' % (type(e).__name__, str(e)))
