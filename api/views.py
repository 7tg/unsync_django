from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pprint
import datetime
from unsync import unsync
from functools import reduce


URL = "http://univ.cc/search.php?dom=world&key=&start="
HEADERS = {'User-Agent': 'Mozilla/5.0'}


@unsync
async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            return await resp.text()

@unsync
async def get_link_data(url, page_count):
    response = await get_html(url)
    soup = BeautifulSoup(response, 'html.parser')
    links = []
    for link in soup.find("ol", {"start": page_count}).find_all('a', href=True):
      links.append(str(link.get_text())+','+link['href'])
    
    return links

class ParseView(APIView):

    def get(self, request):
        start_time = datetime.datetime.now()

        stock_list = []

        tasks = []
        for page_number in range(1, 7500, 50):
            tasks.append(get_link_data(
                URL + str(page_number),
                page_number
            ))

        results = [task.result() for task in tasks]

        results = reduce(lambda x, y: x + y, results)

        response = {
            "status": "okey",
            "duration": datetime.datetime.now() - start_time,
            "results": results
        }
        return Response(response)
