import requests
import bs4
import dhooks


siteLink = input("Enter link of page\n")
site = requests.get(siteLink, timeout = 10)
sourceCode = bs4.BeautifulSoup(site.content, "html.parser")

userWebhook = input("Please input your webhook.\n")
userWebhook = userWebhook.split("discordapp")
webhook = userWebhook[0] + "discord" + userWebhook[1]
try:
	webhook = dhooks.Webhook(webhook)
except ValueError as error:
	print(error)
	exit()
	
title = sourceCode.find("title")
logo = sourceCode.find("meta", {"property": "og:image"})
dropDate = sourceCode.find("h1")
itemTitles = sourceCode.find_all("h2", {"class": "item-details-title"})
itemImages = sourceCode.find_all("img", {"class": "prefill-img"})
upvotes = sourceCode.find_all("div", {"class": "progress-bar-success"})
downvotes = sourceCode.find_all("div", {"class": "progress-bar-danger"})
for x in range(len(itemTitles)):

	embed = dhooks.Embed(
			title = itemTitles[x].text,
			description = itemImages[x]['alt'],
			color = 16187677,
			thumbnail_url = "https://www.supremecommunity.com" + itemImages[x]['src']
		)
	embed.set_author(name = dropDate.text)
	embed.set_footer(text = title.text, icon_url = logo['content'])
	embed.add_field(name = "Upvotes", value = upvotes[x].text)
	embed.add_field(name = "Downvotes", value = downvotes[x].text)
	webhook.send(embed = embed, username = "Supreme Community", avatar_url = logo['content'])