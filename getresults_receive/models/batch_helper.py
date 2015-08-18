from django.db import IntegrityError, transaction


class BatchError(Exception):
    pass


class BatchHelper(object):

    def __init__(self, batch):
        self.batch = batch

    def add(self, items):
        self.validate_count(items)
        try:
            with transaction.atomic():
                for item in items:
                    item.save()
        except IntegrityError as e:
            raise BatchError(str(e))

    def validate_count(self, items):
        if len(items) != self.batch.item_count:
            raise BatchError('Expected {} items. Got {}'.format(self.batch.item_count, len(items)))
