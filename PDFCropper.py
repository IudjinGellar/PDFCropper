from PyPDF2 import PdfWriter, PdfReader
import tkinter as tk
import tkinter.filedialog as tkf
from os.path import exists
from os import sep as os_sep

def crop(widgets): 
	filepath = widgets['file_path_entry'].get()
	page_from = widgets['page_from_wg'].get()
	page_to = widgets['page_to_wg'].get()
	new_file_name = widgets['new_file_name_wg'].get() 
	save_path = widgets['new_file_path_ent'].get()

	# проверка и преобразование введенных данных
	check_file = exists(filepath)
	if not check_file:
		widgets['message_lbl'].config(text='Нет такого файла!')
		return
	try: 
		page_from = int(page_from) -1 
		page_to = int(page_to) - 1 
	except ValueError:
		widgets['message_lbl'].config(text='Страницы должны быть числами!')
		return
	try :
		assert page_to - page_from >= 0, Exception
	except AssertionError:
		widgets['message_lbl'].config(text='Некорректно введены страницы')
		return
	check_new_filename = new_file_name.isalnum()
	if not check_new_filename: 
		widgets['message_lbl'].config(text='Имя файла только из букв и цифр.')
		return
	check_save_path = exists(save_path)
	if not check_save_path: 
		widgets['message_lbl'].config(text='Несуществующая директория для сохранения')
		return

	new_file_name = save_path + os_sep + new_file_name + '.pdf'
	reader = PdfReader(filepath)
	writer = PdfWriter()
	current_page = page_from
	for times in range(page_to-page_from + 1):
		writer.add_page(reader.pages[current_page])
		current_page += 1
	with open(new_file_name, 'wb') as new_file:
		writer.write(new_file)
	widgets['message_lbl'].config(text='Успешно!')


def clear_fields(widgets):
	try : widgets['file_path_entry'].delete(0, tk.END)
	except KeyError: pass
	try: widgets['page_from_wg'].delete(0, tk.END)
	except KeyError: pass
	try: widgets['page_to_wg'].delete(0, tk.END)
	except KeyError: pass 
	try: widgets['new_file_name'].delete(0, tk.END)
	except KeyError: pass 
	try: widgets['new_file_path_ent'].delete(0, tk.END)
	except KeyError: pass
	widgets['message_lbl'].config(text = 'Отчищено')
	
def choose_file(widgets):
	filepath = tkf.askopenfile(filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")], \
		title = 'Выбор файла').name
	widgets['file_path_entry'].delete(0, tk.END)
	widgets['file_path_entry'].insert(0, filepath)

def choose_dir(widgets):
	dirpath = tkf.askdirectory(title='Выбор папки для сохранения файла')
	widgets['new_file_path_ent'].delete(0, tk.END)
	widgets['new_file_path_ent'].insert(0, dirpath)


def create_gui():
	root = tk.Tk()
	root.title('PDFCropper')
	widgets = {} # редактируемые виджеты для обращения из функций

	# ввод файла для обрезки
	filename_frame = tk.Frame(root)
	file_path_entry = tk.Entry(filename_frame, width=20)
	file_path_entry.pack(side = tk.LEFT)
	file_path_choose = tk.Button(filename_frame, text='Select file', command = (lambda: choose_file(widgets)))
	file_path_choose.pack(side = tk.RIGHT)
	filename_frame.pack(side = tk.TOP)

	# ввод деталей обрезки
	input_frame = tk.Frame(root)
	tk.Label(input_frame, text = 'Вырезать страницы:').pack(side=tk.LEFT)
	page_from_wg = tk.Entry(input_frame, width=4)
	page_from_wg.pack(side=tk.LEFT)
	tk.Label(input_frame, text='-').pack(side=tk.LEFT)
	page_to_wg = tk.Entry(input_frame, width=4)
	page_to_wg.pack(side = tk.LEFT)
	input_frame.pack()

	# данные нового файла
	new_file_frame = tk.Frame(root)
	tk.Label(new_file_frame, text='Имя нового файла:').pack(side=tk.LEFT)
	new_file_name_wg = tk.Entry(new_file_frame, width=10)
	new_file_name_wg.pack(side=tk.LEFT)
	tk.Label(new_file_frame, text='.pdf').pack(side=tk.RIGHT)
	new_file_frame.pack(side=tk.TOP)
	new_file_path_frame = tk.Frame(root)
	new_file_path_ent = tk.Entry(new_file_path_frame)
	new_file_path_ent.pack(side=tk.LEFT)
	tk.Button(new_file_path_frame, text='Сохранить в', command = (lambda : choose_dir(widgets))).pack(side=tk.RIGHT)
	new_file_path_frame.pack(side=tk.TOP)
	
	# кнопки действий
	btns_frame = tk.Frame(root)
	tk.Button(btns_frame, text='Обрезать', command = (lambda: crop(widgets))).pack(side = tk.RIGHT)
	tk.Button(btns_frame, text='Отчистить', command = (lambda: clear_fields(widgets))).pack(side=tk.RIGHT)
	btns_frame.pack(side = tk.TOP)
	
	# поле сообщений
	output_frame = tk.Frame()
	message_lbl = tk.Label(output_frame, text = '')
	message_lbl.pack()
	output_frame.pack(side=tk.TOP)

	widgets['root'] = root
	widgets['file_path_entry'] = file_path_entry
	widgets['page_from_wg'] = page_from_wg
	widgets['page_to_wg'] = page_to_wg
	widgets['new_file_name_wg'] = new_file_name_wg
	widgets['new_file_path_ent'] = new_file_path_ent
	widgets['message_lbl'] = message_lbl
	return widgets

if __name__ == '__main__':
	widgets = create_gui()
	widgets['root'].mainloop()

