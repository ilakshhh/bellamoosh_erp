app_name = "bellamoosh_erp"
app_title = "Bellamoosh ERP"
app_publisher = "Your Company"
app_description = "ERP system for Bellamoosh"
app_email = "your@email.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bellamoosh_erp/css/bellamoosh_erp.css"
# app_include_js = "/assets/bellamoosh_erp/js/bellamoosh_erp.js"

# include js, css files in header of web template
# web_include_css = "/assets/bellamoosh_erp/css/bellamoosh_erp.css"
# web_include_js = "/assets/bellamoosh_erp/js/bellamoosh_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bellamoosh_erp/public/scss/website"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bellamoosh_erp.install.before_install"
# after_install = "bellamoosh_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bellamoosh_erp.install.before_uninstall"
# after_uninstall = "bellamoosh_erp.install.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bellamoosh_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"bellamoosh_erp.tasks.all"
#	],
#	"daily": [
#		"bellamoosh_erp.tasks.daily"
#	],
#	"hourly": [
#		"bellamoosh_erp.tasks.hourly"
#	],
#	"weekly": [
#		"bellamoosh_erp.tasks.weekly"
#	]
#	"monthly": [
#		"bellamoosh_erp.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "bellamoosh_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "bellamoosh_erp.event.get_events"
# }
#
# each overriding function accepts a `data` parameter;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task" : "bellamoosh_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# HTTP request events are bound to this module

# request_events = {
#	"before_request": "bellamoosh_erp.api.before_request",
#	"after_request": "bellamoosh_erp.api.after_request"
# }

# API method
# -----------
# expose functions as API endpoints

# api_endpoint = "bellamoosh_erp.api.endpoint"

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "bellamoosh_erp.utils.jinja_methods",
#	"filters": "bellamoosh_erp.utils.jinja_filters"
# }

# Migration
# ----------

# Specify the version when you want to trigger the migration
# migration = "1.0.0"

# Fixtures
# --------

# fixtures = ["Custom Field", "Property Setter"]

# Authenticate
# ------------

# authenticate = "bellamoosh_erp.authenticate.authenticate"

# OAuth
# -----

# oauth_providers = [
#	{
#		"provider_name": "google",
#		"client_id": "your_client_id",
#		"client_secret": "your_client_secret",
#		"redirect_uri": "your_redirect_uri",
#		"api_endpoint": "https://www.googleapis.com/oauth2/v2/userinfo",
#		"api_endpoint_args": {
#			"access_token": "access_token"
#		},
#		"auth_endpoint": "https://accounts.google.com/o/oauth2/auth",
#		"auth_endpoint_args": {
#			"scope": "openid email profile",
#			"response_type": "code"
#		}
#	}
# ]

# Webhooks
# --------

# webhooks = [
#	{
#		"method": "bellamoosh_erp.api.webhook_handler",
#		"event": "on_update",
#		"doctype": "DocType"
#	}
# ]

# Template
# --------

# template = "bellamoosh_erp.template.template"

# Rate Limit
# -----------

# rate_limit = {
#	"window": 3600,
#	"max": 100
# }

# Email
# -----

# email_append_to = {
#	"Task": ["user@example.com"]
# }

# Email Brand
# ------------

# email_brand = "bellamoosh_erp"

# Push Notification
# -----------------

# push_notification = {
#	"app_name": "Bellamoosh ERP",
#	"api_key": "your_api_key",
#	"api_secret": "your_api_secret"
# }

# Print Format
# ------------

# print_format = "bellamoosh_erp.print_format.print_format"

# Website
# -------

# website_route_rules = [
#	{"from_route": "/bellamoosh_erp/<path:app_path>", "to_route": "bellamoosh_erp"},
# ]

# website_redirects = [
#	{"source": "/old-path", "target": "/new-path"},
# ]

# website_context = {
#	"favicon": "/assets/bellamoosh_erp/images/favicon.ico",
#	"splash_image": "/assets/bellamoosh_erp/images/splash.png"
# }

# Admin
# -----

# admin_include_js = "assets/bellamoosh_erp/js/admin.js"
# admin_include_css = "assets/bellamoosh_erp/css/admin.css"

# Website
# -------

# website_generators = ["Web Page"]

# Search
# ------

# search = "bellamoosh_erp.search.search"

# Patch
# -----

# patch = "bellamoosh_erp.patch.patch"