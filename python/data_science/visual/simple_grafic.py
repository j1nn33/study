from matplotlib import pyplot as pit
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]             # годы
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]  # ВВП

# создать линейную диаграмму: годы по оси X, ВВП по оси Y
pit.plot(years, gdp, color='green', marker='o', linestyle='solid')

# добавить название диаграммы
pit.title("Номинальный ВВП")
# добавить подпись к оси Y
pit.ylabel("Млрд $")
pit.show