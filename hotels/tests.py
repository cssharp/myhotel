from django.test import TestCase
from .models import Hotel, Room


# Create your tests here.
class Demo(TestCase):
    def setUp(self):
        Hotel(
            hotelNo='nick',
            name='nick',
        ).save()
        print('启动')

    def tearDown(self):
        print('释放')

    def test_1_InsertHotel(self):
        Hotel(
            hotelNo='万豪',
            name='明珠',
        ).save()
        self.assertEqual(Hotel.objects.filter(name='明珠').count(), 1, '没有插入成功')

    def test_2_InsertRoom(self):
        ohotel = Hotel.objects.all().first()
        Room(
            roomNo='9998',
            title='名流',
            hotel=ohotel,
        ).save()
        self.assertEqual(Room.objects.filter(roomNo='9998').count(), 1, '没有插入成功')

    def test_3_index(self):
        response = self.client.get('/hotels/')
        self.assertEqual(response.status_code, 200, 'hotels状态码不为200')
