from django.db import models
from django.urls import reverse

"""
ПРИМЕР ступенчатой модели (решает проблему когда в одном классе необходимо сделать более одного поля ссылающегося на один и тот же класс)

- (добавить в Vch несколько изделий a_type  b_type  c_type которые выбираются  Sostav  )
- если сделать на прямую при миграции выдает ошибку которая обходится создание промежуточных объектов
 
  Vch
  - a_type --> Sostav
  - b_type --> Sostav
  - c_type --> Sostav



- данная ошибка обходится созданием промежуточны объектов

изделие  --> a_type --> Sostav
         --> b_type -->
         --> c_type -->
  
  Vch
  a_type --> Top_Sostav
  b_type --> Middle_Sostav
  c_type --> Low_Sostav
  
 
  Top_Sostav    --> Sostav
  Middle_Sostav --> Sostav
  Low_Sostav    --> Sostav





"""
# --------------Модель объекта---------------------------------------
class Vch(models.Model):
    """Модель ОбЪекта"""

    OKRUG_Ch = (
        ('ЦВО', 'ЦВО'),
        ('ЗВО', 'ЗВО'),
        ('ЮВО', 'ЮВО'),
        ('ВВО', 'ВВО'),
        ('ЦЕНТР', 'ЦЕНТР'),

         )

    manager = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    # manager = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)

    # ============== В\Ч ===============

    number_vch = models.CharField(max_length=10, null=True, blank=True)       # № части
    okrug = models.CharField(max_length=5, choices=OKRUG_Ch, default='ЦВО')    # округ
    oblast = models.CharField(max_length=30, null=True, blank=True)           # область
    town = models.CharField(max_length=30, null=True, blank=True)             # город

    # ============== Контакты ===============

    contact_index = models.PositiveIntegerField(default=10, null=True, blank=True)   # Индекс
    contact_adress = models.CharField(max_length=100, default='Почтовый адрес')
    contact_commander = models.CharField(max_length=60, default='Ф.И.О. Командира')
    tel_commander = models.CharField(max_length=18, null=True, blank=True, default='(xxxx) xx xx xx')
    contact_tech = models.CharField(max_length=60, null=True, blank=True, default='Ф.И.О. Зам. по тех.')
    tel_tech = models.CharField(max_length=18, null=True, blank=True, default='(xxxx) xx xx xx')
    contact_asy = models.CharField(max_length=60, null=True, blank=True, default='Ф.И.О. автоматизатора')
    tel_asy = models.CharField(max_length=18, null=True, blank=True, default='(xxxx) xx xx xx')
    contact_curator = models.CharField(max_length=60, null=True, blank=True, default='Ф.И.О.ответсвенного в 61535')
    tel_curator = models.CharField(max_length=18, null=True, blank=True, default='(xxxx) xx xx xx')
    vch_info = models.TextField(default='Контактная информация')              # контакты в свободной форме

    # ============== Описание изделия ==============

    name = models.CharField(max_length=10, null=True, blank=True, default='83т3ХХХ/ХM')  # 83т361/3M
    a_type = models.ForeignKey('Top_Sostav', on_delete=models.CASCADE, null=True, blank=True)
    a_serial_number = models.CharField(max_length=10, null=True, blank=True, default='Mxxx-xxxxx')
    a_year_born = models.DateField(null=True, blank=True)
    a_warranty = models.DateField('не на гарантии', null=True, blank=True)
    b_type = models.ForeignKey('Middle_Sostav', on_delete=models.CASCADE,  null=True, blank=True)
    b_serial_number = models.CharField(max_length=10, null=True, blank=True, default='Mxxx-xxxxx')
    b_year_born = models.DateField(null=True, blank=True)
    b_warranty = models.DateField('не на гарантии', null=True, blank=True)
    c_type = models.ForeignKey('Low_Sostav', on_delete=models.CASCADE,  null=True, blank=True)
    c_serial_number = models.CharField(max_length=10, null=True, blank=True, default='Mxxx-xxxxx')
    c_year_born = models.DateField(null=True, blank=True)
    c_warranty = models.DateField('не на гарантии', null=True, blank=True)

    # ============== контракты ==============
    contract_name = models.ForeignKey('Contract', on_delete=models.CASCADE, null=True, blank=True)
    contract_doc = models.CharField(max_length=10,null=True, blank=True, default='Акт')
    contract_act = models.DateField('акт не подписан', null=True, blank=True)

    izdel_info = models.TextField(default='Дополнительная информация по изделию')


    # ============== описание состава изделия ==============
    # ============== дополниетельное оборудование ==============
    server_add = models.PositiveIntegerField(default=0)                 # количество серверов дополнительно
    arm_add = models.PositiveIntegerField(default=0)                    # количество арм дополнительно
    laptop_add = models.PositiveIntegerField(default=0)                 # количество ноутов дополнительно
    switch_add = models.PositiveIntegerField(default=0)                 # количество коммутаторов дополнительно
    printer_a3_add = models.PositiveIntegerField(default=0)
    printer_a4_add = models.PositiveIntegerField(default=0)
    scanner_add = models.PositiveIntegerField(default=0)
    copir_add = models.PositiveIntegerField(default=0)
    ups_server_add = models.PositiveIntegerField(default=0)
    ups_arm_big_add = models.PositiveIntegerField(default=0)
    ups_arm_small_add = models.PositiveIntegerField(default=0)
    air_conditioner_add = models.PositiveIntegerField(default=0)
    indicator_add = models.PositiveIntegerField(default=0)
    block_679_add = models.PositiveIntegerField(default=0)
    block_680_add = models.PositiveIntegerField(default=0)
    block_683_add = models.PositiveIntegerField(default=0)
    block_689_add = models.PositiveIntegerField(default=0)
    soft_add = models.CharField(max_length=10, null=True, blank=True, default='ДМххх')

    # ============== итого ==============
    server_total = models.PositiveIntegerField(default=0)  # всего серверов в  изделии
    arm_total = models.PositiveIntegerField(default=0)     # всего арм в  изделии
    switch_total = models.PositiveIntegerField(default=0)  # всего коммутаторов в  изделии
    laptop_total = models.PositiveIntegerField(default=0)  # всего ноутов в  изделии
    printer_a3_total = models.PositiveIntegerField(default=0)
    printer_a4_total = models.PositiveIntegerField(default=0)
    scanner_total = models.PositiveIntegerField(default=0)
    copir_total = models.PositiveIntegerField(default=0)
    ups_server_total = models.PositiveIntegerField(default=0)
    ups_arm_big_total = models.PositiveIntegerField(default=0)
    ups_arm_small_total = models.PositiveIntegerField(default=0)
    air_conditioner_total = models.PositiveIntegerField(default=0)
    indicator_total = models.PositiveIntegerField(default=0)
    block_679_total = models.PositiveIntegerField(default=0)
    block_680_total = models.PositiveIntegerField(default=0)
    block_683_total = models.PositiveIntegerField(default=0)
    block_689_total = models.PositiveIntegerField(default=0)
    soft_total = models.CharField(max_length=10, null=True, blank=True, default='ДМххх')

    supp_standart = models.TextField(default='Периферийные устройства')  # переферия в стандартном изделии


    class Meta:
        ordering = ['number_vch']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return 'Воинская часть  {0} ,  округ - {1} , изделие - {2}, {3}'.format(self.number_vch,
                                                                                self.okrug,
                                                                                self.name,
                                                                                self.manager)

# -------------Модель состава -------------------------------------------


class Sostav(models.Model):
    """Модель состава изделия"""
    sostav_izdelya = models.CharField(max_length=40)     # 83т055.02

    server = models.PositiveIntegerField(default=0)  # количество серверов в стандарном изделии
    arm = models.PositiveIntegerField(default=0)    # количество арм в стандарном изделии
    laptop = models.PositiveIntegerField(default=0)  # количество ноутов в стандарном изделии
    switch = models.PositiveIntegerField(default=0)  # количество коммутаторов в стандарном изделии
    printer_a3 = models.PositiveIntegerField(default=0)
    printer_a4 = models.PositiveIntegerField(default=0)
    scanner = models.PositiveIntegerField(default=0)
    copir = models.PositiveIntegerField(default=0)
    ups_server = models.PositiveIntegerField(default=0)
    ups_arm_big = models.PositiveIntegerField(default=0)
    ups_arm_small = models.PositiveIntegerField(default=0)
    air_conditioner = models.PositiveIntegerField(default=0)
    indicator = models.PositiveIntegerField(default=0)
    block_679 = models.PositiveIntegerField(default=0)
    block_680 = models.PositiveIntegerField(default=0)
    block_683 = models.PositiveIntegerField(default=0)
    block_689 = models.PositiveIntegerField(default=0)
    soft = models.CharField(max_length=10, null=True, blank=True, default='ДМххх')


    class Meta:
        ordering = ['sostav_izdelya']

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.sostav_izdelya


# --------------Модель Контракта--------------------------------------

class Contract(models.Model):
    """Модель контракта"""
    contract_name = models.CharField(max_length=40)
    contract_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['contract_name']

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return 'Контракт  {0} ,  дата подписания  - {1}  '.format(self.contract_name, self.contract_date)

# -------------Модель TOP, Middle, Low состава ------------------------

class Top_Sostav(models.Model):
    top_name = models.ForeignKey('Sostav', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['top_name']

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}  '.format(self.top_name)


class Middle_Sostav(models.Model):
    middle_name = models.ForeignKey('Sostav', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['middle_name']


    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}  '.format(self.middle_name)


class Low_Sostav(models.Model):
    low_name = models.ForeignKey('Sostav', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['low_name']

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}  '.format(self.low_name)

# ----------------------------------------------------