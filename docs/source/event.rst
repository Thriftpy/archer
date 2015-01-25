.. _event:

event
=====

event
-----

.. currentmodule:: archer.event

Event is used to add customized hook functions which would be called
before or after An api calling.

Archer provides 3 events :data:`before_api_call`,  :data:`after_api_call`,
:data:`tear_down_api_call` 

for `after_api_call`,it would take one argument, 
    which is an instance of :class:`~archer.app.ApiMeta`

it receives two arguments, first is instance of
    :class:`~archer.app.ApiMeta` and the second is instance of :class:`~archer.app.ApiResultMeta`.

