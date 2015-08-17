from django.db import IntegrityError, transaction
from django.utils.decorators import method_decorator


class BatchHelper(object):

    @method_decorator(transaction.atomic)
    def batchitem_transaction(self, batch_items):
        for item in batch_items:
            try:
                item.save()
            except IntegrityError:
                print("Integrity Error")
