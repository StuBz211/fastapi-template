import dramatiq

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from config import settings


rabbitmq_broker = RabbitmqBroker(url=settings.BROKER_URL)
dramatiq.set_broker(rabbitmq_broker)


from worker.tasks import activate_user_message
