	Test fixture
	Test fixture – обеспечивает подготовку окружения для выполнения тестов, а также
организацию мероприятий по их корректному завершению (например очистка
ресурсов). Подготовка окружения может включать в себя создание баз данных, запуск
необходим серверов и т.п.

	Test case
	Test case – это элементарная единица тестирования, в рамках которой
проверяется работа компонента тестируемой программы (метод, класс, поведение и
т.п). Для реализации этой сущности используется класс TestCase .

	Test suite
	Test suite – это коллекция тестов, которая может в себя включать как отдельные
test case’ы так и целые коллекции (т.е. можно создавать коллекции коллекций).
Коллекции используются с целью объединения тестов для совместного запуска.

	Test runner
	Test runner – это компонент, который оркестрирует (координирует
взаимодействие) запуск тестов и предоставляет пользователю результат их
выполнения. Test runner может иметь графический интерфейс, текстовый интерфейс
или возвращать какое-то заранее заданное значение, которое будет описывать
результат прохождения тестов.

	Запуск тестов

Интерфейс командной строки ( CLI )

CLI позволяет запускать группы тесты из модуля или класса, а также
обеспечивает доступ к каждому тесту по отдельности.

	Запуск всех тестов в модуле utest_calc.py .
> python -m unittest test_calc.py

	Запуск тестов из класса CalcTest .
> python -m unittest utest_calc.CalcTest

	Запуск теста test_sub() .
> python -m unittest utest_calc.CalcTest.test_sub

	Для вывода подробной информации
необходимо добавить ключ -v .
> python -m unittest -v utest_calc.py

	Если осуществить запуск без указания модуля с тестами, то будет запущен Test
Discovery , который проведет определенную работу по выполнению тестов.
> python -m unittest


Графический интерфейс пользователя ( GUI 

> pip install cricket

Для запуска тестов в данном приложении, перейдите в каталог с вашим
тестирующим кодом и в командной строке запустите cricket-unittest , для этого просто
наберите название программы и нажмите Enter .
> cricket-unittest

----------------------
import unittest
import calc

class CalcTests ( unittest.TestCase ):
    def test_add ( self ):
        self .assertEqual(calc.add( 1 , 2 ), 3 )
-----------------
При выборе имени класса наследника от TestCase можете руководствоваться
следующим правилом:
[ИмяТестируемойСущности]Tests.
[ИмяТестируемойСущности] – это некоторая логическая единица, тесты для которой
нужно написать. В нашем случае – это калькулятор, CalcTests.

Для того, чтобы метод класса выполнялся как тест, необходимо, чтобы он
начинался со слова test
имена тестов будем начинать с префикса test_  - test_add


	методы класса TestCase можно разделить на три группы:
● методы, используемые при запуске тестов;
● методы, используемые при непосредственном написании тестов (проверка условий, сообщение об ошибках);
● методы, позволяющие собирать информацию о самом тесте.


		● методы, используемые при запуске тестов;

setUp() - Метод вызывается перед запуском теста. Как правило, используется для
подготовки окружения для теста.

tearDown() - Метод вызывается после завершения работы теста. Используется для “приборки”
за тестом.

setUpClass() - Метод действует на уровне класса, т.е. выполняется перед запуском тестов
класса. При этом синтаксис требует наличие декоратора @classmethod .
@classmethod
def setUpClass ( cls ):
...

tearDownClass() - Запускается после выполнения всех тестов класса, 
требует наличия декоратора @classmethod .
@classmethod
def tearDownClass ( cls ):
...

skipTest(reason) - Данный метод может быть использован для пропуска теста, если это
необходимо


		● методы, используемые при непосредственном написании тестов;

Метод 			Проверяемое условие
assertEqual     (a, b) a == b
assertNotEqual  (a, b) a != b



		● методы, позволяющие собирать информацию о самом тесте.

countTestCases()    Возвращает количество тестов в объекте класса-наследника от TestCase .
id() 			    Возвращает строковый идентификатор теста. Как правило это полное имя
	 			    метода, включающее имя модуля и имя класса.
shortDescription()  Возвращает описание теста, которое представляет собой первую строку
					docstring’а метода, если его нет, то возвращает None .

utest_calc_2.py


Организация тестов (класс TestSuite ). Загрузка и запуск тестов

Класс TestSuite - используется для объединения тестов в группы, которые могут
                  включать в себя как отдельные тесты так и заранее созданные группы. Помимо этого,
				  TestSuite предоставляет интерфейс, позволяющий TestRunner’у, запускать тесты.

addTest(test)   - Добавляет TestCase или TestSuite в группу.
addTests(tests) - Добавляет все TestCase и TestSuite объекты в группу, итеративно проходя по
				  элементам переменной tests .
run(result)     - Запускает тесты из данной группы.
countTestCases()- Возвращает количество тестов в данной группе (включает в себя как отдельные
				  тесты, так и подгруппы).

ПРИМЕР:
	В качестве кода, который нужно протестировать, возьмем уже знакомый нам
модуль calc.py
	За основу модуля с тестами примем тот, что приведен в конце первой главы
( calc_tests.py ).
	Для запуска тестов test_runner.py

	Все модули должны находиться в одном каталоге. Для запуска тестов используйте команду:
>python test_runner.py

count of tests: 6
test_add (calc_tests.CalcBasicTests) ... ok
test_div (calc_tests.CalcBasicTests) ... ok
test_mul (calc_tests.CalcBasicTests) ... ok
test_sub (calc_tests.CalcBasicTests) ... ok
test_pow (calc_tests.CalcExTests) ... ok
test_sqrt (calc_tests.CalcExTests) ... ok
-------------------------------------------------------------------
Ran 6 tests in 0.000s
OK


-------------------------------------------------------------------
Загрузка и запуск тестов

TestLoader - класс используется для создания групп из
			 классов и модулей. 
			 методы:
loadTestsFromTestCase(testCaseClass), возвращающий группу со всеми тестами из
			класса testCaseClass . (под тестом понимается метод, начинающийся
со слова “ test ”. Используя этот l oadTestsFromTestCase, можно создать список групп
тестов, где каждая группа создается на базе классов-наследников от TestCase,
объединенных предварительно в список. 

test_runner_2.py

loadTestsFromModule(module, pattern=None)
	Загружает все тесты из модуля module . Если модуль поддерживает l oad_tests
	протокол, то будет вызвана соответствующая функция модуля и ей будет передан в
	качестве аргумента (третьим по счету) параметр pattern .
loadTestsFromName(name, module=None)
	Загружает тесты в соответствии с параметром name . Параметр name – это имя,
	разделенное точками. С помощью этого имени указывается уровень, начиная с
	которого будут добавляться тесты.
getTestCaseNames(testCaseClass)
	Возвращает список имен методов-тестов из класса testCaseClass .

test_runner_3.py

>python test_runner_3.py


test_add (calc_tests.CalcBasicTests) ... ok
test_div (calc_tests.CalcBasicTests) ... ok
test_mul (calc_tests.CalcBasicTests) ... ok
test_sub (calc_tests.CalcBasicTests) ... ok
test_pow (calc_tests.CalcExTests) ... ok
test_sqrt (calc_tests.CalcExTests) ... ok
-------------------------------------------------------------------
Ran 6 tests in 0.016s
OK

Если в модуле test_runner_3.py заменить строку
suites = testLoad.loadTestsFromModule(calc_tests)
на
suites = testLoad.loadTestsFromName(“calc_tests.CalcBasicTests”)
то будут выполнены только тесты из класса CalcBasicTests .
test_add (calc_tests.CalcBasicTests) ... ok
test_div (calc_tests.CalcBasicTests) ... ok
test_mul (calc_tests.CalcBasicTests) ... ok
test_sub (calc_tests.CalcBasicTests) ... ok
----------------------------------------------------------------------
Ran 4 tests in 0.002s
OK

----------------------------------------------------------------------
Класс TestResult используется для сбора информации о результатах прохождения тестов.

test_runner_4.py


Класс TextTestRunner
Объекты класса TextTestRunner используются для запуска тестов. Среди
параметров, которые передаются конструктору класса, можно выделить verbosity , по
умолчанию он равен 1, если создать объект с verbosity=2 , то будем получать
расширенную информацию о результатах прохождения тестов. Для запуска тестов
используется метод run() , которому в качестве аргумента передается класс-наследник
от TestCase или группа ( TestSuite ).

В наших примерах TextTestRunner используется в модуле test_runner_4.py в строчках:
runner = unittest.TextTestRunner(verbosity=2)
testResult = runner.run(suites)
В первой строке создается объект класса TextTestRunner с verbosity=2 , а во
второй строке запускаются тесты из группы suites , результат тестирования попадает в
объект testResult , атрибуты которого можно анализировать в дальнейшем.


-------------------------------------------

Пропуск тестов

calc.py   calc_tests.py  	test_runner_5.py

При запуске теста все протестируется. Исключим тест test_add из списка тестов.

Для пропуска теста воспользуемся декоратором
@unittest.skip(reason) , который пишется перед тестом

Модифицируем класс CalcBasicTests из модуля calc_tests.py .
class CalcBasicTests ( unittest.TestCase ):
    @unittest.skip("Temporary skip test_add")
    def test_add ( self ):
        self.assertEqual(calc.add( 1 , 2 ), 3 )
    def test_sub ( self ):
        self.assertEqual(calc.sub( 4 , 2 ), 2 )
    def test_mul ( self ):
        self.assertEqual(calc.mul( 2 , 5 ), 10 )
    def test_div ( self ):
        self.assertEqual(calc.div( 8 , 4 ), 2 )

"""
test_add (calc_tests.CalcBasicTests) ... skipped 'Temporarily skipped'
test_div (calc_tests.CalcBasicTests) ... ok
test_mul (calc_tests.CalcBasicTests) ... ok
test_sub (calc_tests.CalcBasicTests) ... ok
test_pow (calc_tests.CalcExTests) ... ok
test_sqrt (calc_tests.CalcExTests) ... ok
-------------------------------------------------------------------
Ran 6 tests in 0.003s
OK (skipped=1)
"""

	Условный пропуск тестов

Для условного пропуска тестов применяются следующие декораторы:
@unittest.skipIf(condition, reason)
Тест будет пропущен, если условие ( condition ) истинно.
@unittest.skipUnless(condition, reason)
Тест будет пропущен если, условие ( condition ) не истинно.

Условный пропуск тестов можно использовать в ситуациях, когда те или иные
тесты зависят от версии программы, например: в новой версии уже не поддерживается
часть методов; или тесты могут быть платформозависимые, например: ряд тестов
могут выполняться только под операционной системой MS Windows. Условие
записывается в параметр condition , текстовое описание – в reason .



	Пропуск классов
Для пропуска классов используется декоратор @unittest.skip(reason), который
записывается перед объявлением класса. В результате все тесты из данного класса не
будут выполнены. В рамках нашего примера с математическими действиями, для
исключения из процесса тестирования методов sqrt и pow поместим декоратор skip
перед объявлением класса CalcExTests .


Модуль calc_tests.py

import unittest
import calc


class CalcBasicTests ( unittest.TestCase ):
    def test_add ( self ):
        self.assertEqual(calc.add( 1 , 2 ), 3 )
    def test_sub ( self ):
        self.assertEqual(calc.sub( 4 , 2 ), 2 )
    def test_mul ( self ):
        self.assertEqual(calc.mul( 2 , 5 ), 10 )
    def test_div ( self ):
        self.assertEqual(calc.div( 8 , 4 ), 2 )


@unittest.skip("Skip CalcExTests")
class CalcExTests ( unittest.TestCase ):
    def test_sqrt ( self ):
        self.assertEqual(calc.sqrt( 4 ), 2 )
    def test_pow ( self ):
        self.assertEqual(calc.pow( 3 , 3 ), 27 )

"""
Результат будет следующим:
test_add (calc_tests.CalcBasicTests) ... ok
test_div (calc_tests.CalcBasicTests) ... ok
test_mul (calc_tests.CalcBasicTests) ... ok
test_sub (calc_tests.CalcBasicTests) ... ok
test_pow (calc_tests.CalcExTests) ... skipped 'Skip CalcExTests'
test_sqrt (calc_tests.CalcExTests) ... skipped 'Skip CalcExTests'
----------------------------------------------------------------------
Ran 6 tests in 0.001s
OK (skipped=2)
"""

