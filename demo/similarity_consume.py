#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 21-04-09
# @Author  : tiankang

import json
import logging
import re
import sys
import time
import datetime
from uuid import uuid1
from functools import reduce

import redis
import pymysql
import jieba
from gensim import corpora, models, similarities
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from pymysql.err import IntegrityError


class SimilarityConsume:

    MYSQL_ASSET_TEST = {
        'host': '172.18.255.8',
        'port': 3306,
        'database': 'asset_test',
        'user': 'asset',
        'password': 'Youcheng2017!',
    }
    ONLINE_REDIS_PARAM = {
        "host": '172.18.255.7',
        "password": 'youcheng7347'
    }
    KAFKA_SOCK = ['172.18.255.9:9092', '172.18.255.9:9093', '172.18.255.9:9094']

    def __init__(self):
        # topic
        self.topic_name = 'auction_similary_test'
        self.tagname = 'auction_similary_tag_ids_test'
        self.dictionary_path = 'deerwester_test.dict'
        # mysql
        self.conn = pymysql.Connect(**self.MYSQL_ASSET_TEST)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        # redis
        self.redis_conn = redis.Redis(**self.ONLINE_REDIS_PARAM)
        self.redis_key = 'auction_similary:' + self.topic_name
        date_str = str(datetime.date.today())
        self.redis_tag_key = self.tagname + ':' + date_str
        # kafka
        self.consumer = KafkaConsumer(group_id='group_similary', bootstrap_servers=self.KAFKA_SOCK)
        self.partition = TopicPartition(topic=self.topic_name, partition=0)
        self.consumer.assign([self.partition])
        self.record_one_day = True
        self.SOURCE_ID_LIMIT = (1, 3, 4, 5, 6, 10857, 10873)
        # 日志
        logging.warning('{} {}'.format(self.get_now_datetime('%Y-%m-%d %H:%M:%S'), '源诚相似度分析v1.6'))

    def query_price_limit(self):
        """
        获取动态配置的限制参数，符合条件的才做结构化和相似判断
        """
        sql = 'select * from `lab_model_auction_extract_base_config` where `id` = 1'
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res

    @staticmethod
    def format_company(name):
        """解决有多个括号的情况，替换()为（）"""
        name = name.replace('(', '（').replace(')', '）')
        return re.sub('（[^（]*?）$', '', name)

    @staticmethod
    def create_docs(res_list):
        all_doc = []
        for doc in res_list:
            all_doc.append(doc['title'].strip())
        all_doc_list = []
        for doc in all_doc:
            doc_list = [word for word in jieba.cut(doc)]
            all_doc_list.append(doc_list)
        return all_doc_list

    @staticmethod
    def gen_guid():
        return str(uuid1())

    def pre_process(self, res_list):
        trip_round_res_list = [{'id': res['auction_id'], 'title': res['title'][(res['title'].find('】') + 1 if (
                res['title'] and res['title'][0] == '【' and res['title'].find('】') != -1) else 0):]} for res in
                               res_list]
        new_trip_round_res_list = [{'id': res['id'], 'title': res['title'][(res['title'].find(
            ')') + 1 if (res['title'] and res['title'][0] == '(' and res['title'].find(')') != -1) else 0):]} for res in
                                   trip_round_res_list]
        return new_trip_round_res_list

    def similarity(self, similary_rate, topic_name_, redis_key_):
        """
        文本相似度分析，从拍卖物中取前n条数据，在中间找出相似度大于制定比率的拍卖物id
        """
        auction_list = []
        new_trip_round_res_list = []
        total_sims_ = []
        dictionary = corpora.Dictionary()
        price_limit = self.query_price_limit()
        record_date = self.get_now_datetime()

        # 偏移之前必须获取一下所有topics
        logging.warning('Use topic: %s' % topic_name_)
        logging.warning(self.consumer.end_offsets([TopicPartition(topic=topic_name_, partition=0)]))
        offset_dict = self.redis_conn.hgetall(redis_key_)

        # 之前是取前一天的offset，如果前天系统异常，没有存储，会导致取不到值的报错。
        if offset_dict:
            last_day = max(map(lambda x: x.decode(), offset_dict.keys()))
            offset = int(self.redis_conn.hget(redis_key_, last_day).decode()) - 100
            act_off = offset if offset and offset > 0 else 0
        else:
            act_off = 0
        logging.warning('Start with offset: %s' % act_off)
        self.consumer.seek(self.partition, act_off)

        count = 0
        for msg in self.consumer:
            try:
                length = 0 if len(total_sims_) < 1 else reduce(lambda a, b: a + b, map(lambda c: len(c), total_sims_))
                logging.warning('{} {}'.format(self.get_now_datetime('%Y-%m-%d %H:%M:%S'),
                                               '--------------------msg.offset:{} - similary.groups:{} - similary.length:{}'
                                               '-------------------------'.format(msg.offset, len(total_sims_),
                                                                                  length)))
                demo = self.just_for_count_time(msg, record_date, auction_list, new_trip_round_res_list,
                                           dictionary, similary_rate, count, total_sims_, redis_key_, price_limit)
                if demo:
                    record_date, auction_list, new_trip_round_res_list, dictionary, similary_rate, count, \
                    total_sims_, redis_key_, price_limit = demo

            except Exception as e:
                logging.warning('ERROR: {}'.format(e))

    def just_for_count_time(self, msg, record_date, auction_list, new_trip_round_res_list, dictionary,
                            similary_rate, count, total_sims_, redis_key_, price_limit):
        """
        处理单独的数据，进行相似的判断，去重，合并
        """
        recv = json.loads(msg.value.decode(), strict=False)
        print(recv)
        recv['title'] = re.sub('拍品号【.*?】', '', recv['title'])
        recv['title'] = re.sub('、', '', recv['title'])
        recv['title'] = self.format_company(recv['title'])
        logging.warning(recv)
        now_date = self.get_now_datetime()

        # 当第二天时会退出该系统并记录这时的偏移量，pm2负责自动重启
        if record_date != now_date:
            self.redis_conn.hset(redis_key_, now_date, msg.offset)
            dictionary.save(self.dictionary_path)
            if self.record_one_day:
                sys.exit()

        # 判断相似前的过滤条件
        current_price = recv['current_price']
        source_id = recv['source_id']
        category = recv['category']
        if current_price < price_limit['current_price'] * 10000 or int(
                source_id) not in self.SOURCE_ID_LIMIT or category in (56956002, 50025972):
            return None

        self.conn.ping(reconnect=True)
        doc = self.pre_process([recv])[0]
        if re.search(r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼澳]·?[A-Z][A-Z0-9]{4,5}', doc['title']):
            return
        elif len(doc['title']) <= 2:
            return
        auction_list.append(recv)

        # 预处理
        trip_res = self.pre_process([recv])
        new_trip_round_res_list.extend(trip_res)
        # 从记录id和title的new_trip_round_res_list删除以标记的id
        tag_id_list = self.redis_conn.lrange(self.redis_tag_key, 0, -1)
        tag_id_list = [int(i) for i in tag_id_list]
        new_trip_round_res_list = list(filter(lambda x: x['id'] not in tag_id_list, new_trip_round_res_list))
        # 生成文档建立模型
        doc_ = self.create_docs(trip_res)
        dictionary.add_documents(doc_)
        corpus = [dictionary.doc2bow(self.create_docs([i])[0]) for i in new_trip_round_res_list]

        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=800)
        index_similar = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))

        doc_test_list = doc_[0]
        doc_test_vec = dictionary.doc2bow(doc_test_list)
        sims = index_similar[lsi[doc_test_vec]]
        last_sim = sorted(enumerate(sims), key=lambda sim_: -sim_[1])  # 按相似分数排序

        sims_ = []
        for sim in last_sim:
            # 2018-11-28，不是同一法院不会算作同类。
            if round(sim[1], 2) >= similary_rate and new_trip_round_res_list[sim[0]]['id'] != doc['id'] and \
                    auction_list[sim[0]]['court'] == recv['court']:
                sims_.append((sim, new_trip_round_res_list[sim[0]]))
            elif round(sim[1], 2) < similary_rate:
                # 只有未匹配到相似数据才会将此条标题加入语料库
                # dictionary.add_documents(doc_)
                break

        new_sims = sims_
        if new_sims:
            for single in new_sims:
                guid = single[1].get('sign')
                if guid:
                    break
            else:
                guid = self.gen_guid()
            for single in new_sims:
                sim_ = single[1]
                if not sim_.get('sign'):
                    sim_['sign'] = guid
                    # self.insert_similar_sign_list([sim_['id']], guid)
                    # self.sign_len_increase(guid)
            last_res_list = new_trip_round_res_list[-1]
            if not last_res_list.get('sign'):
                last_res_list['sign'] = guid
                # self.insert_similar_sign_list([doc['id']], guid)
                # self.sign_len_increase(guid)
            # 将自己添加进去
            new_sims.append(((len(new_trip_round_res_list) - 1, 1), new_trip_round_res_list[-1]))
            # 将sign值一样的new_sims合并
            for index, sims_ in enumerate(total_sims_):
                if sims_[0][1]['sign'] == guid:
                    total_sims_[index] = new_sims
                    break
            else:
                total_sims_.append(new_sims)
        # 记录条数
        count += 1
        if count > 2500:
            dictionary = corpora.Dictionary()
            auction_list = []
            new_trip_round_res_list = []
            total_sims_ = []
            count = 0
        return (record_date, auction_list, new_trip_round_res_list, dictionary, similary_rate, count,
                total_sims_, redis_key_, price_limit)

    def main(self):
        self.similarity(0.8, self.topic_name, self.redis_key)

    @staticmethod
    def get_now_datetime(date_format='%Y-%m-%d'):
        return time.strftime(date_format, time.localtime(time.time()))

    def insert_similar_sign_list(self, auction_id_list, sign, insert_once=False):
        """
        一次插入多条版本，会有更新问题，增加参数insert_once=False，默认为分开插入，修复插入重复记录失败问题
        """
        cols = ['id', 'similar_sign']

        if insert_once:
            sql = 'insert into `lab_model_auction_extract_detail`({}) values{}'.format(
                ', '.join([col for col in cols]),
                ', '.join(('({})'.format(', '.join(('%s',) * len(cols))),) * len(auction_id_list))
            )
            values = []
            for id_ in auction_id_list:
                values.extend([id_, sign])
            try:
                self.cursor.execute(sql, values)
                self.conn.commit()
                return 1
            except IntegrityError:
                self.conn.rollback()
                return 2
        else:
            for auction_id in auction_id_list:
                sql = 'insert into `lab_model_auction_extract_detail`({}) values({}) on duplicate key update ' \
                      '`similar_sign` = {}'.format(', '.join([col for col in cols]), ', '.join(('%s',) * len(cols)),
                                                   '%s')
                values = (auction_id, sign, sign)
                try:
                    self.cursor.execute(sql, values)
                    self.conn.commit()
                except IntegrityError:
                    self.conn.rollback()
                    return 2
            return 1

    def sign_len_increase(self, sign):
        res = self.query_sign_record(sign)

        now_time = int(time.time())
        if not res:
            sql = 'insert into `lab_sign_record`(`similar_sign`, `sign_len`,`total_sign`, `create_time`, `update_time`) values({})'.format(
                ', '.join(('%s',) * 5)
            )
            try:
                self.cursor.execute(sql, (sign, 1, 1, now_time, now_time))
                self.conn.commit()
            except:
                self.conn.rollback()
            return
        else:
            sign_len = res['sign_len'] + 1
            total_sign = res['total_sign'] + 1
            sql = 'update `lab_sign_record` set `similar_sign`=%s, `sign_len`= %s,`total_sign`= %s, `create_time`= %s, `update_time`= %s where similar_sign = %s'
            try:
                self.cursor.execute(sql, (sign, sign_len, total_sign, now_time, now_time, sign))
                self.conn.commit()
            except:
                self.conn.rollback()
            return

    def query_sign_record(self, sign):
        sql = 'select similar_sign,sign_len,total_sign from `lab_sign_record` where similar_sign = {}'.format('%s')
        self.cursor.execute(sql, sign)
        res = self.cursor.fetchone()
        return res

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    similarity_consume = SimilarityConsume()
    similarity_consume.main()
