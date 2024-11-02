import asyncio
import json
import os

import httpx
import jmespath
from DrissionPage._pages.chromium_page import ChromiumPage
from loguru import logger

from utils.csv_utils import write_new_csv_file, append_csv_file
from utils.dp import get_page, record_data


class MainProcess(object):
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.page: ChromiumPage = None

    async def start_dp(self):
        debugger_port = 12345
        self.page = get_page(debugger_port=debugger_port)

    async def handle(self):
        keyword = 'Salwar'
        url = f'https://guide.prod.iam.aha.org/guide/searchResults'
        # self.page.get(url)

        url1 = "https://guide.prod.iam.aha.org/guide/graphql"

        obj_list = []

        btn_xpath = "//a[@class='page-link' and @href='' and text()='Next']"

        url_list = [url1, ]
        page_no = 0

        self.page.listen.start(targets=url_list, is_regex=False)  #
        btn_ele = self.page.ele(f"x:{btn_xpath}")
        btn_ele.click()

        for packet in self.page.listen.steps(count=1):
            #print(packet.url)  # 打印数据包url
            #print(json.dumps(packet.request.postData))
            print(json.dumps(packet.request.postData).split('"pageNum": ')[1].split("}")[0])
            #tmp = json.dumps(packet.request.postData).split("'pageNum': ")[1].split("}")[0]
            #print(tmp)

            file_path = f"data/output/outbound_{page_no}.json"
            record_data(file_path=file_path, data=packet.response.body,
                        is_parse=False)
            logger.debug(f"save file-> {file_path}")

            result = jmespath.search('data.search.result', packet.response.body)
            for i in result:
                ahaId = i.get('ahaId', '')
                resultType = i.get('resultType', '')
                orgDisplayName = i.get('orgDisplayName', '')
                personDisplayName = i.get('personDisplayName', '')
                title = i.get('title', '')
                ahaMember = i.get('ahaMember', '')

                obj_list.append(
                    {
                        "ahaId": ahaId,
                        "resultType": resultType,
                        "orgDisplayName": orgDisplayName,
                        "personDisplayName": personDisplayName,
                        "title": title,
                        "ahaMember": ahaMember,
                    })

            csv_filename = 'data/output/data.csv'
            #print(obj_list)
            # 检查文件是否存在
            if os.path.exists(csv_filename):
                append_csv_file(filename=csv_filename, data_list=obj_list)
            else:
                write_new_csv_file(filename=csv_filename, data_list=obj_list)

    async def run(self):
        await self.start_dp()  # 启动dp框架
        while 1:
            await self.handle()


async def main():
    process = MainProcess()
    await process.run()


def test():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    test()
