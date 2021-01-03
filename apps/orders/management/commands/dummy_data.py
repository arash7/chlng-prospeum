import random

from datetime import datetime, date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from django_seed import Seed

from apps.orders.models import Order, OrderContent
from apps.restaurants.models import Restaurant, Food

User = get_user_model()
seeder = Seed.seeder()


class Command(BaseCommand):
    help = 'Pushes unconsumed payments to their corresponding servers'

    def add_arguments(self, parser):
        parser.add_argument('restaurant_ids', nargs='*', type=int)

        parser.add_argument('--orders',
                            dest='orders_count',
                            default=10,
                            help='Number of orders',
                            type=int)

        parser.add_argument('--sd',
                            dest='start_date',
                            help='start range for date of orders')

        parser.add_argument('--ed',
                            dest='end_date',
                            help='end range for date of orders')

    def handle(self, *args, **options):
        # self.stdout.write((' %s [S%s] ' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), options['segment'])).center(120, "="))

        if not options['restaurant_ids']:
            options['restaurant_ids'] = list(Restaurant.objects.filter(is_enable=True).values_list('pk', flat=True))

        try:
            start_date = datetime.strptime(options['sd'], '%Y-%m-%d')
        except:
            start_date = date.today()

        try:
            end_date = datetime.strptime(options['ed'], '%Y-%m-%d')
        except:
            end_date = date.today() + timedelta(days=options['orders_count'])

        delta_days = (end_date - start_date).days
        reservation_dates = [start_date + timedelta(days=i) for i in range(delta_days)]
        food_list = list(Food.objects.all())

        guest_list = list(User.objects.filter(role=User.ROLE_GUEST))
        while len(guest_list) < options['orders_count']:
            try:
                guest = User.objects.create_user(
                    username=seeder.faker.user_name(),
                    address=seeder.faker.address(),
                    first_name=seeder.faker.first_name(),
                    last_name=seeder.faker.last_name(),
                    email=seeder.faker.email(),
                )
            except:
                continue
            guest_list.append(guest)

        for i in range(options['orders_count']):
            order = Order.objects.create(
                guest=guest_list[i],
                restaurant_id=options['restaurant_ids'][i % len(options['restaurant_ids'])],
                reservation_date=reservation_dates[i % len(reservation_dates)],
                is_takeout=seeder.faker.boolean()
            )
            for i in range(random.randint(1, 15)):
                try:
                    OrderContent.objects.create(
                        order=order,
                        food=random.choice(food_list),
                        qty=random.randint(1, 5)
                    )
                except:
                    continue
