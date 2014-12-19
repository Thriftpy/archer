# -*- coding: utf-8 -*-


from archer import Archer

app = Archer(__name__, 'thrift')


@app.api('get')
def get(order_id):
    return order_id

@app.api
def mget(ids):
    raise ValueError("no such id {}".format(ids))


# app.mget(123)
print app.get(12)
