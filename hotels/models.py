from django.db import models
import datetime


# 酒店
class Hotel(models.Model):
    id = models.AutoField("id", primary_key=True)
    hotelNo = models.CharField("酒店编号", max_length=100)
    name = models.CharField('酒店名称', max_length=100)
    brand = models.CharField('酒店品牌', max_length=100)
    city = models.CharField("城市", max_length=100)
    addr = models.CharField('酒店地址', max_length=200)

    def __str__(self):
        return self.name

# 房间
class Room(models.Model):
    id = models.AutoField("房间ID", primary_key=True)
    roomNo = models.CharField("房间编号", max_length=100)
    roomType = models.CharField('房间类型', max_length=100)
    title = models.CharField('标题', max_length=100, null=True)
    countsBed = models.IntegerField('床数量', default=0)
    countsBreakfirst = models.IntegerField('早餐数量', default=0)
    isTwoNightsMore = models.BooleanField("是否连住2晚及以上", default=False)
    checkInDate = models.DateField("入住日期", null=True,  default=datetime.date.today)
    checkOutDate = models.DateField("离开日期", null=True,  default=datetime.date.today)
    countsMember = models.IntegerField("入住人数", default=1)
    costPrice = models.FloatField("成本价格", default=0)
    roomSyncTime = models.DateTimeField("酒店同步时间", null=True, auto_now_add=True)
    agent1 = models.CharField("代理商1", max_length=100)
    agent1Price = models.CharField("代理商1价格", max_length=100)
    agent2 = models.CharField("代理商2", max_length=100)
    agent2Price = models.CharField("代理商2价格", max_length=100)
    agentSyncTime = models.DateTimeField("代理商同步时间", null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.roomType

