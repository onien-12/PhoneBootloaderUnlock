from subprocess import getoutput as system
from time import sleep
from os import system as ossystem

import time

def pressAnyKey(msg = "Нажмите любую клавишу..."):
	input(msg);
	exit();


class Phone:
	def __init__(self, checkCommand = "adb get-state print bootloader"):
		super();
		self.check = checkCommand;
		self.phone = False;
		self.Bootloader.__init__(self.Bootloader);

	def StartCheck(self):
		check = system(self.check)
		if ("error: no devices/emulators found" in check) or ("unauthorized" in check):
			while 1:
				sleep(1)
				ossystem("cls")

				check = system(self.check)

				if "error: no devices/emulators found" in check:
					print("Ожидание подключения смартфона...")
					continue

				elif "unauthorized" in check:
					print("Устройство было подключено, но нужно включить отладку по usb...")
					continue

				else:
					print("Устройство было подключено.")
					self.phone = True;
					return True;

	@property	
	def DeviceEnabled(self):
		if ("no devices/emulators found" in system(self.check)): return False;
		else: return True;

	def reboot(self, where = ""):
		ossystem("adb reboot " + where);
		return True;

	def bootloader(self, action):
		if (action == "getinfo"):
			self.Bootloader.vars = self.Bootloader.infoBoot["before"] = system("fastboot getvar all");

			BootloaderVars = open("1_infoBoot.txt", "w")
			BootloaderVars.write(self.Bootloader.vars)
			BootloaderVars.close()

			return self.Bootloader.vars;
		if (action == "unlock"):
			self.Bootloader.infoBoot["after"] = UnlockInfo = system("fastboot flashing unlock");

			BootloaderVarsCheck = open("2_infoBoot.txt", "w")
			BootloaderVarsCheck.write(UnlockInfo)
			BootloaderVarsCheck.close()

			if "Command failed" in UnlockInfo:
				if "Key not match, Please input correct key!" in UnlockInfo:
					error = "ключ разблокировки не совпадает!"
				print("Ошибка: fastboot: отдтанная команда не выполнена {errorcode}".format(errorcode=UnlockInfo))
				self.Bootloader.unlock = False;
				return False;

			self.Bootloader.unlock = True;
			return True;

		if (action == "check"):
			try: 
				readinfo = open('2_infoBoot.txt').read().split('\n')[95]
				if "unlocked: no" in readinfo:
					print("Неудачно!")
					self.Bootloader.unlock = False;

				elif "unlocked: yes" in readinfo:
					print("Успешно!")
					self.Bootloader.unlock = True;

			except IndexError:
				readinfo = open('2_infoBoot.txt').read();
				if "Key not match, Please input correct key!" in readinfo:
					print("Неудачно!")
					self.Bootloader.unlock = False;

				else:
					print("Успешно!")
					self.Bootloader.unlock = True;

			

			return self.Bootloader.unlock;


	class Bootloader:
		def __init__(self):
			self.vars = None;
			self.infoBoot = {
				"before": None,
				"after": None
			};
			self.unlock = False;

		def reboot():
			ossystem("fastboot reboot");
			return True;


App = Phone();

App.StartCheck(); #проверка на подключение

wantToContinue = input("Хотите продолжить (на свой страх и риск)? (y/N): ").lower();
if (wantToContinue == "y"): pass;
else: pressAnyKey();

if (input("yes/no").lower() == "yes"): print("Продолжаем...");
else: pressAnyKey();


if (not App.DeviceEnabled): 
	print("Устройство было отключено!\n Продолжение невозможно!");
	pressAnyKey();

print('Перезагрузка в fastboot...', end='')
App.reboot("bootloader");
print("Успешно!")


print("Получение сведений системы загрузчика..." , end='')
timeCount = time.time();
App.bootloader("getinfo");
print("Успешно! in " + str(time.time() - timeCount) + "s");


print("Разблокировка смартфона..." , end='')
timeCount = time.time();
App.bootloader("unlock");
App.bootloader("check");
print(str(time.time() - timeCount) + "s");


print("Перезагрузка смартфона...", end='')

App.Bootloader.reboot();

print("Команда была отдана смартфону!\nВключение...", end='')


while 1:

	sleep(5)

	chk = App.DeviceEnabled;

	if (not chk): continue;
	else: break;

print("Телефон был включен!");

input()