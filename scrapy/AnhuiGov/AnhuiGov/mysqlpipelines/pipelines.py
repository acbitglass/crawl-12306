from .sql import Sql
from AnhuiGov.items import AnhuigovItem


class AnhuigovPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AnhuigovItem):
            source_url = item['source_url']
            ret = Sql.duplicate(source_url)
            print('ret:', ret)
            if ret == 1:
                print('This message is already exists!')
                pass
            else:
                title = item['title']
                content = item['context']
                source_publish_time = item['source_publish_time']
                info_source = item['info_source']
                source_url = item['source_url']
                Sql.insert_data(title, content, source_publish_time, info_source, source_url)
                print('Start write data:', title)
