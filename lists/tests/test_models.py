from django.test import TestCase
from lists.models import Item,List
from django.core.exceptions import ValidationError

class ListAndItemModelsTest(TestCase):
        def test_saving_and_retrieving_items(self):
            list_=List.objects.create()

            first_item=Item.objects.create(text='The first (ever) list item',list=list_)
            second_item=Item.objects.create(text='Item the second',list=list_)

            saved_list=List.objects.first()
            self.assertEqual(saved_list,list_)

            saved_items=Item.objects.all()
            self.assertEqual(saved_items.count(),2)

            first_item_saved=saved_items[0]
            second_item_saved=saved_items[1]
            self.assertEqual('The first (ever) list item',first_item_saved.text)
            self.assertEqual('Item the second',second_item_saved.text)
            self.assertEqual(first_item_saved.list,list_)
            self.assertEqual(second_item_saved.list,list_)

        def test_cannot_save_empty_list_items(self):
            list_=List.objects.create()
            item=Item(list=list_,text='')
            with self.assertRaises(ValidationError):
                item.save()
                item.full_clean()