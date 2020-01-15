# -*- coding: utf-8 -*-

from aio_pika import Message, DeliveryMode, Channel


def create_message(content: bytes) -> Message:
    return Message(
        body=content,
        priority=0,
        delivery_mode=DeliveryMode.PERSISTENT,
        content_encoding="UTF-8",
        content_type="text/plain",
    )


async def send_amqp_message(channel: Channel, content: bytes, routing_key: str) -> None:
    message = create_message(content)
    await channel.default_exchange.publish(message, routing_key=routing_key)
