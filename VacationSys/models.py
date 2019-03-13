from django.db import models

# Create your models here.
class Passengersinfo(models.Model):
    passengerid = models.IntegerField(db_column='PassengerId', primary_key=True)  # Field name made lowercase.
    pclass = models.IntegerField(db_column='Pclass')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=10, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    sibsp = models.CharField(db_column='SibSp', max_length=10, blank=True, null=True)  # Field name made lowercase.
    parch = models.CharField(db_column='Parch', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ticket = models.CharField(db_column='Ticket', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fare = models.FloatField(db_column='Fare', blank=True, null=True)  # Field name made lowercase.
    cabin = models.CharField(db_column='Cabin', max_length=50, blank=True, null=True)  # Field name made lowercase.
    embarked = models.CharField(db_column='Embarked', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PassengersInfo'


class typeofvacation(models.Model):
    """
    休假类型表
    存储休假类型及其对应条件,通过个人情况查询得到其休假类型.
    """
    idVacation = models.IntegerField(primary_key=True)
    holiType = models.CharField(max_length=10, verbose_name="请假类型")
    marryOrNot = models.NullBooleanField(verbose_name="婚否")
    sepWithCouple = models.NullBooleanField(verbose_name="两地分居")
    sepWithParent = models.NullBooleanField(verbose_name="与父母异地")
    serMeet10 = models.NullBooleanField(verbose_name="服役满10年")
    serMeet20 = models.NullBooleanField(verbose_name="服役满20年")
    daysOfVacation = models.IntegerField(null=True,verbose_name="假期天数")

    class Meta:
        verbose_name = "休假类型表"
        verbose_name_plural = "休假类型表"
        ordering = ["idVacation"]

    def __str__(self):
        return self.holiType


class holiday(models.Model):
    """
    公休假期表
    存储公休假期日期,每年需更新一次.
    """
    nameOfHoli = models.CharField(max_length=10,blank=True, verbose_name="假期名称")
    dateOfHoli = models.DateField(blank=True, null=True, verbose_name="假期日期")

    class Meta:
        verbose_name = "公休假期表"
        verbose_name_plural = "公休假期表"

    def __str__(self):
        return self.nameOfHoli


class tableofinfo(models.Model):
    """
    请假信息维护表
    根据人员类别不同，记录人员请假相关信息，每年需更新.
    """
    STATUS_CHOICES = (('in', 'IN'), ('out', 'OUT'))

    person = models.OneToOneField('passengersinfo', on_delete=models.CASCADE, primary_key=True) # Modify based on table of name
    daysOfRoad = models.IntegerField(default=0, verbose_name="路途")
    sepWithCouple = models.NullBooleanField(verbose_name="两地分居")
    sepWithParent = models.NullBooleanField(verbose_name="与父母异地")
    holiType = models.ForeignKey("typeofvacation", on_delete=models.CASCADE, verbose_name="休假类型")
    daysLeft = models.IntegerField(default=0, verbose_name="剩余天数")
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='in', verbose_name="在位情况")

    class Meta:
        verbose_name = "请假信息维护表"
        verbose_name_plural = "请假信息维护表"

    def __str__(self):
        return self.person.lastname

    def init_info(**kwargs):
        objs = Passengerinfo.objects.all()
        for obj in objs:
            obj, created = tableofinfo.objects.update_or_create(person=obj)

    def update_or_create(person, holiType=typeofvacation.objects.get(idVacation=11), **kwargs):
        """
        基本情况表、配偶情况表、社会关系情况表发生变化（增加或者删除对象）时，执行此方法。
            当表中存在对象时，执行更新操作；
            当表中不存在对象时，执行创建操作。
        """
        try:
            """
            update information in the table
            """
            obj = tableofinfo.objects.get(person=person)
            # sp_ids = F_配偶情况.objects.all().values('身份号')
        except tableofinfo.DoesNotExist:
            """
            create informantion in the table
            """
            param = {'person':person, 'holiType':holiType}
            param.update(kwargs)
            obj = tableofinfo.objects.create(**param)


class noteforleave(models.Model):
    """
    请假记录表
    记录每次请假信息，自动生成请假时间和销假时间.
    """
    person = models.OneToOneField('PassengersInfo', on_delete=models.CASCADE) # Modify based on table of name
    holiType = models.OneToOneField("TypeOfVacation", on_delete=models.CASCADE, verbose_name="请假类型")
    dateOfStart = models.DateField(blank=True, null=True, verbose_name="开始时间") # 假期开始时间
    dateOfEnd = models.DateField(blank=True, null=True, verbose_name="结束时间")   # 假期结束时间
    destination = models.CharField(max_length=50, null=True, verbose_name="目的地")
    toolOff = models.CharField(max_length=50, null=True, verbose_name="交通工具")
    dateOfAdd = models.DateField(auto_now=False, auto_now_add=True, verbose_name="请假时间")    # 填写请假记录时间
    dateOfCancel = models.DateField(auto_now=True, auto_now_add=False, verbose_name="销假时间") # 删除请假记录时间
    apprFlag = models.NullBooleanField(verbose_name="本级审批情况")
    apprUpperFlag = models.NullBooleanField(verbose_name="上级审批情况")
    contact = models.CharField(max_length=10, null=True, verbose_name="联系人")
    contactPhone = models.CharField(max_length=15, null=True, verbose_name="联系电话")

    class Meta:
        verbose_name = "请假记录表"
        verbose_name_plural = "请假记录表"

    def __str__(self):
        return self.person.lastname
