import time
import unittest

import redis
from redis import WatchError


class TestRedis(unittest.TestCase):
    r = redis.Redis(host='localhost', port=6379)

    def setUp(self):
        print('setup')

    def tearDown(self):
        print("teardown")

    def test_redis(self):
        print("test")

    def test_string(self):
        """
        redis-command
        get     mget
        set     mset
        exists
        type
        incr    decr    incrby  decrby
        strlen
        getbit  setbit  bitcount
        :return:
        """
        counter_key = 'user_count'
        counter_value = 20
        self.r.set(counter_key, counter_value)

        self.assertEqual(int(self.r.get(counter_key)), counter_value)
        self.assertTrue(self.r.exists(counter_key))
        self.assertEqual(self.r.type(counter_key), b'string')

        self.r.incr(counter_key, 1)
        self.assertEqual(int(self.r.get(counter_key)), counter_value + 1)

        counter_key_2 = 'user_count_2'
        self.r.mset({counter_key: counter_value, counter_key_2: counter_value})
        self.assertEqual(self.r.mget([counter_key, counter_key_2]), [b'20', b'20'])

        self.r.delete(counter_key_2)
        self.assertFalse(self.r.exists(counter_key_2))

    def test_hash(self):
        """
        hset    hmset
        hget    hmget   hgetall
        hincr   hincrby
        hexists     hsetnx
        hdel
        hkeys
        hvals
        hlens
        :return:
        """
        car_key = 'car:0'
        car_value = {b'name': b'mazda', b'price': b'3000', b'country': b'jp'}

        if self.r.exists(car_key):
            self.r.delete(car_key)

        self.r.hset(car_key, b'name', car_value[b'name'])
        self.assertEqual(self.r.hget(car_key, b'name'), b'mazda')

        self.r.hmset(car_key, car_value)
        print('hmget  {}'.format(self.r.hmget(car_key, [b'price', b'country'])))
        self.assertEqual(self.r.hgetall(car_key), car_value)

        self.assertFalse(self.r.hexists(car_key, b'sales'))
        self.r.hsetnx(car_key, b'sales', b'200')
        self.assertTrue(self.r.hexists(car_key, b'sales'))
        self.r.hdel(car_key, b'sales')
        self.assertFalse(self.r.hexists(car_key, b'sales'))

    def test_list(self):
        """
        lpush   rpush
        lpop    rpop
        llen
        lrange
        lrem
        lindex  lset
        ltrim
        linsert
        rpoplpush [src][dst]
        :return:
        """
        lst_key = 'lst_users'
        lst_value = [b'jim', b'peter', b'mary']

        if self.r.exists(lst_key):
            self.r.delete(lst_key)

        self.r.lpush(lst_key, lst_value[0])
        self.r.rpush(lst_key, lst_value[1], lst_value[2])
        self.assertEqual(self.r.lrange(lst_key, 0, -1), lst_value)

        self.r.ltrim(lst_key, 0, 1)
        self.assertEqual(self.r.llen(lst_key), 2)

        self.r.linsert(lst_key, 'after', b'peter', b'mary')
        self.assertEqual(self.r.lrange(lst_key, 0, -1), lst_value)

    def test_set(self):
        """
        sadd
        srem
        smembers    sismbeber
        sdiff   sunion  sinter
        scard
        srandmember
        spop:rand
        :return:
        """
        set_key = "set_player"
        set_value = [b'jim', b'peter', b'mary']

        if self.r.exists(set_key):
            self.r.delete(set_key)

        self.r.sadd(set_key, set_value[0], set_value[1], set_value[2])
        print('members:  {}'.format(self.r.smembers(set_key)))

        self.assertTrue(self.r.sismember(set_key, b'jim'))
        self.assertEqual(self.r.scard(set_key), len(set_value))
        for i in range(10):
            self.assertTrue(self.r.srandmember(set_key) in set_value)

    def test_zset(self):
        """
        zadd
        zcard   zcount  zrank
        zscore
        arange
        zincrby
        zrem
        zinterstore
        :return:
        """

        zset_key = 'scores'
        zset_value = {'jim': 1, 'peter': 3, 'mary': 2}

        if self.r.exists(zset_key):
            self.r.delete(zset_key)

        self.r.zadd(zset_key, zset_value)
        self.assertEqual(self.r.zcard(zset_key), len(zset_value))
        print('member   {}'.format(self.r.zrange(zset_key, 1, -1, desc=True)))
        print('member byscore   {}'
              .format(self.r.zrangebyscore(zset_key, 0, '+inf', withscores=True)))

    def test_session(self):
        """
        pipeline
        multi
        exec
        transcation =True
        watch
        :return:
        """
        users_key = 'users'
        users_value = ['jim', 'peter', 'mary']

        if self.r.exists(users_key):
            self.r.delete(users_key)

        with self.r.pipeline(transaction=True) as p:
            p.multi()
            p.sadd(users_key, users_value[0])
            p.sadd(users_key, users_value[1])
            p.execute()
        self.assertEqual(self.r.scard(users_key), 2)

        count_key = 'user_count:0'
        count_value = 3
        self.r.set(count_key, count_value)
        try:
            with self.r.pipeline(transaction=True) as p:
                p.watch(count_key)
                p.incr(count_key)
                p.multi()
                p.incr(count_key)
                p.execute()
        except WatchError as e:
            print("do nothing on watch error")
        self.assertEqual(int(self.r.get(count_key)), 4)

        with self.r.pipeline(transaction=False) as p:
            p.incr(count_key)
            p.incr(count_key)
            p.execute()
        self.assertEqual(int(self.r.get(count_key)), 6)

    def test_expired(self):
        """
        expire
        ttl
        :return:
        """
        timed_key = 'user_exist:0'
        timed_value = 'jim'
        self.r.set(timed_key, timed_value)
        self.r.expire(timed_key, 5)

        time.sleep(6)
        self.assertFalse(self.r.exists(timed_key))

    def test_sort(self):
        """
        sort
        alpha
        by
        get
        store
        :return:
        """
        lst_key = 'customer'
        lst_value = ['jim', 'peter', 'mary']

        if self.r.exists(lst_key):
            self.r.delete(lst_key)

        self.r.rpush(lst_key, lst_value[0], lst_value[1], lst_value[2])

        print('sort {}'.format(self.r.sort(lst_key, alpha=True)))

        map_score = {'score:jim': 1, 'score:peter': 3, 'score:mary': 5}
        self.r.mset(map_score)

        print('sort by  {}'.format(self.r.sort(lst_key, by='socre:*', get=['score:*', '#']
                                               )))
        #print('result   {}'.format(self.r.hget('result')))

    def test_queue(self):
        """
        lpush
        blpop
        brpop   [key]   [key]   [key]
        :return:
        """

    def test_publish(self):
        """
        publish
        subscribe   psubscribe
        :return:
        """