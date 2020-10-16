from flask import Flask, render_template, request
import requests

app = Flask(__name__)

USERNAME_STATUS = {
    "AVAILABLE": "available",
    "NOT_AVAILABLE": "not available",
    "NOT_ALLOWED": "not allowed",
    "COULD_NOT_FIND": "could not find",
}

HTTP_STATUS = {
    "OK": 200,
    "MOVED_PERMANENTLY": 301,
    "METHOD_NOT_ALLOWED": 405,
}

username_availability_on_each_site = {}

sites_with_syntax_domain_username = {
    "twitter": "https://twitter.com/",
    "facebook": "https://facebook.com/",
    "instagram": "https://www.instagram.com/",
    "github": "https://github.com/",
    "gitlab": "https://gitlab.com/",
    "bitbucket": "https://bitbucket.org/",
    # TODO: Add more here.
}

sites_with_syntax_username_dot_domain = {
    "wordpress": ".wordpress.com/",
    # TODO: Add more here.
}


def check_username_availability_on_sites_with_syntax_domain_username(username):
    """
    Function to check for the username availability on those sites that use
    usernames in their URL direcly after their domain as endpoint.

    Valid example: https://github.com/<username>

    Invalid example: https://askubunt.com/users/<userid>/<username>

    :arg username: Username to be search

    :return: None

    """
    for site_name, url in sites_with_syntax_domain_username.items():
        username_availability_on_each_site.update(
            {site_name: USERNAME_STATUS["AVAILABLE"]}
        )
        url = url + username + "/"
        # TODO: Add specific username validation as per the site if required.
        http_response = requests.head(url)
        if (
            http_response.status_code == HTTP_STATUS["METHOD_NOT_ALLOWED"]
            or http_response.status_code == HTTP_STATUS["MOVED_PERMANENTLY"]
        ):
            http_response = requests.get(url)
        if http_response.status_code == HTTP_STATUS["OK"]:
            username_availability_on_each_site.update(
                {site_name: USERNAME_STATUS["NOT_AVAILABLE"]}
            )


def check_username_availability_on_sites_with_syntax_username_dot_domain(username):
    """
    Function to check for the username availability on those sites that use
    usernames in front of their domain as subdomain.

    Valid example: https://<username>.wordpress.com

    Invalid example: https://twitter.com/<username>

    :arg username: Username to be search

    :return: None

    """
    for site_name, url in sites_with_syntax_username_dot_domain.items():
        username_availability_on_each_site.update(
            {site_name: USERNAME_STATUS["AVAILABLE"]}
        )
        url = "https://" + username + url
        # TODO: Add specific username validation as per the site if required.
        http_response = requests.head(url)
        if (
            http_response.status_code == HTTP_STATUS["METHOD_NOT_ALLOWED"]
            or http_response.status_code == HTTP_STATUS["MOVED_PERMANENTLY"]
        ):
            http_response = requests.get(url)
        if http_response.status_code == HTTP_STATUS["OK"]:
            username_availability_on_each_site.update(
                {site_name: USERNAME_STATUS["NOT_AVAILABLE"]}
            )


def check_username_availability(username):
    """
    Function to check the username availability on various groups of websites.

    :arg username: Username to be search

    :returns: None

    """
    # TODO: Add a general function to validate the username.
    check_username_availability_on_sites_with_syntax_domain_username(username)
    check_username_availability_on_sites_with_syntax_username_dot_domain(username)
    # TODO: Add more functions to check the username availability on different
    # groups of websites.


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        username = request.form["username"]
        check_username_availability(username)
        return render_template(
            "index.html",
            results=username_availability_on_each_site,
            username=username,
        )

    return render_template("index.html")
