```mermaid
graph TD;
    Website-->Scrapy_SitemapSpider;
    Job-->Scrapy_Spider;
    Scrapy_SitemapSpider-->Website_Folder;
    Scrapy_Spider-->Job_Folder;
    Website_Folder-->Vector_Store_Loader;
    Job_Folder-->Vector_Store_Loader;
    Vector_Store_Loader-->OpenAi_VectorStore;
    OpenAi_VectorStore-->OpenAi_Assistant;
    OpenAi_Assistant-->Streamlit;
```