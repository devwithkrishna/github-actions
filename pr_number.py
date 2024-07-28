import os
import re
import requests
import json
from dotenv import load_dotenv

def get_branch_or_tag_name():
  return os.environ.get('GITHUB_REF_NAME', None)


def get_pull_request_number(ref_name):
  match = re.match(r'^refs/pull/(\d+)/merge$', ref_name)
  if match:
    return int(match.group(1))
  return None


def get_assignees_of_a_pull_request(assignees: list):
	"""
	Assignees on a PR can be upto 10 nos. getting the names of assignees corresponding to the PR
	:param assignees:
	:return:
	"""
	assignees_list = []
	for assignee in assignees:
		assignees_list.append(assignee['login'])

	return assignees_list


def get_labels_of_a_pull_request(labels: list):
	"""
	Labels on a PR can be multiple. getting the labels on a pr
	:param labels:
	:return:
	"""
	labels_list = []
	for label in labels:
		labels_list.append(label['name'])

	return labels_list


def get_details_from_pull_request():
	"""
	get details from a PR in github
	:return:
	"""
	github_repository = os.getenv('GITHUB_REPOSITORY') # The owner and repository name
	pull = 2
	api_url = f'https://api.github.com/repos/{github_repository}/pulls/{pull}'
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
		"X-GitHub-Api-Version": "2022-11-28"
	}
	print(f'Retreving details from pull request #{pull} - {github_repository} repository')
	response = requests.get(url=api_url, headers=headers)
	if response.status_code == 200:
		print(f'Data retrieved from pull request #{pull} from {github_repository}')
		response_json = response.json()
		# print(response_json)
	elif response.status_code == 304:
		print(f'Not Modified')
	elif response.status_code == 404:
		print(f'Resource Not found')
	elif response.status_code == 406:
		print(f'Unacceptable')
	elif response.status_code == 500:
		print(f'internal server error')
	else:
		print('Service unavailable')
	pull_request_details = {}
	pull_request_details['pull_request_title'] = response_json['title']
	pull_request_details['pull_request_url'] = response_json['url']
	pull_request_details['pull_request_opened_by'] = response_json['user']['login']
	pull_request_details['pull_request_body'] = response_json['body']
	pull_request_details['pull_request_created_at'] = response_json['created_at']
	pull_request_details['pull_request_closed_at'] = response_json['closed_at']
	assignees_list = get_assignees_of_a_pull_request(response_json['assignees'])
	pull_request_details['pull_request_assignee'] = assignees_list
	labes_list = get_labels_of_a_pull_request(response_json['labels'])
	pull_request_details['pull_request_labels'] = labes_list
	pull_request_details['total_commits'] = response_json['commits']

	# # Convert dictionary to JSON string and print it
	pull_request_details_json = json.dumps(pull_request_details, indent=4)
	print(pull_request_details_json)
	return pull_request_details


def main():
	"""To run the code"""
	load_dotenv()
	branch_or_tag = get_branch_or_tag_name()
	if branch_or_tag:
		print(f"Current branch or tag: {branch_or_tag}")
		pull_request_number = get_pull_request_number(branch_or_tag)
		print(f"Pull Request Number: {pull_request_number}")

	# Do something with the branch or tag name
	else:
		print("Branch or tag name not available")
	



if __name__ =="__main__":
	main()
