from django.db import models
from django.urls import reverse


# --------------Модель объекта---------------------------------------
class Vch(models.Model):
    """Модель в\ч"""

    OKRUG_Ch = (
        ('ЦФО', 'ЦФО'),
        ('СЗФО', 'СЗФО'),
        ('ЮФО', 'ЮФО'),
        ('СКФО', 'СКФО'),
        ('ПФО', 'ПФО'),
        ('УрФО', 'УрФО'),
        ('СФО', 'СФО'),
        ('ДФО', 'ДФО'),
    )


    number_vch = models.CharField(max_length=10)                              # № части
    okrug = models.CharField(max_length=5, choices=OKRUG_Ch, default='ЦФО')   # округ
    oblast = models.CharField(max_length=30)                                  # область
    town = models.CharField(max_length=30)                                    # город
    vch_info = models.TextField(default='Контактная информация')              # контакты в свободной форме
    manager = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)
    # описание изделия
    name = models.CharField(max_length=10, null=True, blank=True, default='83т3ХХХ/ХM')  # 83т361/3M
    serial = models.ForeignKey('Sostav', on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(max_length=10)                         # заводской номер
    warranty = models.CharField(max_length=60, default=' не на гарантии, 25 октября 2020')
    izdel_info = models.TextField(default='Дополнительная информация по изделию')


    # описание состава изделия
    # стандарное издели с учетом ЗИП
    server_standart = models.PositiveIntegerField(default=4)            # количество серверов в стандарном изделии
    arm_standart = models.PositiveIntegerField(default=10)              # количество арм в стандарном изделии
    laptop_standart = models.PositiveIntegerField(default=0)            # количество ноутов в стандарном изделии
    switch_standart = models.PositiveIntegerField(default=4)            # количество коммутаторов в стандарном изделии
    supp_standart = models.TextField(default='Периферийные устройства') # переферия в стандартном изделии

    #  доплниетльное оборудование
    server_add = models.PositiveIntegerField(default=0)                 # количество серверов дополнительно
    arm_add = models.PositiveIntegerField(default=0)                    # количество арм дополнительно
    laptop_add = models.PositiveIntegerField(default=0)                 # количество ноутов дополнительно
    switch_add = models.PositiveIntegerField(default=0)                 # количество коммутаторов дополнительно
    supp_add = models.TextField(default='Дополнительная информация')    # переферия дополнительно

    #  итого
    server_total = models.PositiveIntegerField(default=0)  # всего серверов в  изделии
    arm_total = models.PositiveIntegerField(default=0)     # всего арм в  изделии
    switch_total = models.PositiveIntegerField(default=0)  # всего коммутаторов в  изделии
    laptop_total = models.PositiveIntegerField(default=0)  # всего ноутов в  изделии


    class Meta:
        ordering = ['number_vch']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return 'Воинская часть  {0} ,  округ - {1} , изделие - {2}, состав - {3}, зав. номер - {4} , {5}'.format(self.number_vch,
                                                                                                                 self.okrug,
                                                                                                                 self.name,
                                                                                                                 self.serial,
                                                                                                                 self.serial_number,
                                                                                                                 self.manager)

# -------------Модель состава -------------------------------------------
class Sostav(models.Model):
    """Модель состава изделия"""
    sostav_izdelya = models.CharField(max_length=40)     # 83т055.02

    class Meta:
        ordering = ['sostav_izdelya']

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.sostav_izdelya

# -------------Модель сотрудника---------------------------------------------
class Author(models.Model):
    """Модель сотрудника"""
    STATUS_CHOSE = (
        ('менеджер', 'менеджер'),
        ('руководитель', 'руководитель'),
        ('оператор', 'оператор'),

    )
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    login = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOSE, default='менеджер')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1}'.format(self.last_name, self.first_name)

# ---------------------------------------------------------------------



