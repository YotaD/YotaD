#!/usr/bin/env python
"""
github.py - Yota Github Info Module
Copyright 2009-2015, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.
Copyright 2016, Santos D. Dominges
^Yota^ by SantosD
"""

import json
import random
import re
import traceback
import urllib2
import urlparse

# For information about the Github API check out https://developer.github.com/v3/

BASE_URL = "https://api.github.com"
DEFAULT_HEADER = { "Accept": "application/vnd.github.v3+json" }

def fetch_github(m5, url, term):
    t = urllib2.quote(term)
    if '%' in term:
        t = urllib.quote(term.replace('%', ''))

    request = urllib2.Request(url % t, headers=DEFAULT_HEADER)

    try:
        content = json.loads(urllib2.urlopen(request).read())
        return content
    except Exception as e:
        m5.say("An error occurred fetching information from Github: {0}".format(e))
        return None

# Search for repos
def github_search(m5, term):
    search_url = BASE_URL + "/search/repositories?q=%s"

    content = fetch_github(m5, search_url, term)
    if content is None: return

    if "items" in content:
        # Take no more than 5 entries
        list_names = min(len(content["items"]), 5)
        full_names = ", ".join([ x["full_name"] for x in content["items"][:5] ])
        m5.say("Top {0} results: {1}".format(list_names, full_names))
    else:
        m5.say("Couldn't find any repos matching your search term")

# Search for users
def github_user_search(m5, term):
    search_url = BASE_URL + "/search/users?q=%s"

    content = fetch_github(m5, search_url, term)
    if content is None: return

    if "items" in content:
        # Take no more than 5 entries
        list_names = min(len(content["items"]), 5)
        logins = ", ".join([ x["login"] for x in content["items"][:5] ])
        m5.say("Top {0} results: {1}".format(list_names, logins))
    else:
        m5.say("Couldn't find any users matching your search term")

# List open PRs
def github_prs(m5, project):
    pr_url = BASE_URL + "/repos/%s/pulls"

    content = fetch_github(m5, pr_url, project)
    if content is None: return

    num_pulls = len(content)

    m5.say("{0} has {1} open PRs".format(project, num_pulls))
    if num_pulls > 0:
        list_pulls = min(num_pulls, 5)
        titles = ", ".join([ x["title"] for x in content[:5] ])
        m5.say("Latest {0} PRs: {1}".format(list_pulls, titles))

# User info
def github_user(m5, login):
    user_url = BASE_URL + "/users/%s"

    content = fetch_github(m5, user_url, login)
    if content is None: return

    if "login" not in content:
      msg = "An error occurred fetching user info"
      if "message" in content:
        msg += ": {0}".format(content["message"])
      m5.say(msg)
      return

    user_info = "Login: {0}; Member since: {1}; Name: {2}; Public repos: {3}; Followers: {4}".format(content["login"], content["created_at"], content["name"], content["public_repos"], content["followers"])
    if "company" in content and len(content["company"]) > 0:
      user_info += "; Company: {0}".format(content["company"])

    if "blog" in content and len(content["blog"]) > 0:
      user_info += "; Blog: {0}".format(content["blog"])

    if "location" in content and len(content["location"]) > 0:
      user_info += "; Location: {0}".format(content["location"])

    if "hireable" in content and content["hireable"] is not None:
      user_info += "; Available for hire: {0}".format(content["hireable"])

    m5.say(user_info)

# Contributors to a repo
def github_contribs(m5, project):
    contrib_url = BASE_URL + "/repos/%s/contributors"

    content = fetch_github(m5, contrib_url, project)
    if content is None: return

    num_contribs = len(content)

    m5.say("This repo has {0} contributors".format(num_contribs))
    if num_contribs > 0:
        list_contribs = min(num_contribs, 5)
        contribs = ", ".join([ "{0} ({1} contributions)".format(x["login"], x["contributions"]) for x in content[:5] ])
        m5.say("Top {0} contributors: {1}".format(list_contribs, contribs))

# m5 commands start here
def gh_search(m5, input):
    origterm = input.groups()[1]
    if not origterm:
        return m5.say('Perhaps you meant ".github_search repo"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_search(m5, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_search.commands = ['github_search']
gh_search.priority = 'low'
gh_search.rate = 10

def gh_user_search(m5, input):
    origterm = input.groups()[1]
    if not origterm:
        return m5.say('Perhaps you meant ".github_user_search user"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_user_search(m5, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_user_search.commands = ['github_user_search']
gh_user_search.priority = 'low'
gh_user_search.rate = 10

def gh_user_info(m5, input):
    origterm = input.groups()[1]
    if not origterm:
        return m5.say('Perhaps you meant ".github_user_info user"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_user(m5, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_user_info.commands = ['github_user_info']
gh_user_info.priority = 'low'
gh_user_info.rate = 10

def gh_prs(m5, input):
    origterm = input.groups()[1]
    if not origterm:
        return m5.say('Perhaps you meant ".github_prs user/repo"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_prs(m5, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_prs.commands = ['github_prs']
gh_prs.priority = 'low'
gh_prs.rate = 10

def gh_contribs(m5, input):
    origterm = input.groups()[1]
    if not origterm:
        return m5.say('Perhaps you meant ".github_contribs user/repo"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_contribs(m5, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_contribs.commands = ['github_contribs']
gh_contribs.priority = 'low'
gh_contribs.rate = 10

if __name__ == '__main__':
    print __doc__.strip()
