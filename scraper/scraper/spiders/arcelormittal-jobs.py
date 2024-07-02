import os
import time

import scrapy
from scrapy.spiders import Rule, CrawlSpider, Spider
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup

from utils import make_safe_filename


class MycrawlerSpider(Spider):
    name = "arcelormittal-jobs"
    allowed_domains = ["emfg.fa.em4.oraclecloud.com"]
    job_result_url = (
        'https://emfg.fa.em4.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData'
        '=true&expand=requisitionList.secondaryLocations,'
        'flexFieldsFacet.values&finder=findReqs;siteNumber=CX_4001,'
        'facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS'
        '%3BPOSTING_DATES%3BFLEX_FIELDS,limit={limit},locationId=300000000314799,sortBy=POSTING_DATES_DESC,'
        'offset={offset}'
    )
    job_page_url = 'https://emfg.fa.em4.oraclecloud.com/hcmUI/CandidateExperience/nl/sites/CX_4001/job/{job_id}/'
    job_page_url = ('https://emfg.fa.em4.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails'
                    '?finder=ById;Id=%22{job_id}%22')
    limit = 100

    def __init__(self):
        # create the data/jobs directory if it does not exist
        if not os.path.exists('data/jobs'):
            os.makedirs('data/jobs')

        # remove all files in the data/jobs directory
        for file in os.listdir('data/jobs'):
            os.remove(f'data/jobs/{file}')
        self.offset = 0
        super().__init__()

    def start_requests(self):
        first_results_page_url = self.job_result_url.format(limit=self.limit, offset=self.offset)
        self.logger.debug(f'First page: {first_results_page_url}')
        yield scrapy.Request(url=first_results_page_url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        json_response = response.json()
        job_list = json_response.get("items")[0].get('requisitionList', [])
        self.logger.debug(f'{len(job_list)} jobs on this page')
        if job_list:
            self.offset += self.limit
            next_results_page_url = self.job_result_url.format(limit=self.limit, offset=self.offset)
            self.logger.debug(f'Next page: {next_results_page_url}')
            yield scrapy.Request(url=next_results_page_url, callback=self.parse_result_page)
        for job in job_list:
            job_id = job.get('Id')
            jub_url = self.job_page_url.format(job_id=job_id)
            yield scrapy.Request(url=jub_url, callback=self.parse_job_page)


    def parse_job_page(self, response):
        response_json = response.json()
        items = response_json.get('items', [])
        if not items:
            self.logger.warning(f'No items in {response.url}')
            return
        id_ = items[0].get('Id', '')
        title = items[0].get('Title', '')
        category = items[0].get('Category', '')
        location = items[0].get('PrimaryLocation', '')
        description = items[0].get('ExternalDescriptionStr', '')
        if not title or not description or not id_:
            self.logger.warning(f'no id, title or description for {response.url}')

        description_soup = BeautifulSoup(description, 'html.parser')

        description_without_tags = description_soup.get_text()
        description_without_tags = description_without_tags.replace(' ', ' ')

        content = f"""# Job: {title}
## Category: 
{category}
## Location: 
{location}
## Description:
{description_without_tags}
"""

        filename = make_safe_filename(f'{id_}--{title}.md')
        with open(f'data/jobs/{filename}', 'w', encoding='utf-8') as file:
            file.write(content)
            self.logger.info(f'Saved {filename}')
