####   Переменные 
###### def
###### void
#### Базовые типы
#### Объектные типы
###### Логический 
###### Численные 
###### Строки
###### Коллекции
###### Closure
#### Операторы условного выполнениея 
#### Циклы
#### ОПП
###### Классы 
###### Интерфейсы 
###### Абстрактрные методы и классы
###### Шаблон объявления
###### Модификаторы
###### Наследование
###### Полиморфизм 
###### Инкапсуляция

#####   Переменные 
```
Общий вид объявления переменной
    <модификаторы> <def|Тип> variableName[= value ]
    - модификаторы могут быть использованы для управления доступом к переменным и их инициализацией
        - static статический метод, которое доступно без создания экземпляра 
        - final не позволяет измениение пеерменной
        - protected доступен внутри класса
        - public (по умолчанию) доступен из любого места
        - private ограничение доступа внутри самого класса
        - abstract метод который дожен быть реализован в подклассах
    - def используется для объявления переменной без явного указания типа (тип пеерменной определяется при получении значения)
        def myVariable              // объявление переменной без указания типа
        myVariable = 'Hello World'  // переменная получает тип string
    - void (в отличие от def функция не ожидает возврата какого-либо значения) а ля процедура из pascal
        методы не возвращают никаких значений, они выполняют действие или меняют состояние объекта

// объявление переменной с использованием def
def firstName
// явное указание типа для строковой переменной
String lastName = "Smith"

// объявление числовой переменой с использоваинем def
def age = 30
// явное указание типа для числовой переменной
Integer year = 2023

// объявление логической переменной с использованием def
def isTrue = true
// явное указание типа для логической переменной
Boolean active = false

// объявление коллекции с использованием def
def numbers = [1, 2, 3]
def names = ["John", "May", "Bob"]
def grades = ["John": 90, "May": 85, "Bob": 75]

// явное указание типа коллекции
List<Integer> ages = [10, 20, 30]
Map<String, Integer> gragesMap = ["John": 90, "May": 85, "Bob": 75]
```
##### Базовые типы
```
boolean  - логический тип true/false
byte     - целочисленный тип 1 байт от -128 до 127 
char     - символ Unicode
shot     - целочисленный тип 2 байта от -32768 до 32767
int      - целочисленный тип 4 байта 
long     - целочисленный тип 8 байта 
float    - числовой тип с плавающей точкой в 4 байта 
double   - числовой тип с плавающей точкой в 8 байта 
```
##### Объектные типы
```
####### Логический 
```
```groovy
def boolVar = true
def boolObj = new Boolean(true)
Boolean bool = true

println (boolVar ? "boolVar is true" : "boolVar is False")
if (boolObj && bool) {
    print ("boolObj and bool is true")
}

// преобразование другий типов данных в логиченские при возможности 
def nullVal = null
def emptyStr = ""
def zero = 0

if (!nullVal && !emptyStr && zero !=0) {
    println ("At least one condition is true")
}
```
####### Строки
```groovy
// '' - строка как есть 
// "" - можно подставлять значениея

def variable = 'value'
def v1 = "This string ${variable}"
// замыкание здесь идет попадание динамичекое NewValue - которое переопределили
def v2 = "This string ${ -> variable}"
println (v1)   // value
println (v2)   // value
variable = 'NewValue'
println (v1)   // value
println (v2)   // NewValue

// удаление пробелов в начале до |
def Myfunc:String = """
                    |line1
                    |line2
                    |line3
                    """.stringMarging()
println (Myfunc)

```
####### метод c явным именем
```groovy
def name_metthod (def variable){
    println variable
}

name_metthod('test')
name_metthod(123)
name_metthod(['a','b'])
```
####### Closure

```groovy
// здесь метод не имеет явного имени от представлен в виде Closure
metthod {def variable ->
    println variable
}

method('test')
method(123)
method(['a','b'])
```
```
##### Операторы условного выполнениея 
```
```groovy
// if-else
if (condition) {
    // some code
} else {
    // some code
}
// ternary operator
boolean someCondition = true
String value = someCondition ? "true" : "false"
int max = someValue > otherValue ? someValue : otherValue

// switch
switch (somevalue) {
    case 1:
        // some code when value is 1
        break
    case 2:
        // some code when value is 2
        break 
    default:
        // some code for all other value
        break 

}

// elvis operator 
// например - обращаемся к полю username, но не увеерны что оно есть 
// чтобы не упасть с ошибкой присваиваем значение, Anonymoys
string username = profile?.username : "Anonymoys" 
```
```
##### Циклы
```
```groovy
// цикл для итерации по списку
def names = ["John", "May", "Bob"]
for (name in names) {
    println(name)
}

// 
for (i in 1..10){
    println(i)
}
//
for (int i = 0; i<10; i++) {
    println(i)
}

// Foreach loop
// для итерации по списку
def names = ["John", "May", "Bob"]
names.each { name ->
    println(name)
}
names.each {println(it)}
names.eachWithIndex { name, index ->
    println("Element with index ${index} = " + name)
}

//для итерации по ключам
def grades = ["John": 90, "May": 85, "Bob": 75]
grades.each { key, value ->
    println("$key: $value")
}
grades.each {
    println ("$it.key: $it.value")
}

// проверка условия и выполнение кода пока условие истино
def counter = 0
while (counter <10) {
    println(counter)
    counter++
}

// чтение ввода до момента ввода определенного значения
def input = ""
while (input != "quit") {
    println ("enter: ")
    input = System.console().readLine()
}
// выполение кода хоть раз
def input = ""
do {
    println ("enter: ")
    input = System.console().readLine()
} while (input != "quit") 

// проверак на корректность воода
def password = ""
do {
    println ("enter: ")
    password = readPasssword()
} while (password.length() < 8) 


```
##### ОПП
```
```
###### Классы 
```
```
```groovy
class ColoredText {
    String text
    String color

    ColoredText (String text, String color) {     // Конструктор - вызывается при создании нового объекта
        this.text = text
        this.color = color
    }
    String formatTextWithANSICode() {
        return "\u001b [${color}m$text\u001b[0m"
    }
} 

// класс без явного конструктора
class Example {
    String name
    Integer age
}
// конструктор по умолчанию (пример)
Example (String name, Integer age) {
    this.name = name
    this.age = age
}

// Суперконструктор если наследуемся от другого класса
class Superclass {
    String name
}

class Subcalss extends SuperClass {
    Integer age
    Subclass (String name, Integer age) {
        super (name)
        this.age =age
    }
}

// setter - метод принимает значение и устанавливает его в поле 
// getter - метод который возвращет значение поля 
class Person {
    int age = 0

    Person (int age) {
        this.age = age
    }
    int getAge () {
        return age
    }
    void setAge (int newAge) {
        age = newAge > age ? newAge : age
    }
}
```

###### Полиморфизм 
```
реализация добавления ФИО разными способами 
```
```groovy
interface Person {
    // перегрузка методов
    void initFullName (
        String firstName,
        String lastName
    )
    void initFullName (
        List<String> fullname
    )
}

Class Empoloyee implements Person {
    //----
@Override void initFullName (String firstName, String lastName)
        {this.fullname = "$firstName $lastName"}
@Override void initFullName (List<String> fullname)
        {this.fullname = fullname.join(" ")}
}
```
###### Инкапсуляция
```
```
```groovy

```

