# -*- coding: utf-8 -*-

from archer.event import Event
from mock import MagicMock
import pytest


@pytest.fixture
def listener1():
    return MagicMock()


@pytest.fixture
def listener2():
    return MagicMock()


def test_event(listener1, listener2):
    event = Event('event1')
    event.add_listener(listener1)
    event.add_listener(listener2)
    event.notify(1, 2)
    listener1.assert_called_once_with(1, 2)
    listener2.assert_called_once_with(1, 2)


def test_event_is_singleton():
    event = Event('1')
    event1 = Event('1')
    assert event is event1
    event2 = Event('2')
    assert event is not event2


def test_event_target(listener1, listener2):
    event = Event('event2')
    event.add_listener(listener1, target='target1')
    event.notify(1, 2)
    listener1.assert_called_once_with(1, 2)
    with pytest.raises(AssertionError):
        listener2.assert_any_call(1, 2)
    event.add_listener(listener2, target='target1')
    event.notify(1, 2)
    listener2.assert_called_once_with(1, 2)


def test_notify_givent_target(listener1, listener2):
    event = Event('event3')
    event.add_listener(listener1)
    event.add_listener(listener2, target='target2')
    event.notify(1, 2, target='target1')

    with pytest.raises(AssertionError):
        listener1.assert_called_once_with(1, 2)
    with pytest.raises(AssertionError):
        listener2.assert_called_once_with(1, 2)

    event.notify(1, 2, target='target2')
    listener2.assert_called_once_with(1, 2)
    with pytest.raises(AssertionError):
        listener1.assert_called_once_with(1, 2)


def test_notify_none_target_will_notify_all(listener1, listener2):
    event = Event('event3')
    event.add_listener(listener1, target='target1')
    event.add_listener(listener2, target='target2')
    event.notify(1, 2, target=None)
    listener1.assert_called_once_with(1, 2)
    listener2.assert_called_once_with(1, 2)
